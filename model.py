from pydantic import BaseModel
from typing import List
import openai
import random
import pandas as pd
import numpy as np

# classe de mensagens do role: user
class Message(BaseModel):
    username: str
    content: str

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

def answerDummy(*args, **kwargs):
    buzzwords = [ "Dev Software", "Concepcao de artefatos", "????", "Forms", "Eigenvalues "
    "synergy", "pivot", ",", "mas também", "blockchain", ", além de ", "cloud-native", ".",
    "big data",]
    return " ".join(random.sample(buzzwords, 3) )

class OpenaiInteface:
    """Essa classe proverá (quando isso for implementado) 
    as respostas de um chatbot.
    Essa classe deve preparar os parametros, prompts e outras coisas
    Parameters:
    useDummy (bool): usar um chatbot fake ou não;."""
    def __init__(self, useDummy=True, **kwargs):
        self.openai = None
        self.getReply = answerDummy
        if (useDummy):
            #nao usar o chatgpt de verdade
            self.openai = None
        else:
            #inicializar o modulo openai
            #implementar aqui
            pass

# classe de usuario
class User():
    username: str
    message_history: List[GptMessage]
    
    def __init__(self, username="John Doe", message_history=[]):
        self.username = username
        self.message_history = message_history

    # adiciona mensagem comm base na role
    def addMessage(self, msg: Message):
        role = "assistant"

        if msg.username != "assistant":
            role = "user"

        self.message_history.append(GptMessage(role=role, content=msg.content))
    
    # retorna cada mensagem do historico no formato de Message
    def getMessageHistory(self) -> List[Message]:
        return [Message(username=item.role, content=item.content) for item in self.message_history]

# banco de dados de usuarios (provisorio)
user_list = {"André" : User(username="André", message_history=[GptMessage(role="user", content="Se estou lendo isso, é porque deu certo")])}

#exemplo#
rob = User(username="Robinson", message_history=[])
rob.addMessage(Message(username="robinser", content="eae"))
#print(rob.message_history)