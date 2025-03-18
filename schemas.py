from pydantic import BaseModel
from enum import Enum
import time 
class GptMessage(BaseModel):
    role: str
    content: str
    id: int = 0

class Activity(BaseModel):
    name: str
    short_description: str
    long_description: str

class UserStatus(Enum):
    DISCUSSING = 'discussing'
    SUMMARIZING_ACTIVITIES = 'summarizing_activities'
    MODIFYING_ACTIVITY = 'modifying_activity'
    
class Message(BaseModel):
    username: str
    content: str
    is_activity: bool = False
    id: int = 0

from crawl4ai import CrawlResult
class CrawlResultChunked(CrawlResult):
    chunks: list[str]

class DB_Site(BaseModel):
    timestamp: int = int (time.time())
    url: str
    content: str
    title: str
    id: int = 0
    chunks: list[str] = []


from openai import AsyncOpenAI

class LLMModelInfo(BaseModel):
    url: str
    model: str
    rate_limit: int
    key:str

class MasterOpenaiInterface:
    def __init__(self, main_model: LLMModelInfo | None = None, cheap_models: list[ LLMModelInfo] = [], **kwargs):
        self.openai: AsyncOpenAI | None = None
        self.cheap_models=cheap_models

        if main_model:
            self.switch_to_model(main_model)
            self.main_model = main_model
        else:
            self.main_model = cheap_models[0]
            self.switch_to_model(cheap_models[0])


    def switch_to_model(self, model: LLMModelInfo):
        """Start using another LLM model from now on"""
        self.model = model.model
        self.rate_limit = model.rate_limit
        self.base_url = model.url 
        self.openai = AsyncOpenAI(
            base_url=model.url,
            api_key=model.key
        )        

class DB_Document(BaseModel):
    content: str
    site_id: int
    id: int = 0

class SearchItem(BaseModel):
    title: str
    url: str
    is_source_local: bool
    is_source_both: bool
    description: str = ""
    page_age: str = ""
    page_fetched: str = ""
    profile: dict = {}
    language: str = ""
    family_friendly: bool = False
