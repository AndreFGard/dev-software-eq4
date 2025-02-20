from pydantic import BaseModel
import asyncio as aio
import random
from openai import AsyncOpenAI


from schemas import *
from user import User

prompts = {
    UserStatus.DISCUSSING: 'You are a quiet travel planner helping a tourist. Don\'t answer questions unrelated to this.',
    UserStatus.SUMMARIZING_ACTIVITIES: """You are summarizing the chosen activities below for the tourist.
    Please summarize them as a list of activities, each with values for name, short_description, and long_description.""",
    UserStatus.MODIFYING_ACTIVITY: 'You are modifying an activity for the tourist.'
}

async def answerDummy(*args, **kwargs):
    buzzwords = ["voce nao esta usando o chatgpt, forneca uma OPENAI_KEY\n", "- **Design Science Research**:\n1. isso é uma lista\n2. ainda é uma lista", ""]
    await aio.sleep(2)
    return " ".join(random.sample(buzzwords, 3) )



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
                base_url="https://api.groq.com/openai/v1",
                api_key=self.__openai_key__
            )

        self.model='llama3-8b-8192'
    
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
        completion = await self.openai.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion.choices[0].message.content

