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
        self.users: dict[str, User] = {}
        self.message_history: dict[str, List[DBMessage]] = {}
        self.activities: dict[str, dict[int, Activity]] = {}
        self.schedules: dict[str, List[Schedule]] = {}
        self.favorite_messages: dict[str, List] = {}

    def getUser(self, username: str) -> User:
        if username not in self.users:
            self.addUser(username)
        return self.users[username]

    def addUser(self, username: str):
        if username not in self.users:
            self.users[username] = User(username)
            self.message_history[username] = [DBMessage(role='assistant', 
                content="Hello! I'm a travel planner. Where would you like to travel today?")]
            self.activities[username] = {}
            self.schedules[username] = []
            self.favorite_messages[username] = []

    def getMessageHistory(self, username: str) -> dict[int, Message]:
        messages = self.message_history.get(username, [])
        return {msg.id: Message(
            username=username if msg.role == "user" else "assistant",
            content=msg.content,
            id=msg.id
        ) for msg in messages}
    
    def getGPTMessageHistory(self, username:str) -> list[GPTMessage]:
        messages = self.message_history.get(username, [])
        return [GPTMessage(role=msg.role, content=msg.content) for msg in messages]

    def getMessageById(self, username: str, id: int):
        messages = self.message_history.get(username, [])
        return next((msg for msg in messages if msg.id == id), None)

    def addMessage(self, username: str, message: Message):
        if username not in self.users:
            self.addUser(username)
        
        messages = self.message_history[username]
        role = "user" if message.username != "assistant" else "assistant"
        
        if message.id is None:
            message.id = 1 if not messages else messages[-1].id + 1
            
        self.message_history[username].append(
            DBMessage(role=role, content=message.content, id=message.id)
        )
        return message.id

    def getActivities(self, username: str) -> list[Activity]:
        return list(self.activities.get(username, {}).values())

    def addActivity(self, username: str, act: Activity):
        if username not in self.users:
            self.addUser(username)
        
        if act.id is None:
            act.id = len(self.activities[username]) + 1
        
        self.activities[username][act.id] = act

    def deleteActivity(self, username: str, act_id: int):
        if username in self.activities and act_id in self.activities[username]:
            del self.activities[username][act_id]
            return
        raise ValueError(f"Activity with id {act_id} not found for user {username}")

    def updateActivity(self, username: str, id: int, act: Activity):
        if username not in self.activities or id not in self.activities[username]:
            raise ValueError("Activity not found")
        self.activities[username][id] = act
        return self.activities[username]

    def addSchedule(self, username: str, sched: Schedule):
        if username not in self.users:
            self.addUser(username)
        self.schedules[username].append(sched)

    def getSchedule(self, username: str) -> Schedule | None:
        if username not in self.users:
            raise ValueError(f"User: {username} was not found in the database")
        schedules = self.schedules.get(username, [])
        return schedules[-1] if schedules else None

    def dumpGPTMessages(self, username: str):
        messages = self.message_history.get(username, [])
        return [{"role": m.role, "content": m.content} for m in messages]

    def dumpActivities(self, username: str):
        return {id: act.model_dump() for id, act in self.activities.get(username, {}).items()}

    def __repr__(self):
        return f"UserDB(users={self.users}, favorite_messages={self.favorite_messages})"