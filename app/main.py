from typing import Optional
from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
   
   
while True:   
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi', user='postgres', password='9362',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error :", error)
        time.sleep(5)
    
@app.get("/")
def root():
    
    return {"message": "Hello world !"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data" : posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}


@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * from  posts where id = %s""",(str(id))) # id recieved is int from post model and sql query is str
    get_post = cursor.fetchone()
    print(get_post)
    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with id: {id} was not found")
    return {"data": get_post}

@app.delete("/posts/{id}")
def delete_post(id:int):
     cursor.execute("""DELETE FROM posts WHERE id = %s""", (id,))
     conn.commit()
     if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
     return {"message":"Post was successfully deleted"}
 
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
     cursor.execute("""UPDATE posts  SET title = %s, content = %s, published = %s   WHERE id = %s RETURNING *""", (post.title,post.content,post.published,id))
     updated_post = cursor.fetchone()
     conn.commit()
     if cursor.rowcount == 0:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
     return {"data": updated_post}
     