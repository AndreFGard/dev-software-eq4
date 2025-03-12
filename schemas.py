from pydantic import BaseModel
from enum import Enum

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
    user_id: int | None = None
