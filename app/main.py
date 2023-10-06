from typing import Optional,List
from fastapi import FastAPI,Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel #pydantic = data validation
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models,schemas,utils
from .database import engine,get_db
from .routers import post,user,auth

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/') # "@' = decorator. it is used to add a new route to the API.(get = http method & '/' = path(route))
async def root(): #async is used to make the function asynchronous(non-blocking)
    return {'message': 'WELCOME TO THE FIRST API'}

