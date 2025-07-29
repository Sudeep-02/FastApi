# model.py
from typing import Optional
from sqlmodel import Field,Relationship
from datetime import datetime
from .schemas import ForbidExtraBase
from pydantic import EmailStr,BaseModel
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

def now_ist():
    return datetime.now(IST)


class User(ForbidExtraBase,table=True):
    id : Optional[int] = Field(default=None, primary_key=True) 
    email : str = Field(unique=True)
    password : str
    created_at: datetime = Field(default_factory=now_ist) 

class UserCreate(ForbidExtraBase):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    email : EmailStr

class PostBase(ForbidExtraBase):
    title: str
    content: str
    published: bool = True
    
class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=now_ist)
    # Foreign key column
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id", ondelete="CASCADE")
    owner: Optional["User"] = Relationship() # type: ignore
    

class PostCreate(PostBase):
    pass

class PostUpdate(ForbidExtraBase):
    title : Optional[str] = None
    content : Optional[str] = None

class PostOut(BaseModel):
    id:int
    title: str
    content: str
    owner_id : int
    owner : UserOut
    published: bool
    created_at : datetime
    