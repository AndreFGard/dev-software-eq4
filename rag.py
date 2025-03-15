from search import Searcher, SearchItem
import asyncio
import os
from schemas import *

brave_key = os.getenv("BRAVE_KEY")
from crawl4ai import AsyncWebCrawler, CacheMode, BrowserConfig, CrawlerRunConfig, CacheMode, CrawlResult
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai import CrawlerRunConfig

prune_filter = PruningContentFilter(
    threshold=0.5,
    threshold_type="fixed",  # or "dynamic"
    min_word_threshold=5
)

crawler_config = CrawlerRunConfig(
    cache_mode=CacheMode.ENABLED,
    excluded_tags=['a'],
    markdown_generator=DefaultMarkdownGenerator(
        content_filter=prune_filter,
        options={
            "ignore_links":True,
            "ignore_images": True,
            "escape_html": False
        }
    )
)

async def crawl4ai_crawl_many(urls: list,crawler_config = crawler_config) -> list[CrawlResult]:
    

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun_many(
            urls=urls, config=crawler_config, 
        )

        return result   #type: ignore 


class SlidingWindowChunking:
    """
    A class used to perform sliding window chunking on text data.
    This class provides methods to split text into chunks of a specified window size
    with a given step size. It also summarizes with an LLM if possible and filters the markdown
    """

    def __init__(self, window_size=135, step=35):
        self.window_size = window_size
        self.step = step
    
    def chunk(self, text, window_size=0,step=0) -> list[str]:
        window_size = window_size or self.window_size
        step = step or self.step

        words = text.split(" ")
        chunks = []
        for i in range(0, len(words) - window_size + 1, step):
            chosen = words[i:i + window_size]
            if chosen:
                chunks.append(' '.join(chosen))
        if not chunks:
            chunks = [text]
        return chunks
    


class RAGOpenai(MasterOpenaiInterface):
    def __init__(self, cheap_models:list[LLMModelInfo], useDummy=False):
            super().__init__(cheap_models=cheap_models, useDummy=useDummy)

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
    

import vdb, os
class RAG:
    def __init__(self, cheap_models: list[LLMModelInfo], brave_api_key="", TEMBO_PSQL_URL=os.environ.get('TEMBO_PSQL_URL'), top_results=5, demo_search=False):
        """This class requires a list of cheap models"""

        self.sr = Searcher(brave_api_key, use_demo=demo_search)
        self.demo_search = demo_search
        self.chunker = SlidingWindowChunking()
        self.top_results=top_results
        self.db = vdb.VecDb(TEMBO_PSQL_URL=TEMBO_PSQL_URL) #type: ignore
        self.llm = RAGOpenai(cheap_models=cheap_models, useDummy=False)

    async def search_and_crawl(self, query=""):
        srItems = await self.sr.search(query)

        results = await crawl4ai_crawl_many(urls=[site.url for i,site in zip(range(self.top_results), srItems)])
        return results
    
    async def CrawlResult_to_DB_Site(self, site: CrawlResult, crawler_config=crawler_config) -> DB_Site:
        """
        Asynchronously processes a CrawlResult object to generate markdown content,
        summarize it if necessary, and split it into chunks.
        """
        oldmd = str(crawler_config.markdown_generator.generate_markdown(str(site.cleaned_html)).fit_markdown or site.markdown)
        md = oldmd
        if (len(oldmd) < self.llm.rate_limit) and self.llm.openai:
            md = await self.llm.summarize(oldmd)
            print('f{SUMMARIZING REDUCTION: {(100*len(oldmd)/len(md)):.1f}%')
        else:
            print("ERROR SUMMARIZING: TOO LONG")
        
        chunks = self.chunker.chunk(str(md))
        title = (site.metadata or {}).get('title') or site.url

        return DB_Site(url=site.url,
                        content=md,
                       title=title,
                       chunks = chunks
                       )


    async def add_chunks(self, sites: list[CrawlResult]) -> list[DB_Site]:
        """do topic segmentation/chunking"""
        results = [await self.CrawlResult_to_DB_Site(site) for site in sites]
        return results
    
    async def search_store(self, query):
        results = [site for site in await self.search_and_crawl(query) if site.success]
        results = await self.add_chunks(results) 
        return await self.db.insert_sites_n_chunks(results)
    
    async def retrieve_no_search(self, query) -> list[str]:
        return await self.db.retrieve_no_search(query)
    
    async def retrieve_with_search(self, query) -> list[str]:
        await self.search_store(query)
        return await self.db.retrieve_no_search(query)


    
async def demo():
    #rag = RAG(brave_api_key=brave_key, demo_search=True)
    #await rag.db.retrieve_no_search("what to do in rio")
    query = "Best Tourist attractions in Rio de Janeiro"
    # crawled_results = asyncio.run( rag.search_and_crawl(query))
    # segmented_results = rag.add_chunks(crawled_results)
    # for result in segmented_results:
    #     print("\n\n\tCHUNK BLOCK")
    #     #[print(f"\n\t\tCHUNK: ---{chunk}") for chunk in result.chunks]
    # return await (rag.store_search(query))
