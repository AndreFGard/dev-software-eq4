from pydantic import BaseModel
from typing import List, Dict, Optional
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

# -----------------------------
# Repository for User Data
# -----------------------------
class UserRepository:
    def __init__(self):
        self.users: Dict[str, User] = {}

    def get(self, username: str) -> User:
        if username not in self.users:
            self.add(username)
        return self.users[username]

    def add(self, username: str):
        if username not in self.users:
            self.users[username] = User(username)

    def __repr__(self):
        return f"UserRepository(users={self.users})"


# -----------------------------
# Repository for Message History
# -----------------------------
class MessageRepository:
    def __init__(self):
        self.message_history: Dict[str, List[DBMessage]] = {}

    def initialize_for_user(self, username: str):
        self.message_history[username] = [
            DBMessage(
                role='assistant',
                content="Hello! I'm a travel planner. Where would you like to travel today?",
                id=1
            )
        ]

    def get_history(self, username: str) -> List[DBMessage]:
        return self.message_history.get(username, [])

    def add_message(self, username: str, message: Message):
        if username not in self.message_history:
            self.initialize_for_user(username)
        messages = self.message_history[username]
        role = "user" if message.username != "assistant" else "assistant"
        if message.id is None:
            message.id = 1 if not messages else messages[-1].id + 1
        db_message = DBMessage(role=role, content=message.content, id=message.id)
        messages.append(db_message)
        return message.id

    def get_message_by_id(self, username: str, id: int) -> Optional[DBMessage]:
        messages = self.message_history.get(username, [])
        return next((msg for msg in messages if msg.id == id), None)

    def dump_gpt_messages(self, username: str) -> List[dict]:
        messages = self.get_history(username)
        return [{"role": m.role, "content": m.content} for m in messages]

    def get_message_history(self, username: str) -> Dict[int, Message]:
        messages = self.get_history(username)
        # Transform DBMessage to Message model
        return {
            msg.id: Message(
                username=username if msg.role == "user" else "assistant",
                content=msg.content,
                id=msg.id
            )
            for msg in messages
        }

    def get_gpt_message_history(self, username: str) -> List[GPTMessage]:
        messages = self.get_history(username)
        return [GPTMessage(role=msg.role, content=msg.content) for msg in messages]

    def __repr__(self):
        return f"MessageRepository(message_history={self.message_history})"


# -----------------------------
# Repository for Activities
# -----------------------------
class ActivityRepository:
    def __init__(self):
        self.activities: Dict[str, Dict[int, Activity]] = {}

    def initialize_for_user(self, username: str):
        self.activities[username] = {}

    def get_activities(self, username: str) -> List[Activity]:
        return list(self.activities.get(username, {}).values())

    def add_activity(self, username: str, act: Activity):
        if username not in self.activities:
            self.initialize_for_user(username)
        if act.id is None:
            act.id = len(self.activities[username]) + 1
        self.activities[username][act.id] = act

    def delete_activity(self, username: str, act_id: int):
        if username in self.activities and act_id in self.activities[username]:
            del self.activities[username][act_id]
        else:
            raise ValueError(f"Activity with id {act_id} not found for user {username}")

    def update_activity(self, username: str, act_id: int, act: Activity):
        if username not in self.activities or act_id not in self.activities[username]:
            raise ValueError("Activity not found")
        self.activities[username][act_id] = act
        return self.activities[username]

    def dump_activities(self, username: str) -> Dict[int, dict]:
        return {act_id: act.model_dump() for act_id, act in self.activities.get(username, {}).items()}

    def __repr__(self):
        return f"ActivityRepository(activities={self.activities})"


# -----------------------------
# Repository for Schedules
# -----------------------------
class ScheduleRepository:
    def __init__(self):
        self.schedules: Dict[str, List[Schedule]] = {}

    def initialize_for_user(self, username: str):
        self.schedules[username] = []

    def add_schedule(self, username: str, sched: Schedule):
        if username not in self.schedules:
            self.initialize_for_user(username)
        self.schedules[username].append(sched)

    def get_latest_schedule(self, username: str) -> Optional[Schedule]:
        if username not in self.schedules:
            raise ValueError(f"User: {username} was not found in the database")
        scheds = self.schedules.get(username, [])
        return scheds[-1] if scheds else None

    def __repr__(self):
        return f"ScheduleRepository(schedules={self.schedules})"


# -----------------------------
# Repository for Favorite Messages
# -----------------------------
class FavoriteMessageRepository:
    def __init__(self):
        self.favorite_messages: Dict[str, List] = {}

    def initialize_for_user(self, username: str):
        self.favorite_messages[username] = []

    def get_favorites(self, username: str) -> List:
        return self.favorite_messages.get(username, [])

    def __repr__(self):
        return f"FavoriteMessageRepository(favorite_messages={self.favorite_messages})"


# -----------------------------
# Composite Repository / Service
# -----------------------------
class UserDB:
    def __init__(self):
        self.user_repo = UserRepository()
        self.msg_repo = MessageRepository()
        self.activity_repo = ActivityRepository()
        self.schedule_repo = ScheduleRepository()
        self.fav_repo = FavoriteMessageRepository()

    def addUser(self, username: str):
        self.user_repo.add(username)
        self.msg_repo.initialize_for_user(username)
        self.activity_repo.initialize_for_user(username)
        self.schedule_repo.initialize_for_user(username)
        self.fav_repo.initialize_for_user(username)

    def getUser(self, username: str) -> User:
        if username not in self.user_repo.users:
            self.addUser(username)
        return self.user_repo.get(username)

    def getMessageHistory(self, username: str) -> Dict[int, Message]:
        return self.msg_repo.get_message_history(username)

    def getGPTMessageHistory(self, username: str) -> List[GPTMessage]:
        return self.msg_repo.get_gpt_message_history(username)

    def getMessageById(self, username: str, id: int) -> Optional[DBMessage]:
        return self.msg_repo.get_message_by_id(username, id)

    def addMessage(self, username: str, message: Message):
        if username not in self.user_repo.users:
            self.addUser(username)
        return self.msg_repo.add_message(username, message)

    def dumpGPTMessages(self, username: str):
        return self.msg_repo.dump_gpt_messages(username)

    def getActivities(self, username: str) -> List[Activity]:
        return self.activity_repo.get_activities(username)

    def addActivity(self, username: str, act: Activity):
        if username not in self.user_repo.users:
            self.addUser(username)
        self.activity_repo.add_activity(username, act)

    def deleteActivity(self, username: str, act_id: int):
        self.activity_repo.delete_activity(username, act_id)

    def updateActivity(self, username: str, act_id: int, act: Activity):
        return self.activity_repo.update_activity(username, act_id, act)

    def dumpActivities(self, username: str):
        return self.activity_repo.dump_activities(username)

    def addSchedule(self, username: str, sched: Schedule):
        if username not in self.user_repo.users:
            self.addUser(username)
        self.schedule_repo.add_schedule(username, sched)

    def getSchedule(self, username: str) -> Optional[Schedule]:
        return self.schedule_repo.get_latest_schedule(username)

    def __repr__(self):
        return (
            f"UserDB(\n"
            f"  Users: {self.user_repo},\n"
            f"  Favorite Messages: {self.fav_repo}\n"
            f")"
        )

