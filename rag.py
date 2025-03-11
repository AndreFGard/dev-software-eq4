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
    min_word_threshold=50
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
    def __init__(self, window_size=70, step=35):
        self.window_size = window_size
        self.step = step

    def chunk(self, text):
        words = text.split()
        chunks = []
        for i in range(0, len(words) - self.window_size + 1, self.step):
            chunks.append(' '.join(words[i:i + self.window_size]))
        return chunks
    
    def _add_chunks(self, site: CrawlResult) -> list[DB_Site]:
        chunks = self.chunk(str(site.markdown))
        site.chunks = chunks

        return DB_Site(url=site.url,
                        content=site.markdown,
                       title=site.metadata.get('title'),
                       chunks = chunks
                       )

from concurrent.futures import ThreadPoolExecutor



import vdb, os
class RAG:
    def __init__(self, brave_api_key="", TEMBO_PSQL_URL=os.environ.get('TEMBO_PSQL_URL'), top_results=2, demo_search=True):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.sr = Searcher(brave_api_key, use_demo=demo_search)
        self.demo_search = demo_search
        self.chunker = SlidingWindowChunking()
        self.top_results=top_results
        self.db = vdb.VecDb(TEMBO_PSQL_URL=TEMBO_PSQL_URL)

    async def search_and_crawl(self, query=""):
        srItems = await self.sr.search(query)

        results = await crawl4ai_crawl_many(urls=[site.url for i,site in zip(range(self.top_results), srItems)])
        return results
    
    def add_chunks(self, sites: list[CrawlResult]) -> list[CrawlResultChunked]:
        """do topic segmentation/chunking in the content of many sites in parallel"""
        with ThreadPoolExecutor(max_workers=6) as executor:
            results = list(executor.map(self.chunker._add_chunks, sites))
        return results
    
    async def store_search(self, query):
        results = [site for site in await self.search_and_crawl(query) if site.success]
        results = self.add_chunks(results) 
      
        
        return await self.db.insert_sites_n_chunks(results)

    
def demo():
    rag = RAG(brave_api_key=brave_key, demo_search=True)
    query = "Tourist attractions in Recife"
    # crawled_results = asyncio.run( rag.search_and_crawl(query))
    # segmented_results = rag.add_chunks(crawled_results)
    # for result in segmented_results:
    #     print("\n\n\tCHUNK BLOCK")
    #     #[print(f"\n\t\tCHUNK: ---{chunk}") for chunk in result.chunks]
    asyncio.run(rag.store_search(query))
