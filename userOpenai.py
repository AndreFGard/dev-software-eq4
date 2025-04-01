from pydantic import BaseModel
import asyncio as aio
import random
from openai import AsyncOpenAI

import json
from schemas import *


prompts = {
    UserStatus.DISCUSSING: 'You are a travel planner helping a tourist. Don\'t answer questions unrelated to this. If necesssary, call tools to search info on the internet about a destination, but only use their result if it\'s relevant. Upon calling the search and geting results, always present relevant info in a nicely formatted form.',
    UserStatus.SUMMARIZING_ACTIVITIES: """You are summarizing the chosen activities below for the tourist.
    Please summarize them as a list of activities, each with values for name, short_description, and long_description.""",
    UserStatus.MODIFYING_ACTIVITY: 'You are modifying an activity for the tourist.'
}

async def answerDummy(*args, **kwargs):
    buzzwords = ["voce nao esta usando o chatgpt, forneca uma OPENAI_KEY\n", "- **Design Science Research**:\n1. isso é uma lista\n2. ainda é uma lista", ""]
    await aio.sleep(2)
    return " ".join(random.sample(buzzwords, 3) )





from rag.rag import RAG
from rag.rag_openai import RAGOpenai
from schedule_maker import ScheduleMaker
class userOpenai(MasterOpenaiInterface):
    """Essa classe proverÁ (quando isso for implementado) 
    as respostas de um chatbot.
    Essa classe deve preparar os parametros, prompts e outras coisas
    Parameters:
    """

    def __init__(self, main_model: LLMModelInfo | None , cheap_models:list[LLMModelInfo]=[],brave_api_key="",TEMBO_PSQL_URL="", **kwargs):
        if not main_model: main_model= cheap_models[0]
        super().__init__(cheap_models=cheap_models, main_model=main_model)
        if not cheap_models: cheap_models = [main_model]
        self.RAG = RAG(cheap_models=cheap_models, brave_api_key=brave_api_key, TEMBO_PSQL_URL=TEMBO_PSQL_URL,demo_search=False)
        self.schedule_maker = ScheduleMaker(cheap_models=cheap_models)




    def getSystemMessage(self):
        return [GPTMessage(role='system',content=prompts[UserStatus.DISCUSSING]).model_dump()]

    async def reply(self, GPTMessageHistory: list[GPTMessage]) -> str:
        return await self.completion_with_tool(GPTMessageHistory) or "couldnt build openai object"

    async def retrieve_info(self, query: str, GPTMessageHistory: list[GPTMessage]) -> list[str]:
        """
        Searches for information using a two-step process:
        1. First checks the existing database for relevant information
        2. Only searches the internet if database results aren't sufficient
        """
        # First, try to get results from the database
        db_results = await self.RAG.retrieve_no_search(query)
        
        # If we don't have any results, immediately use web search
        
        # Otherwise, evaluate the relevance of the database results
        is_relevant = await self.evaluate_relevance(query, db_results, GPTMessageHistory=GPTMessageHistory)
        
        # If the results are not relevant, search the web
        if not is_relevant:
            print(f"RETRIEVAL: SEARCHIN '{query}'")
            return await self.RAG.retrieve_with_search(query)
        else:
            print("RETRIEVAL: DATABASE")
        # Return the database results if they're relevant
        return db_results

    async def evaluate_relevance(self, query: str, results: list[str], GPTMessageHistory: list[GPTMessage]) -> bool:
        if 'groq' not in self.base_url:
            print ("Structured output is likely to not work, as it's not a Groq hosted model")

            
        """Evaluates whether the retrieved results are relevant to the query"""
        # Create a prompt to evaluate relevance
        evaluation_prompt = f"""
        QUERY: {query}
        INFORMATION:
        {results}
        
        If the information is relevant and provides helpful details about the query, it is true that it's relevant enough
        If the information is insufficient, irrelevant, or too generic to answer the query, it's false that it's relevant enough".
        
        fill the json correctly, following the schema.
        """
        
        messages = [
            GPTMessage(role="system", content="""You are an evaluator determining the relevance of retrieved information, that responds in json.
            Determine if the provided information is relevant to a query enough. The JSON schema you will follow is this:
            {
            "query": "The query that was asked",
            "is_relevant_enough": true or false
            }
            """).model_dump(),
        ]

        messages += [gptm.model_dump() for gptm in GPTMessageHistory][:-4]
        messages.append(GPTMessage(role="user", content=evaluation_prompt).model_dump())
        
        for message in messages:
            if "id" in message:
                message.pop("id")

        for i in range(2):
            try:
                completion = await self.openai.chat.completions.create( # type: ignore
                    model=self.model,
                    messages=messages, # type: ignore
                    response_format= {'type': 'json_object'}
                )
                result = json.loads(completion.choices[0].message.content) # type: ignore
                if "is_relevant_enough" in result:
                    return result["is_relevant_enough"]
            except Exception as e:
                print(f"Error evaluating relevance: {e}")
                # In case of error, assume results are not relevant to be safe
            
        return False

    async def completion(self, GPTMessageHistory: list[GPTMessage]):
        #make the retrieved info placeholder tool available to gpt, detect if it was called (the gpt is already instructured
        # to only call it if needed) and then try again while providing the returned data
        choice = ""
        messages = self.getSystemMessage() + [gptm.model_dump() for gptm in GPTMessageHistory]

        [m.pop("id") for m in messages if 'id' in m]
        completion = await self.openai.chat.completions.create( #type: ignore
            model=self.model,
            messages=messages #type: ignore
        )
        return completion.choices[0].message.content
    

    async def completion_with_tool(self, GPTMessageHistory: list[GPTMessage]):
        # Define the retrieve_info tool
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "retrieve_info",
                    "description": "Search for information about travel destinations on google",
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
        
        messages = self.getSystemMessage() + [gptm.model_dump() for gptm in GPTMessageHistory]

        
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
            for i in range(2):
                # Get all tool calls
                tool_messages = [response]
                query, info_results = '', []
                for tool_call in response.tool_calls:
                    if tool_call.function.name == "retrieve_info":
                        # Extract query from the function arguments
                        function_args = json.loads(tool_call.function.arguments)
                        query = function_args.get("query")
                        
                        # Call retrieve_info with the query
                        info_results = await self.retrieve_info(query, GPTMessageHistory)
                        
                        # Add tool response to messages
                        tool_messages.append({
                            "tool_call_id": tool_call.id, #type: ignore
                            "role": "tool", 
                            "name": "retrieve_info", 
                            "content": str(info_results)
                        })

                if await self.evaluate_relevance(query,info_results, GPTMessageHistory):
                    second_completion = await self.openai.chat.completions.create( #type: ignore
                        model=self.model,
                        messages=messages + tool_messages  #type: ignore
                    )
                    return second_completion.choices[0].message.content
                print("RAG: TRYING AGAIN")

            #if everything went bonkers
            print("RAG: gave up")
            return await self.completion(GPTMessageHistory)
            
        
        # If no tool was called, return the original response
        return response.content

    async def make_schedule(self, GPTMessageHistory:list[GPTMessage], activities: list[Activity]):
        sched = await self.schedule_maker.create_cronogram(GPTMessageHistory, activities)
        return sched
    
    async def breakMessageIntoActivities(self, message: GPTMessage, message_history: list[GPTMessage]) -> list[Activity]:
        # Break the message into activities
        activities = await self.schedule_maker.activity_maker.build_activity_from_messages(message,message_history)
        return activities