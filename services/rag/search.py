import asyncio
import aiohttp
from schemas import SearchItem
from  pydantic import BaseModel
brave_api_key = ""  # Add your Brave API key here
search_url = "https://api.search.brave.com/res/v1/web/search"

def _update_demo(fname="searchdemo.json"):
    f = open(fname,"w")
    import os
    x = asyncio.run(Searcher(os.getenv('BRAVE_KEY') or "", use_demo=False)._search_brave("what to do in olinda pernambuco brazil"))
    import json
    json.dump(x, f)
    f.close()


def getDemoResults():
        import json
        f = open("searchdemo.json", "r")
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
        else:
            results = await self._search_brave(query)
            return [SearchItem(**result) for result in results['web']['results']]
   
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
        search_url = "https://api.search.brave.com/res/v1/web/search"

        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=headers, params=params) as response:
                return await response.json()

