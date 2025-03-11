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






class DB_Document(BaseModel):
    content: str
    site_id: int
    id: int = 0