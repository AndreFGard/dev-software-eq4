from pydantic import BaseModel
from enum import Enum
import time 
class GPTMessage(BaseModel):
    """
    A message compatible with openai's message type.
    """
    role: str
    content: str

class DBMessage(GPTMessage):
    """The internal representation of Messages. It includes an id field"""
    role: str
    content: str
    id: int = 0


class Message(BaseModel):
    """The chat representation of a message. Contains an id field
     and a username field, not to be mixed up with the role field"""
    username: str
    content: str
    id: int | None = None

class Activity(BaseModel):
    name: str
    short_description: str
    long_description: str
    id: int | None = None

class UserStatus(Enum):
    DISCUSSING = 'discussing'
    SUMMARIZING_ACTIVITIES = 'summarizing_activities'
    MODIFYING_ACTIVITY = 'modifying_activity'
    


def message_to_gpt_message(message: Message) -> GPTMessage:
    """
    Converts a Message object to a GPTMessage object.
    """
    return GPTMessage(role= "assistant" if message.username == "assistant" else "user", content=message.content)

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
    name: str
    time: str
    duration: str
    end_time: str
    description: str
    explanations: str | None = None

class DayDetail(BaseModel):
    day: int
    activities: list[ActivityDetail]

class Schedule(BaseModel):
    title: str
    days: list[DayDetail]
    explanations: str 