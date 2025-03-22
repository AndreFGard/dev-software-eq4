from .search import Searcher

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
    

    async with AsyncWebCrawler(config=BrowserConfig(verbose=False)) as crawler:
        result = await crawler.arun_many(
            urls=urls, config=crawler_config, 
        )

        return result   #type: ignore 






from .rag_openai import RAGOpenai
from .chunker import SlidingWindowChunking
import os
from .vdb import VecDb
class RAG:
    def __init__(self, cheap_models: list[LLMModelInfo], brave_api_key="", TEMBO_PSQL_URL=os.environ.get('TEMBO_PSQL_URL'), top_results=4, demo_search=False):
        """This class requires a list of cheap models"""

        self.sr = Searcher(brave_api_key, use_demo=demo_search)
        self.demo_search = demo_search
        self.chunker = SlidingWindowChunking()
        self.top_results=top_results
        self.db = VecDb(TEMBO_PSQL_URL=TEMBO_PSQL_URL) #type: ignore
        self.llm = RAGOpenai(cheap_models=cheap_models)

    async def search_and_crawl(self, query=""):
        start = time.time()
        srItems = await self.sr.search(query)
        print(f"SEARCH: {time.time()-start:.3f}")
        start = time.time()
        results = await crawl4ai_crawl_many(urls=[site.url for i,site in zip(range(self.top_results), srItems)])
        print(f"CRAWL: {time.time()-start:.3f}")
        return results
    
    async def CrawlResult_to_DB_Site(self, site: CrawlResult, crawler_config=crawler_config) -> DB_Site | None:
        """
        Asynchronously processes a CrawlResult object to generate markdown content,
        summarize it if necessary, and split it into chunks.
        """
        
        #apply pruning filter to get rid of useless content such as tags
        oldmd = str(crawler_config.markdown_generator.generate_markdown(str(site.cleaned_html)).fit_markdown or site.markdown)
        md = oldmd
        if isinstance(self.llm.rate_limit, int) and (len(oldmd) < self.llm.rate_limit) and self.llm.openai:
            md = await self.llm.summarize(oldmd)
            print(f'PRUNE + SUMMARIZING REDUCTION: {(100*len((oldmd))/len(site.markdown)):.1f}%-{(100*len(md)/len(oldmd)):.1f}%') #type: ignore
        else:
            print("ERROR SUMMARIZING: TOO LONG")
            return None
        
        chunks = [chnk for chnk in self.chunker.chunk(str(md)) if len(chnk) > 1]
        title = (site.metadata or {}).get('title') or site.url

        return DB_Site(url=site.url,
                        content=md,
                       title=title,
                       chunks = chunks
                       )


    async def add_chunks(self, sites: list[CrawlResult]) -> list[DB_Site]:
        """separate text in chunks"""
        start = time.time()
        results = await asyncio.gather(*[self.CrawlResult_to_DB_Site(site) for site in sites])
        print(f"CHUNKING and summarizing: {time.time()-start:.3f}")
        return [site for site in results if site]
    
    async def search_store(self, query):
        """Search on the web, crawl and store the results and their chunks in the database"""
        results = [site for site in await self.search_and_crawl(query) if site.success]
        results = [res for res in await self.add_chunks(results) if (res.chunks and res.url and res.title)]
        return await self.db.insert_sites_n_chunks(results)
    
    async def retrieve_no_search(self, query) -> list[str]:
        """search on the database without searching the web"""

        start = time.time()
        x = await self.db.retrieve_no_search(query)
        print(f"RETRIEVAL: {time.time()-start:.3f}")
        return x
    
    async def retrieve_with_search(self, query) -> list[str]:
        """search on the web and the database"""
        
        await self.search_store(query)
        return await self.db.retrieve_no_search(query)


    
