from typing import Optional
from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None
   


my_posts = [
    {"title": "Title 1", "content": "Content 1", "id": 1},
    {"title": "Title 2", "content": "Content 2", "id": 2},
    {"title": "Title 3", "content": "Content 3", "id": 3},
]

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] ==id:
            return i


@app.get("/")
def root():
    return {"message": "Hello world !"}


@app.get("/posts")
def get_posts():
    return {"data" : my_posts}


# @app.post("/posts")
# # def create_posts(payLoad: dict = Body(...)):
# def create_posts(payLoad: Post):
#     print(payLoad)  # this payload is pydantic model not dict
#     print(payLoad.dict())  # now this is dictionary type
#     # return {"message": f"title {payLoad['title']} content:{payLoad['content']}"}
#     return {"message": "This is posts path"}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    # when i use post model it is automatically accepting values and validate against model from body like frontend or postman 
    # without having to specify user.body() like js or ts in react
    #see above commented function to understand.
    post_dict = post.model_dump()
    post_dict['id']= randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}


@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    result = next((item for item in my_posts if item['id'] == id),None)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return {"data": result}

@app.delete("/posts/{id}")
def delete_post(id:int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    my_posts.pop(index)
    return {"message":"Post was succesfully deleted"}