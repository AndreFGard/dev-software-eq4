from schemas import *
from typing import List
from main import db

class User():
    username: str
    shcedules: List[Schedule]

    # refatorado
    def __init__(self, username="John Doe"):
        self.username = username
        self.schedules: list[Schedule] = []

    # refatorado
    async def get_user_id(self):
        result = await db.read_data("users", {"nome": self.username})
        return result[0].user_id if result else None

    # refatorado
    async def addMessage(self, msg: Message):
        await db.add_data("MESSAGES", {
            "user_id": await self.get_user_id(),
            "content_message": msg.dict(),
            "role": msg.username if hasattr(msg, "role") else "user"
        })
    
    # refatorado -> talvez aplicar validação usando pydantic
    async def getMessageHistory(self):
        user_id = await self.get_user_id()
        result = await db.read_data("MESSAGES", {"user_id": user_id}, order_by="content_id")
        return [msg.content_message for msg in result]
    
    # refatorado
    async def getMessageById(self, id: int):
        result = await db.read_data("MESSAGES", {"content_id": id})
        return result[0].content_message if result else None

    # refatorado
    async def dumpGPTMessages(self):
        msgs = await self.getMessageHistory()
        return [{"role": m["role"], "content": m["content"]} for m in msgs]
    
    # refatorado -> talvez aplicar validação usando pydantic
    async def addActivity(self, msg: Message):
        user_id = await self.get_user_id()
        result = await db.read_data("USERS", {"user_id": user_id})
        if result:
            current_favorites = result[0].lista_favoritos or []
            current_favorites.append(msg.dict())
            await db.update_data("USERS", {"user_id": user_id}, {"lista_favoritos": current_favorites})
    
    # refatorado -> talvez aplicar validação usando pydantic
    async def getActivities(self):
        user_id = await self.get_user_id()
        result = await db.read_data("USERS", {"user_id": user_id})
        if result:
            return result[0].lista_favoritos or []
        return []
    
    # refatorado
    async def dumpActivities(self):
        acts = await self.getActivities()
        return {i: act for i, act in enumerate(acts)}

    # refatorado
    async def updateActivity(self, id: int, act: Activity):
        user_id = await self.get_user_id()
        result = await db.read_data("USERS", {"user_id": user_id})
        if result:
            activities = result[0].lista_favoritos or []
            if 0 <= id < len(activities):
                activities[id] = act.model_dump()
                await db.update_data("USERS", {"user_id": user_id}, {"lista_favoritos": activities})
                return activities
            else:
                raise Exception("Activity ID inválido")
            
    async def removeActivity(self, id: int):
        user_id = await self.get_user_id()
        result = await db.read_data("USERS", {"user_id": user_id})
        if result:
            activities = result[0].lista_favoritos or []
            if 0 <= id < len(activities):
                activities.pop(id)
                await db.update_data("USERS", {"user_id": user_id}, {"lista_favoritos": activities})
            else:
                raise Exception("ID inválido")

    # nao refatorado
    def addSchedule(self, sched: Schedule):
        self.schedules.append(sched)

    # nao refatorado
    def getSchedule(self, username:str):
        return self.schedules[-1] if len(self.schedules) else None

    @classmethod
    async def get_or_create(cls, nome):
        result = await db.read_data("USERS", {"nome": nome})
        if not result:
            await db.add_data("USERS", {
                "nome": nome,
                "senha": "default",  # ajuste conforme necessário
                "status": "ativo",
                "lista_favoritos": []
            })
        return cls(nome)