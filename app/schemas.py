from pydantic import BaseModel
from sqlmodel import SQLModel
from pydantic import EmailStr, BaseModel
from typing import Optional


class ForbidExtraBase(SQLModel):
    class Config:
        extra = "forbid"    
        
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int] = None
    
