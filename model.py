from pydantic import BaseModel
from typing import List
from enum import Enum
from openai import OpenAI, AsyncOpenAI
import random
import pandas as pd
import numpy as np
import time
import asyncio as aio

from schemas import *

from userOpenai import *
from user import User



class UserDB:
    def __init__(self):
        self.users : dict[str, User] = {} 
        self.favorite_messages = {}

    def getUser(self, username:str):
        if username in self.users:
            return self.users[username]
        else:
            self.users[username] = User(username)
            return self.users[username]

    def getMessageHistory(self, username:str) -> list[Message]:
        return self.getUser(username).getMessageHistory()

    def getMessageById(self, username:str, id:int):
        return self.users[username].getMessageById(id)

    def getActivities(self, username:str) -> list[Activity]:
        return list(self.users[username].getActivities().values())

    def deleteAcitivty(self, username:str, act_id:int):
        if username in self.users:
            if act_id in self.users[username].getActivities():
                del self.users[username].__activities__[act_id]
                return 
        raise ValueError(f"Activity with id {act_id} not found for user {username} or username not found in database")

    def addUser(self, username:str):
        if username not in self.users:
            self.users[username] = User(username)
            self.favorite_messages[username] = []

    def addMessage(self, username:str, message:Message):
        if username not in self.users:
            self.addUser(username)
        
        if len(self.users[username].message_history):
            message.id = len(self.users[username].message_history) + 1

        self.users[username].addMessage(message)
        return message.id

    def addActivitiy(self, username:str, act: Activity):
        if username not in self.users:
            print(f"User: {username} was not found in the database. ")
            self.addUser(username)
        
        if act.id is None:
            act.id = len(self.users[username].getActivities()) + 1
        
        self.users[username].addActivity(act)



    def __repr__(self):
        return f"UserDB(users={self.users}, favorite_messages={self.favorite_messages})"
