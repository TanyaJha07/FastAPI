from fastapi import FastAPI,Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel #pydantic = data validation
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(database="fastapi", user="postgres", password="anantmadhav", host="localhost", cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesful!")
        break 
    except Exception as error:
        print("Connection to database failed")  
        print('error',error)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "pizza, burger, fries", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
        
@app.get('/') # "@' = decorator. it is used to add a new route to the API.(get = http method & '/' = path(route))
async def root(): #async is used to make the function asynchronous(non-blocking)
    return {'message': 'WELCOME TO THE FIRST API'}


@app.get('/sqlalchemy')
def test_posts (db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    print(posts)
    return {"data" : posts}

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")   ----------------------------------------------------by sql
    # post = cursor.fetchall() # fetchall to retrive multiple posts, # fetchone to retrive 1 post 
    posts = db.query(models.Post).all()
    return {"data":posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post,db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    # # %s = variable, place holders (order matters)
    # new_post = cursor.fetchone()
    # conn.commit()-----------------------------------------------------------------------------------by sql
    new_post =models.Post(**post.dict())
    print(new_post)
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""Select * from posts where id = 1""", (str(id),))
    # post = cursor.fetchone()-----------------------------------------------by sql
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} was not found")
    return {"post_details": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(""" delete from posts where id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    print("f'deleted post, {delete_post}")
   
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""Update posts SET title = %s,content = %s, published = %s where id = %s returning *""",
                   (post.title, post.content, post.published, str(id)))
    
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    return {"data": updated_post}