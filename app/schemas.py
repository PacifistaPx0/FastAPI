from pydantic import BaseModel
from datetime import datetime


#Working with classes 
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

#Inhenrits from post base
class PostCreate(PostBase):
    pass





#section handles us sending data to the user
#the fields within the classes is the data we will receive 
#We extend Postbase so we can inherit the defined fields within that class
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        orm_mode = True