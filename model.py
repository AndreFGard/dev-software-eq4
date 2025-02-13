from pydantic import BaseModel
from typing import List
from enum import Enum
from openai import OpenAI, AsyncOpenAI
import random
import pandas as pd
import numpy as np

import time
import asyncio as aio


# classe de mensagens do role: user
class Message(BaseModel):
    username: str
    content: str
    is_activity: bool = False

# classe de mensagens do estilo gpt, o content é obtido pelo Message.content
class GptMessage(BaseModel):
    role: str
    content: str

#todo: implementar a logica de achar uma cidade mais apropriadamente
class City(BaseModel):
    name:str
    state:str
    country:str
    data:dict
    id: int

    def __init__(self, name:str, state:str, country:str, data:dict, id:int):
        self.name = name
        self.state = state
        self.country = country
        self.data = data
        self.id = id

class CityValidator:
    def __init__(self):
        fileurl='https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/refs/heads/master/json/countries%2Bstates%2Bcities.json'
        
        j = pd.read_json(fileurl)

        countries = {j.loc[idx, "name"]:j.loc[idx, "states"] for idx in j.index}
        cities = {}
        city_ids = {}

        for country, states in countries.items():
            for state in states:
                for city in state['cities']:
                    if city['name'] not in cities:
                        cities[city['name']] = {}

                    cities[city['name']] = {'name': city['name'], 'state': state['name'], 'country': country, 'data': city, 'id': city['id']}
                    city_ids[city['id']] = city
        
        self.countries = countries
        self.cities = cities
        self.city_ids = city_ids

    # considerar translocar estas funções para uma outra classe e instanciar ela para obter a base de dados

    def identifier(self, city:str, state:str, country:str) -> int:
        if not self.valid(city, state, country):
            return -1
        
        return self.cities[city]['id']

    def valid(self, city, state, country) -> bool:
        if np.where(self.countries.keys() == country)[0].size == 0:
            return False

        if np.where(self.cities.keys() == city)[0].size == 0:
            return False
        
        if np.where(self.cities[city]['state'] == state)[0].size == 0:
            return False
        
        return True

    def city_matches_name(self, name: str) -> List[City]:
        """"Retorna todas as cidades com o mesmo nome"""
        return self.cities['Recife']
    
    #TODO
    def city_matches_name_state(self, name: str, state: str) -> List[City]:
        return self.cities['Recife'] # sample

# classe que vai ter as informações de um lugar
class Place:
    country: str
    state: str
    city : City

    def __init__(self, country, state, city):
        self.country = country
        self.state = state
        self.city = city

    # checando se o lugar existe no banco de dados
    def find(self, country, state, city) -> bool:
        return True

async def answerDummy(*args, **kwargs):
    buzzwords = ["voce nao esta usando o chatgpt, forneca uma OPENAI_KEY\n", "- **Design Science Research**:\n1. isso é uma lista\n2. ainda é uma lista", ""]
    await aio.sleep(2)
    return " ".join(random.sample(buzzwords, 3) )


class Activity(BaseModel):
    name: str
    short_description: str
    long_description: str

class UserStatus(Enum):
    DISCUSSING = 'discussing'
    SUMMARIZING_ACTIVITIES = 'summarizing_activities'
    MODIFYING_ACTIVITY = 'modifying_activity'

prompts = {
    UserStatus.DISCUSSING: 'You are a quiet travel planner helping a tourist. Don\'t answer questions unrelated to this.',
    UserStatus.SUMMARIZING_ACTIVITIES: """You are summarizing the chosen activities below for the tourist.
    Please summarize them as a list of activities, each with values for name, short_description, and long_description.""",
    UserStatus.MODIFYING_ACTIVITY: 'You are modifying an activity for the tourist.'
}

user_list = {}

class User():
    username: str
    message_history: List[GptMessage]
    __activities__: dict[int, Activity]
    status: UserStatus = UserStatus.DISCUSSING

    def __init__(self, username="John Doe", message_history=[]):
        self.username = username
        if not message_history:
            message_history = [GptMessage(role='assistant', content="Hello! I'm a travel planner. Where would you like to travel today?")]

        self.message_history = message_history
        self.__activities__ = {}
        self.status = UserStatus.DISCUSSING

    def addMessage(self, msg: Message):
        role = "assistant"

        if msg.username != "assistant":
            role = "user"

        self.message_history.append(GptMessage(role=role, content=msg.content))
    
    # retorna cada mensagem do historico no formato de Message
    def getMessageHistory(self) -> List[Message]:

        return [Message(username= self.username if item.role == "user" else "assistant", content=item.content) for item in self.message_history]
    
    def dumpHistory(self):
        return[m.model_dump() for m in self.message_history]
    
    def addActivity(self, act: Activity,id=-1):
        if id == -1 : 
            id = self._activity_id_counter
        else: self._activity_id_counter += 1
        
        self.__activities__[id] = act
        
    
    def getActivities(self):
        return self.__activities__
    
    def dumpActivities(self):
        return {id:act.model_dump for id,act in self.getActivities().items()}


class OpenaiInteface:
    """Essa classe proverÁ (quando isso for implementado) 
    as respostas de um chatbot.
    Essa classe deve preparar os parametros, prompts e outras coisas
    Parameters:
    useDummy (bool): usar um chatbot fake ou não;."""

    def __init__(self, useDummy=True, openai_key="", **kwargs):
        self.openai = None
        self.__openai_key__ = openai_key
        useDummy = useDummy or not openai_key
        if (useDummy):
            #nao usar o chatgpt de verdade
            self.openai = None
        else:
            self.openai = AsyncOpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=self.__openai_key__
            )

        self.model='llama3-8b-8192'
    
    def getSystemMessage(self, user: User):
        return [GptMessage(role='system',content=prompts[user.status]).model_dump()]

    async def reply(self, user:User):
        if self.openai:
            return await self.completion(user)
        else: 
            return await answerDummy(user)

    async def completion(self, user: User):
        choice = ""
        messages=self.getSystemMessage(user) + user.dumpHistory()
        completion = await self.openai.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion.choices[0].message.content



# banco de dados de usuarios (provisorio)
user_list = {"André" : User(username="André", message_history=[GptMessage(role="user", content="Se estou lendo isso, é porque deu certo")])}

class City(BaseModel):
    name:str
    state:str
    country:str
    data:dict
    id: int

class CityValidator:
    def __init__(self):
        import json
        filename="countrie_states_cities.json"
        fileurl='https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/refs/heads/master/json/countries%2Bstates%2Bcities.json'
        f = None
        try:
            f = open(filename)
        except:
            import os
            os.system(f"curl {fileurl} -o {filename}")
            f = open(filename)
        j = json.load(f)
        countries = {ct["name"]:ct for ct in j}
        cities ={}
        city_ids = {}
        for ct in countries.values():
            ct['states'] = {st["name"]:st for st in ct['states']}
            for st in ct["states"].values():
                st['cities'] = {city['name']:city for city in st['cities']}
                for city in st['cities'].values():
                    if city['name'] not in cities:
                        cities[city['name']] = []
                    
                    cities[city['name']].append({'name':city['name'], 'state': st['name'], 'country': ct['name'], 'data':city, 'id':city['id']})
                    city_ids[city['id']] = city
        
        self.countries = countries
        self.cities = cities
        self.city_ids = city_ids

    #TODO
    def city_matches_name(self, name:str) ->List[City]:
        """"Retorna todas as cidades com o mesmo nome"""
        return self.cities['Recife']
        pass
    
    #TODO
    def city_matches_name_state(name:str, state:str) -> List[City]:
        pass

class City(BaseModel):
    name:str
    state:str
    country:str
    data:dict
    id: int

class CityValidator:
    def __init__(self):
        import json
        filename="countrie_states_cities.json"
        fileurl='https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/refs/heads/master/json/countries%2Bstates%2Bcities.json'
        f = None
        try:
            f = open(filename)
        except:
            import os
            os.system(f"curl {fileurl} -o {filename}")
            f = open(filename)
        j = json.load(f)
        countries = {ct["name"]:ct for ct in j}
        cities ={}
        city_ids = {}
        for ct in countries.values():
            ct['states'] = {st["name"]:st for st in ct['states']}
            for st in ct["states"].values():
                st['cities'] = {city['name']:city for city in st['cities']}
                for city in st['cities'].values():
                    if city['name'] not in cities:
                        cities[city['name']] = []
                    
                    cities[city['name']].append({'name':city['name'], 'state': st['name'], 'country': ct['name'], 'data':city, 'id':city['id']})
                    city_ids[city['id']] = city
        
        self.countries = countries
        self.cities = cities
        self.city_ids = city_ids

    #TODO
    def city_matches_name(self, name:str) ->List[City]:
        """"Retorna todas as cidades com o mesmo nome"""
        return self.cities['Recife']
        pass
    
    #TODO
    def city_matches_name_state(name:str, state:str) -> List[City]:
        pass

#exemplo#
rob = User(username="Robinson", message_history=[])
rob.addMessage(Message(username="robinser", content="eae"))
#print(rob.message_history)
