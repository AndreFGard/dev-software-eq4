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
            return self.demo
        else: return await [SearchItem(**result) for result in self._search_brave(query)['web']['results']]
   
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






async def main():
    #results = await search_brave("what to do in olinda as a tourist")
    s = Searcher("")
    print(await s.search("eae"))

if __name__ == "__main__":
    asyncio.run(main())