from pydantic import BaseModel
import asyncio as aio
import random
from openai import AsyncOpenAI

import json
from schemas import *
from user import User

prompts = {
    UserStatus.DISCUSSING: 'You are a quiet travel planner helping a tourist. Don\'t answer questions unrelated to this. If necesssary, call tools to search info on the internet about a destination, but only use their result if it\'s relevant',
    UserStatus.SUMMARIZING_ACTIVITIES: """You are summarizing the chosen activities below for the tourist.
    Please summarize them as a list of activities, each with values for name, short_description, and long_description.""",
    UserStatus.MODIFYING_ACTIVITY: 'You are modifying an activity for the tourist.'
}

async def answerDummy(*args, **kwargs):
    buzzwords = ["voce nao esta usando o chatgpt, forneca uma OPENAI_KEY\n", "- **Design Science Research**:\n1. isso é uma lista\n2. ainda é uma lista", ""]
    await aio.sleep(2)
    return " ".join(random.sample(buzzwords, 3) )





from rag import RAGOpenai,RAG

class OpenaiInteface(MasterOpenaiInterface):
    """Essa classe proverÁ (quando isso for implementado) 
    as respostas de um chatbot.
    Essa classe deve preparar os parametros, prompts e outras coisas
    Parameters:
    useDummy (bool): usar um chatbot fake ou não;."""

    def __init__(self, main_model: LLMModelInfo, useDummy=True, cheap_models:list[LLMModelInfo]=[],brave_api_key="",TEMBO_PSQL_URL="", **kwargs):
        super().__init__(useDummy=useDummy, cheap_models=cheap_models, main_model=main_model)
        if not cheap_models: cheap_models = [main_model]
        self.RAG = RAG(cheap_models=cheap_models, brave_api_key=brave_api_key, TEMBO_PSQL_URL=TEMBO_PSQL_URL,demo_search=False)



    def getSystemMessage(self, user: User):
        return [GptMessage(role='system',content=prompts[user.status]).model_dump()]

    async def reply(self, user:User):
        if self.openai:
            return await self.completion_with_tool(user) or ""
        else: 
            return await answerDummy(user) or ""

    async def retrieve_info(self, query:str) -> list[str]:
        """Searches a query on the internet and on the knowledge database and returns the top most relevant texts"""
        return await self.RAG.retrieve_no_search(query)

    async def completion(self, user: User):
        #make the retrieved info placeholder tool available to gpt, detect if it was called (the gpt is already instructured
        # to only call it if needed) and then try again while providing the returned data
        choice = ""
        messages=self.getSystemMessage(user) + user.dumpHistory()

        [m.pop("id") for m in messages]
        completion = await self.openai.chat.completions.create( #type: ignore
            model=self.model,
            messages=messages #type: ignore
        )
        return completion.choices[0].message.content
    

    async def completion_with_tool(self, user: User):
        # Define the retrieve_info tool
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "retrieve_info",
                    "description": "Search for information about travel destinations on the internet",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The RAG query about the travel destination. Make sure it's a good query"
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]
        
        messages = self.getSystemMessage(user) + user.dumpHistory()
        [m.pop("id") for m in messages]
        
        # First call with tool definition
        completion = await self.openai.chat.completions.create( #type: ignore
            model=self.model,
            messages=messages, #type: ignore
            tools=tools, #type: ignore
            tool_choice="auto"
        )
        
        response = completion.choices[0].message
        
        # Check if the model wants to call the retrieve_info tool
        if response.tool_calls:
            # Get all tool calls
            tool_messages = [response]
            
            for tool_call in response.tool_calls:
                if tool_call.function.name == "retrieve_info":
                    # Extract query from the function arguments
                    function_args = json.loads(tool_call.function.arguments)
                    query = function_args.get("query")
                    
                    # Call retrieve_info with the query
                    info_results = await self.retrieve_info(query)
                    
                    # Add tool response to messages
                    tool_messages.append({
                        "tool_call_id": tool_call.id, #type: ignore
                        "role": "tool", #type: ignore
                        "name": "retrieve_info", #type: ignore
                        "content": str(info_results) #type: ignore
                    })
            
            # Second call with the tool results
            second_completion = await self.openai.chat.completions.create( #type: ignore
                model=self.model,
                messages=messages + tool_messages  #type: ignore
            )
            
            return second_completion.choices[0].message.content
        
        # If no tool was called, return the original response
        return response.content