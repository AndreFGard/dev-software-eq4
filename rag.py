from search import Searcher
import asyncio

from crawl4ai import AsyncWebCrawler, CacheMode, BrowserConfig, CrawlerRunConfig, CacheMode, CrawlResult

async def crawl4ai_crawl(url) -> CrawlResult:
    crawler_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url, config=crawler_config
        )
        return result

class RAG:
    def __init__(self, brave_api_key=""):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.sr = Searcher(brave_api_key)
    

            
r = RAG()
asyncio.run()
