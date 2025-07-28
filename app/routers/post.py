from typing import List
from fastapi import APIRouter,status,HTTPException, Depends

from app import oauth2
from ..model import PostCreate,PostUpdate,Post
from sqlmodel import select,Session
from  ..database import get_session
from ..oauth2 import get_current_user
router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


#get all posts
@router.get("/", response_model=List[Post])
def get_posts(session: Session = Depends(get_session)):
    # Make a SELECT query for all posts
    statement = select(Post)
    results = session.exec(statement) # here result is object not data and this can be used in next as medium to get all or single data
    posts = results.all()  # This returns a list of Post objects
    print(posts)
    return posts  # FastAPI/SQLModel automatically converts Post objects to dict for JSON

#Create a post
@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, session: Session = Depends(get_session),get_current_user:int = Depends(oauth2.get_current_user)):
    #get_current_user has user from database
    print(get_current_user)
    db_post = Post.from_orm(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

# get single post
@router.get("/{post_id}",response_model=Post)
def get_post(post_id:int,session : Session = Depends(get_session)):
    db_post = session.get(Post,post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return db_post
   
#delete post
@router.delete("/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int,session :Session = Depends(get_session),get_current_user:int = Depends(oauth2.get_current_user)):
    post = session.get(Post,post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    session.delete(post)
    session.commit()   
    return #line one will return message
 
 #update post
@router.put("/{post_id}",response_model=Post)
def update_post(post_id:int,post_update:PostUpdate,session:Session = Depends(get_session),get_current_user:int = Depends(oauth2.get_current_user)):
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