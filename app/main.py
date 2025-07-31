from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine
from .routers import user,post,auth,vote



app = FastAPI()
   
def create_db_and_tables():
  SQLModel.metadata.create_all(engine) 

create_db_and_tables()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello world !"}




