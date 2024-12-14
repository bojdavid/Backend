from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


#defining a schema for our users -- it is a pydantic model
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class config:
        orm_mode=True

    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#defining a schema for our post request -- it is a pydantic model
class PostBase(BaseModel):
    title: str
    content: str
    rating: int = None
    published: bool=True

class PostCreate(PostBase):
    pass

class Post(PostBase): #extends postbase class
    created_at: datetime
    id: int
    owner_id: int
    owner: UserOut

    class config:
        orm_mode=True

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    votes : int

    """class config:
        orm_mode=True"""


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str]

class Vote(BaseModel):
    post_id: int
    dir: int #direction should be 0 or 1 for upvote or downvote