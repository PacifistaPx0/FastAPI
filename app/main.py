import time
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
import psycopg
import psycopg2
from pydantic import BaseModel
from random import randrange 
from psycopg.rows import dict_row
from . import models, schemas 
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



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


#layout for working with raw sql within our python file
#fetching posts from data base
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("rollback") #fixes the DatabaseError: current transaction is aborted, commands ignored until end of transaction block
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"posts not found")
    
    return{"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    #                RETURNING * """,(post.title, post.content, post.published))
    #new_post = cursor.fetchone() #return the post we just created

    #conn.commit() #to insert data into database. saved changed arent commited yet
    

    #this unpacks our entire baase model insead of typing what user needs to input 
    #as in title = post.title
    new_post = models.Post(**post.dict()) 
    db.add(new_post) #add and commit to database
    db.commit()
    db.refresh(new_post) #this is equivalent to the returning * in sql 
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    
    #cursor.execute("""SELECT * from posts WHERE id = %(idnumber)s""", {"idnumber": str(id)})
    #post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()#Using .all() here is a waste of time as itll keep searching through the data

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} not found")
    
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    #cursor.execute("""DELETE from posts WHERE id= %(idnumber)s returning *""", {"idnumber": str(id)})
    #deleted_post = cursor.fetchone()
    #conn.commit()

    post = db.query(models.Post).filter(models.Post.id ==id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="id not found")
    
    post.delete(synchronize_session=False)
    db.commit()


@app.put("/posts/{id}")
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
    #            (post.title, post.content, post.published, str(id)))

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="id not found")

    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()

    return {"data": post_query.first()}