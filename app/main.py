from typing import Optional,List
from fastapi import FastAPI, Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlmodel import SQLModel, select,Session
from .database import engine, get_session
from .model import Post,PostCreate,PostUpdate

app = FastAPI()
   
def create_db_and_tables():
  SQLModel.metadata.create_all(engine) 

create_db_and_tables()
    
@app.get("/")
def root():
    return {"message": "Hello world !"}

#get all posts
@app.get("/posts", response_model=List[Post])
def get_posts(session: Session = Depends(get_session)):
    # Make a SELECT query for all posts
    statement = select(Post)
    results = session.exec(statement) # here result is object not data and this can be used in next as medium to get all or single data
    posts = results.all()  # This returns a list of Post objects
    print(posts)
    return posts  # FastAPI/SQLModel automatically converts Post objects to dict for JSON

#Create a post
@app.post("/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, session: Session = Depends(get_session)):
    db_post = Post.from_orm(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

# get single post
@app.get("/posts/{post_id}",response_model=Post)
def get_post(post_id:int,session : Session = Depends(get_session)):
    db_post = session.get(Post,post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return db_post
   
#delete post
@app.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int,session :Session = Depends(get_session)):
    post = session.get(Post,post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    session.delete(post)
    session.commit()   
    return #line one will return message
 
 #update post
@app.put("/posts/{post_id}",response_model=Post)
def update_post(post_id:int,post_update:PostUpdate,session:Session = Depends(get_session)):
    db_post = session.get(Post,post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    #update only fields that are passed in
    post_data = post_update.dict(exclude_unset=True)
    for key, value in post_data.items():
        setattr(db_post, key, value)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

