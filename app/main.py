import time
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
import psycopg
import psycopg2
from pydantic import BaseModel
from random import randrange 
from psycopg.rows import dict_row
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

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

#For testing session dependency
#layout for working with an ORM 
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return {"data": posts}


#layout for working with raw sql within our python file
#fetching posts from data base
@app.get("/posts")
def get_posts():
    cursor.execute("rollback") #fixes the DatabaseError: current transaction is aborted, commands ignored until end of transaction block
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"posts not found")
    
    return{"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
                    RETURNING * """,(post.title, post.content, post.published))
    new_post = cursor.fetchone() #return the post we just created

    conn.commit() #to insert data into database. saved changed arent commited yet
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    
    cursor.execute("""SELECT * from posts WHERE id = %(idnumber)s""", {"idnumber": str(id)})
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} not found")
    
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE from posts WHERE id= %(idnumber)s returning *""", {"idnumber": str(id)})
    deleted_post = cursor.fetchone()
    conn.commit()

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="id not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
                (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="id not found")

    return {"data": updated_post}