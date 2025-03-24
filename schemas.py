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
    id: int | None = None

class UserStatus(Enum):
    DISCUSSING = 'discussing'
    SUMMARIZING_ACTIVITIES = 'summarizing_activities'
    MODIFYING_ACTIVITY = 'modifying_activity'
    
class Message(BaseModel):
    username: str
    content: str
    id: int | None = None

def activity_to_message(activity: Activity) -> Message:
    return Message(username="assistant", content=f"Activity: {activity.name}\n{activity.short_description}\n{activity.long_description}", id=activity.id)

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




class ActivityDetail(BaseModel):
    time: str
    name: str
    duration: str
    description: str
    explanations: str | None = None

class DayDetail(BaseModel):
    day: int
    activities: list[ActivityDetail]

class Schedule(BaseModel):
    title: str
    days: list[DayDetail]
    notes: str | None = None