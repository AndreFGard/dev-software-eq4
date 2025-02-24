from schemas import *
from typing import List

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
        self._activity_id_counter =0
        self._message_id_counter=-1

    def addMessage(self, msg: Message):
        role = "assistant"

        if msg.username != "assistant":
            role = "user"

        self._message_id_counter +=1
        self.message_history.append(GptMessage(role=role, content=msg.content, id=self._message_id_counter+1))
        
    
    # retorna cada mensagem do historico no formato de Message
    def getMessageHistory(self) -> List[Message]:

        return [Message(username= self.username if item.role == "user" else "assistant", content=item.content, id = item.id) for item in self.message_history]
    
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
        return {id:act.model_dump() for id,act in self.getActivities().items()}


