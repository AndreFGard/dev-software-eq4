from search import Searcher
import asyncio


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
