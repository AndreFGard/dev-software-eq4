from pydantic import BaseModel
from typing import List
from enum import Enum
import random
import pandas as pd
import numpy as np

import time
import asyncio as aio

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
