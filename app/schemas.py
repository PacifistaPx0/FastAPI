from pydantic import BaseModel


#Working with classes 
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

#Inhenrits from post base
class PostCreate(PostBase):
    pass

