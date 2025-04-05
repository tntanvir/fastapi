from pydantic import BaseModel
from typing import List, Optional

class Blog(BaseModel):
    title:str
    body:str
class User(BaseModel):
    name:str
    email:str
    password:str
class Login(BaseModel):
    email:str
    password:str

    
class ShowUser(BaseModel):
    id:int
    name:str
    email:str
    
    class Config():
        orm_mode= True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None