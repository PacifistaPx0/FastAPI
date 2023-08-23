import time
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
import psycopg
from pydantic import BaseModel
from random import randrange 
from psycopg.rows import dict_row

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

while True:
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', 
                            password='thinkthank2016', row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection was succesful")
        break
    except Exception as error:
        print("conneting to database failed")
        print("Error: ", error)
        time.sleep(2)


my_posts = [{"title": "My first post", "content": "Glad to be on here", "id": 1},
            {"title": "Games", "content": "Video games are great", "id": 2}]

def findpost(id):
    for p in my_posts:
        if p['id']== id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id']==id:
            return i
@app.get("/")
async def root():
    return {"message": "Hello, My World Stand"}

@app.get("/posts")
def get_posts():
    cursor.execute("rollback") #fixes the DatabaseError: current transaction is aborted, commands ignored until end of transaction block
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return{"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post = findpost(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="id not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="id not found")
    post_dict = post.dict()
    post_dict['id'] = id #we assign it the id of the post
    my_posts[index] = post_dict
    return {"data": post_dict}