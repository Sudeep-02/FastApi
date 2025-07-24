from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Hello world !"}


@app.get("/posts")
def get_posts():
    return {"message": "This is posts path"}


@app.post("/posts")
# def create_posts(payLoad: dict = Body(...)):
def create_posts(payLoad: Post):
    print(payLoad)  # this payload is pydantic model not dict
    print(payLoad.dict())  # now this is dictionary type
    # return {"message": f"title {payLoad['title']} content:{payLoad['content']}"}
    return {"message": "This is posts path"}
