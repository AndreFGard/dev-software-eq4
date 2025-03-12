from pydantic import BaseModel
import asyncio as aio
import random
from openai import AsyncOpenAI


from schemas import *
from user import User

prompts = {
    UserStatus.DISCUSSING: 'You are a quiet travel planner helping a tourist. Don\'t answer questions unrelated to this. If necesssary, call tools to search info on the internet about a destination',
    UserStatus.SUMMARIZING_ACTIVITIES: """You are summarizing the chosen activities below for the tourist.
    Please summarize them as a list of activities, each with values for name, short_description, and long_description.""",
    UserStatus.MODIFYING_ACTIVITY: 'You are modifying an activity for the tourist.'
}

async def answerDummy(*args, **kwargs):
    buzzwords = ["voce nao esta usando o chatgpt, forneca uma OPENAI_KEY\n", "- **Design Science Research**:\n1. isso é uma lista\n2. ainda é uma lista", ""]
    await aio.sleep(2)
    return " ".join(random.sample(buzzwords, 3) )


class MasterOpenaiInterface:
    def __init__(self, useDummy=True, openai_key="", **kwargs):
        self.openai = None
        self.__openai_key__ = openai_key
        useDummy = useDummy or not openai_key
        if (useDummy):
            #nao usar o chatgpt de verdade
            self.openai = None
        else:
            self.openai = AsyncOpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=self.__openai_key__
            )

        self.model='llama3-8b-8192'
        
class RAGOpenai(MasterOpenaiInterface):
    def __init__(self, openai_key="", useDummy=False):
            super().__init__(openai_key=openai_key, useDummy=useDummy)

            self.summarize_prompt = """You are a summarization assistant. When summarizing a text,
              provide only a concise, clear summary without any greetings, preamble, or extra commentary. 
              Do not include phrases like \"Sure!\" or
              \"Here is the summary.\" Simply output the summary in a direct and succinct manner.""".replace("\n", " ")
            
    async def summarize(self, text):
        messages=[
            GptMessage(role="system", 
                content=self.summarize_prompt).model_dump(),

            GptMessage(role="user",
                content=text).model_dump()
        ]

        [m.pop("id") for m in messages]
        
        completion = await self.openai.chat.completions.create(
            model=self.model,
            messages=messages
        )
    
        return completion.choices[0].message.content



class OpenaiInteface(MasterOpenaiInterface):
    """Essa classe proverÁ (quando isso for implementado) 
    as respostas de um chatbot.
    Essa classe deve preparar os parametros, prompts e outras coisas
    Parameters:
    useDummy (bool): usar um chatbot fake ou não;."""

    def __init__(self, useDummy=True, openai_key="", **kwargs):
        super().__init__(useDummy=useDummy, openai_key=openai_key)
    
    def getSystemMessage(self, user: User):
        return [GptMessage(role='system',content=prompts[user.status]).model_dump()]

    async def reply(self, user:User):
        if self.openai:
            return await self.completion(user)
        else: 
            return await answerDummy(user)

    async def completion(self, user: User):
        choice = ""
        messages=self.getSystemMessage(user) + user.dumpHistory()

        [m.pop("id") for m in messages]
        completion = await self.openai.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion.choices[0].message.content
    

