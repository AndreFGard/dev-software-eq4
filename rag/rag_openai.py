from schemas import *
from .chunker import SlidingWindowChunking
global summarize_prompt
summarize_prompt = """You are an expert travel assistant helping users plan their trips by extracting useful information from online sources. You receive a website-based document containing relevant travel-related details about a specific location. Your goal is to generate a concise and informative summary that highlights the most relevant attractions, activities, cultural insights, and practical travel tips.

Instructions:

    Identify Key Information: Extract details about popular tourist spots, historical landmarks, local cuisine, transportation tips, and unique experiences mentioned in the content.

    Prioritize Relevance: Focus on the most significant details for a traveler, omitting overly generic or redundant information.

    Summarize Clearly: Use natural, well-structured sentences that are easy to understand. The summary should be engaging yet concise."""
class RAGOpenai(MasterOpenaiInterface):
    """Provides LLM utilities for RAG purposes"""
    def __init__(self, cheap_models:list[LLMModelInfo], prompt:str = ''):
            super().__init__(cheap_models=cheap_models)
            print(f"RAG: using {self.model}")
            sumarize_prompt = summarize_prompt
            self.summarize_prompt =  prompt or summarize_prompt
            self.chunker = SlidingWindowChunking(window_size=self.rate_limit//2, step=90)

    async def __summarize_req(self, piece:str) -> str:
        """Summarize piece of text, using a cheap/HIGH LIMIT model such as gemini"""
        messages=[
            GPTMessage(role="system", 
                content=self.summarize_prompt).model_dump(),

            GPTMessage(role="user",
                content=piece).model_dump()
        ]


        
        completion = await self.openai.chat.completions.create( #type: ignore
            model=self.model,
            messages=messages #type: ignore
        ) 

        return completion.choices[0].message.content or ""

    async def summarize(self, text: str, manage_limits=False)-> str:
        """chunkarize and summarize text"""
        pieces : list[str] = [text]
        n_reqs = 1
        if manage_limits:
            ...
        else:
            pieces = [text] 
        
        results = []
        for piece in pieces:
            try:
                results.append(await self.__summarize_req(piece))
            except Exception as e:
                print("ERROR SUMMARIZING: " + str(e))
        return '\n'.join(results)