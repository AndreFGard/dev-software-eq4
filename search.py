import asyncio
import aiohttp

from  pydantic import BaseModel
search_url = "https://api.search.brave.com/res/v1/web/search"
brave_api_key = ""  # Add your Brave API key here

class SearchItem(BaseModel):
    title: str
    url: str
    is_source_local: bool
    is_source_both: bool
    description: str = None
    page_age: str = None
    page_fetched: str = None
    profile: dict = None
    language: str = None
    family_friendly: bool = False

def getDemoResults():
        import json
        f = open("demosearch.json", "r")
        d = json.load(f)
        f.close()
        return d

class Searcher:
    def __init__(self, api_key:str, use_demo=True):
        self.api_key =api_key
        self.demo = {}
        self.use_demo = use_demo
        
    
    async def search(self, query):
        if self.use_demo:
            if not self.demo: self.demo = getDemoResults()
            return [SearchItem(**result) for result in self.demo['web']['results']]
        else: return [SearchItem(**result) for result in await self._search_brave(query)['web']['results']]
   
    async def _search_brave(self, query: str, country="BR"):
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key
        }
        
        params = {
            "q": query,
            "country": country
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=headers, params=params) as response:
                return await response.json()

from rag_scraper.scraper import Scraper
from rag_scraper.converter import Converter

class RAG:
    def __init__(self, brave_api_key=""):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.sr = Searcher(brave_api_key)
    
    async def search_and_scrap(self, query: str):
        results = await self.sr.search(query)
        for r in results:
            html = Scraper.fetch_html(r.url, headers = self.headers)
            md = markdown_content = Converter.html_to_markdown(html=html, parser_features='html.parser',ignore_links=True)
            print(md)
            break
            
r = RAG()
asyncio.run(r.search_and_scrap(""))
