from schemas import *
from typing import List, Dict
from database import connection as conn
import json

class User():
    def __init__(self, username: str = "John Doe", password: str = "default_password", status: UserStatus = UserStatus.DISCUSSING, message_history: List[GptMessage] | list[Message] = []):
        if not message_history:
            message_history = [GptMessage(role='assistant', content="Hello! I'm a travel planner. Where would you like to travel today?")]

        self.username = username
        self.password = password
        self.status = status
        self.user_id = None
        self.favorite_messages = []
        self.message_history = message_history
        self._is_loaded = False

    async def save(self):
        """Salva o usuário no banco de dados."""

        user_data = {
            "nome": self.username,
            "senha": self.password,
            "status": self.status,
            "lista_favoritos": json.dumps(self.favorite_messages)
        }

        await conn.db.add_data("USERS", user_data)

    async def load(self):
        """Carrega o usuário do banco de dados."""

        if self._is_loaded:
            return

        user_conditions = {"nome": self.username}
        user = await conn.db.read_data("USERS", user_conditions)

        if user:
            self.user_id = user[0]._mapping["user_id"]
            self.status = user[0]._mapping["status"]
            self.favorite_messages = json.loads(user[0]._mapping["lista_favoritos"])
            self._is_loaded = True
        else:
            await self.save()
            await self.load()

    async def add_message(self, msg: Message):
        """Adiciona uma mensagem ao histórico do usuário."""

        if not self.user_id:
            await self.load()

        role = "user" if msg.username != "assistant" else "assistant"

        message_data = {
            "user_id": self.user_id,
            "content_message": json.dumps(msg.model_dump()),
            "role": role
        }

        await conn.db.add_data("MESSAGES", message_data)

    async def get_message_history(self) -> List[Message]:
        """Retorna o histórico de mensagens do usuário."""

        if not self.user_id:
            await self.load()

        conditions = {"user_id": self.user_id}
        messages = await conn.db.read_data("MESSAGES", conditions)

        return [Message(**json.loads(msg._mapping["content_message"])) for msg in messages] if messages else []

    async def dump_history(self):
        temp_messages = await self.get_message_history()

        return [m.model_dump() for m in temp_messages]
    
    async def add_to_favorites(self, msg: Message):
        """Adiciona uma mensagem à lista de favoritos do usuário."""

        if not self.user_id:
            await self.load()

        self.favorite_messages.append(msg.model_dump())

        await conn.db.update_data("USERS", {"user_id": self.user_id}, {"lista_favoritos": json.dumps(self.favorite_messages)})

    """
        Esta função abaixo possui a mesma funcionalidade de add_to_favorites?
    """
    
    # def add_activity(self, act: Activity,id=-1): 
    #     if id == -1 : 
    #         id = self._activity_id_counter
    #     else: self._activity_id_counter += 1
        
    #     self.favorite_messages[id] = act
        
    async def get_favorites(self):
        if not self.user_id:
            await self.load()

        return [Message(**msg) for msg in self.favorite_messages] if self.favorite_messages else []
    
    async def dump_activities(self):
        temp_activities = await self.get_favorites()

        return [act.model_dump() for act in temp_activities]
