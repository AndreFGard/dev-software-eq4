from schemas import *
from typing import List

class User():
    username: str
    message_history: List[DBMessage]
    __activities__: dict[int, Activity]
    status: UserStatus = UserStatus.DISCUSSING

    def __init__(self, username="John Doe", message_history=[]):
        self.username = username
        if not message_history:
            message_history = [DBMessage(role='assistant', content="Hello! I'm a travel planner. Where would you like to travel today?")]

        self.message_history = message_history
        self.__activities__ = {}
        self.status = UserStatus.DISCUSSING
        self.schedules: list[Schedule] = []


    def addMessage(self, msg: Message):
        role = "assistant"

        if msg.username != "assistant":
            role = "user"
        msg.id = 1 if len(self.message_history) == 0 and msg.id is None else self.message_history[-1].id + 1
        self.message_history.append(DBMessage(role=role, content=msg.content, id=msg.id))
    
    def addSchedule(self, sched: Schedule):
        self.schedules.append(sched)
    
    # retorna cada mensagem do historico no formato de Message
    def getMessageHistory(self) -> List[Message]:

        return [Message(username= self.username if item.role == "user" else "assistant", content=item.content, id = item.id) for item in self.message_history]
    
    def getMessageById(self, id:int):
        return next((msg for msg in self.message_history if msg.id == id), None)

    def dumpGPTMessages(self):
        return [{"role": m.role, "content": m.content} for m in self.message_history]
    
    def addActivity(self, act: Activity):
        act.id = 1 if act.id is None else act.id
        self.__activities__[act.id] = act
        
    def getSchedule(self, username:str):
        return self.schedules[-1] if len(self.schedules) else None
    def getActivities(self):
        return self.__activities__
    
    def dumpActivities(self):
        return {id:act.model_dump() for id,act in self.getActivities().items()}


