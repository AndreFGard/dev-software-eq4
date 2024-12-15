from pydantic import BaseModel
from typing import List
from openai import OpenAI, AsyncOpenAI
import random
import time
import asyncio as aio

class Message(BaseModel):
    username: str
    content: str

class GptMessage(BaseModel):
    role: str
    content: str

#todo: implementar a logica de achar uma cidade mais apropriadamente
class City:
    name:str

async def answerDummy(*args, **kwargs):
    buzzwords = [ "Dev Software", "Concepcao de artefatos", "????", "Forms", "Eigenvalues "
    "synergy", "pivot", ",", "mas também", "blockchain", ", além de ", "cloud-native", ".",
    "big data",]
    await aio.sleep(2)
    return " ".join(random.sample(buzzwords, 3) )

user_list = {}


class User():
    username: str
    message_history: List[GptMessage]
    def __init__(self, username="John Doe", message_history=[]):
        self.username = username
        self.message_history = message_history
    def addMessage(self, msg: Message):
        role = "assistant"
        if msg.username != "assistant":
            role = "user"
        self.message_history.append(GptMessage(role=role, content = msg.content))
    
    def getMessageHistory(self) -> List[Message]:
        return [Message(username= self.username if item.role == "user" else "assistant", content=item.content) for item in self.message_history]
    
    def dumpHistory(self):
        return[m.model_dump() for m in self.message_history]

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
                base_url="https://openrouter.ai/api/v1",
                api_key=self.__openai_key__
            )

        self.model='microsoft/phi-3-medium-128k-instruct:free'
        self.__standard_prompt__ =[GptMessage(role='system',content='You are a quiet tralve planner.').model_dump()]
    
    async def reply(self, user:User):
        if self.openai:
            return await self.completion(user)
        else: 
            return await answerDummy(user)

    async def completion(self, user: User):
        choice = ""
        messages=self.__standard_prompt__ + user.dumpHistory()
        completion = await self.openai.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion.choices[0].message.content


        



#exemplo#
rob = User(username="Robinson", message_history=[])
rob.addMessage(Message(username="robinser", content="eae"))
#print(rob.message_history)
