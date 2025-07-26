# model.py

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

def now_ist():
    return datetime.now(IST)

class ForbidExtraBase(SQLModel):
    class Config:
        extra = "forbid"
    
class PostBase(ForbidExtraBase):
    title: str
    content: str
    published: bool = True
    
        
    
class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=now_ist)

class PostCreate(PostBase):
    pass

class PostUpdate(ForbidExtraBase):
    title : Optional[str] = None
    content : Optional[str] = None