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

async def crawl4ai_crawl_many(urls: list) -> list[CrawlResult]:
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

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun_many(
            urls=urls, config=crawler_config, 
        )
        return result    


import nltk
try:
    from nltk.tokenize import TextTilingTokenizer
except:
    nltk.download('stopwords')

from nltk.tokenize import TextTilingTokenizer

class SlidingWindowChunking:
    def __init__(self, window_size=70, step=35, openai_key=os.environ.get('OPENAI_KEY') or 'INVALID'):
        self.window_size = window_size
        self.step = step
        self.llm = RAGOpenai(openai_key=openai_key, useDummy=False)

    #
    def chunk(self, text):
        words = text.split()
        chunks = []
        for i in range(0, len(words) - self.window_size + 1, self.step):
            chosen = words[i:i + self.window_size]
            if chosen:
                chunks.append(' '.join(chosen))

        return chunks
    
    #todo move the summarizer out of here
    async def _add_chunks(self, site: CrawlResult) -> list[DB_Site]:
        md = site.markdown.fit_markdown or site.markdown or " "
        if len(md) < self.llm.rate_limit:
            md = await self.llm.summarize(md)
        
        chunks = self.chunk(str(md))

        return DB_Site(url=site.url,
                        content=md,
                       title=site.metadata.get('title') or site.url,
                       chunks = chunks
                       )

from concurrent.futures import ThreadPoolExecutor

class RAGOpenai(MasterOpenaiInterface):
    def __init__(self, openai_key="", useDummy=False):
            super().__init__(openai_key=openai_key, useDummy=useDummy)

            self.summarize_prompt = """You are a summarization assistant. When summarizing a text,
              provide only a concise, clear summary without any greetings, preamble, or extra commentary. 
              Do not include phrases like \"Sure!\" or
              \"Here is the summary.\" Simply output the summary in a direct and succinct manner.""".replace("\n", " ")
            self.model = "gemma2-9b-it"

    async def summarize(self, text, manage_limits=True):
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
  

import vdb, os
class RAG:
    def __init__(self, brave_api_key="", TEMBO_PSQL_URL=os.environ.get('TEMBO_PSQL_URL'), top_results=10,  openai_key='', demo_search=False):
        self.sr = Searcher(brave_api_key, use_demo=demo_search)
        self.demo_search = demo_search
        self.chunker = SlidingWindowChunking(openai_key=openai_key)
        self.top_results=top_results
        self.db = vdb.VecDb(TEMBO_PSQL_URL=TEMBO_PSQL_URL)

    async def search_and_crawl(self, query=""):
        srItems = await self.sr.search(query)

        results = await crawl4ai_crawl_many(urls=[site.url for i,site in zip(range(self.top_results), srItems)])
        return results
    
    async def add_chunks(self, sites: list[CrawlResult]) -> list[CrawlResultChunked]:
        """do topic segmentation/chunking in the content of many sites in parallel"""
        results = [await self.chunker._add_chunks(site) for site in sites]
        return results
    
    async def search_store(self, query):
        """currently unused because we couldnt find a performant way to both search, store and retrieve"""
        results = [site for site in await self.search_and_crawl(query) if site.success]
        results = await self.add_chunks(results) 
      
        
        return await self.db.insert_sites_n_chunks(results)
    
    async def retrieve_no_search(self, query):
        return await self.db.retrieve_no_search(query)
    
    async def retrieve_with_search(self, query):
        await self.search_store(query)
        return await self.db.retrieve_no_search(query)


    
async def demo():
    rag = RAG(brave_api_key=brave_key, demo_search=True)
    await rag.db.retrieve_no_search("what to do in rio")
    query = "Best Tourist attractions in Rio de Janeiro"
    # crawled_results = asyncio.run( rag.search_and_crawl(query))
    # segmented_results = rag.add_chunks(crawled_results)
    # for result in segmented_results:
    #     print("\n\n\tCHUNK BLOCK")
    #     #[print(f"\n\t\tCHUNK: ---{chunk}") for chunk in result.chunks]
    return await (rag.store_search(query))
