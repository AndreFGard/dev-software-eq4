from schemas import *
from .chunker import SlidingWindowChunking
class RAGOpenai(MasterOpenaiInterface):
    def __init__(self, cheap_models:list[LLMModelInfo]):
            super().__init__(cheap_models=cheap_models)
            print(f"RAG: using {self.model}")
            self.summarize_prompt = """You are a summarization assistant. When summarizing a text,
              provide only a concise, clear summary without any greetings, preamble, or extra commentary. 
              Do not include phrases like \"Sure!\" or
              \"Here is the summary.\" Simply output the summary in a direct and succinct manner.""".replace("\n", " ")
            self.chunker = SlidingWindowChunking(window_size=self.rate_limit//2, step=90)

    async def __summarize_req(self, piece:str):
        messages=[
            GptMessage(role="system", 
                content=self.summarize_prompt).model_dump(),

            GptMessage(role="user",
                content=piece).model_dump()
        ]

        [m.pop("id") for m in messages]
        
        completion = await self.openai.chat.completions.create( #type: ignore
            model=self.model,
            messages=messages #type: ignore
        ) 

        return completion.choices[0].message.content

    async def summarize(self, text: str, manage_limits=False)-> str:
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