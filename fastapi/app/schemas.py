from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from . import modals
from pydantic import conint




class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True

class PostOut(BaseModel):
    post: Post
    votes: int

    class Config:
        from_attributes = True

class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)