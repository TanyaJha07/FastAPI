from fastapi import FastAPI,APIRouter, status,Response,status, HTTPException,Depends
from sqlalchemy.orm import Session
from typing import List
from ..import models,schemas,oauth2
from ..database import  get_db


router = APIRouter(
    prefix="/posts",
    tags= ['Posts']
)

@router.get('/')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")   ----------------------------------------------------by sql
    # post = cursor.fetchall() # fetchall to retrive multiple posts, # fetchone to retrive 1 post 
    posts = db.query(models.Post).all()
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db),
                 user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    # # %s = variable, place holders (order matters)
    # new_post = cursor.fetchone()
    # conn.commit()-----------------------------------------------------------------------------------by sql
    print(user_id)
    new_post =models.Post(**post.dict())
    print(new_post)
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print('gokul', new_post.__dict__)
    # new_post.created_at = datetime(new_post.created_at.strftime("%d-%m-%Y %H:%M:%S"))
    return new_post

@router.get('/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""Select * from posts where id = 1""", (str(id),))
    # post = cursor.fetchone()-----------------------------------------------by sql
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} was not found")
    return  post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute(""" delete from posts where id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()---------------------------------------------------------------------by sql
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""Update posts SET title = %s,content = %s, published = %s where id = %s returning *""",
    #                (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    # conn.commit()-----------------------------------------------------------------------------------------------by sql
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session= False)
    db.commit()
    return post_query.first()