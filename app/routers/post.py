from typing import List,Optional
from fastapi import APIRouter,status,HTTPException, Depends

from app import oauth2
from ..model import PostCreate,PostUpdate,Post,PostOut
from sqlmodel import select,Session,or_
from  ..database import get_session
from ..oauth2 import get_current_user
router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


#get all posts
@router.get("/", response_model=List[PostOut])
def get_posts(session: Session = Depends(get_session),limit :int = 10,search: Optional[str] = ""):
    # Make a SELECT query for all posts
    statement = select(Post)
    
     # Correct way - use column.contains(search_term)
    if search:
        statement = statement.where(
            or_(
                Post.title.contains(search),    # Column.contains(search_term) # type: ignore
                Post.content.contains(search)   # Column.contains(search_term) # type: ignore
            )
        )
    # Apply ordering and limit using SQLModel methods
    statement = statement.order_by(Post.id.desc()).limit(limit) # type: ignore
    
    # Execute with SQLModel session
    posts = session.exec(statement).all()
    return posts
    
    
    
    statement = statement.order_by(Post.id.desc()).limit(limit)
    
    results = session.exec(statement) # here result is object not data and this can be used in next as medium to get all or single data
    posts = results.all()  # This returns a list of Post objects
    print(limit)
    return posts  # FastAPI/SQLModel automatically converts Post objects to dict for JSON

#Create a post
@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, session: Session = Depends(get_session),get_current_user:dict = Depends(oauth2.get_current_user)):
    #get_current_user has user from database
    # print("this is ",get_current_user)
    # db_post = Post.from_orm(post)
    db_post = Post(
        title=post.title,
        content=post.content,
        published=getattr(post, 'published', True),  # If PostCreate has this field
        owner_id=get_current_user.id  # Set owner_id from current user # type: ignore
    )
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    print("This from create post",db_post)
    return db_post

# get single post
@router.get("/{post_id}",response_model=PostOut)
def get_post(post_id:int,session : Session = Depends(get_session)):
    db_post = session.get(Post,post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return db_post
   
#delete post
@router.delete("/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int,session :Session = Depends(get_session),get_current_user:dict = Depends(oauth2.get_current_user)):
    post = session.get(Post,post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.owner_id != get_current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    
    session.delete(post)
    session.commit()   
    return #line one will return message
 
 #update post
@router.put("/{post_id}",response_model=PostOut)
def update_post(post_id:int,post_update:PostUpdate,session:Session = Depends(get_session),get_current_user:dict = Depends(oauth2.get_current_user)):
    db_post = session.get(Post,post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if db_post.owner_id != get_current_user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    
    #update only fields that are passed in
    post_data = post_update.model_dump(exclude_unset=True)
    
    
    for key, value in post_data.items():
        setattr(db_post, key, value)
        
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post