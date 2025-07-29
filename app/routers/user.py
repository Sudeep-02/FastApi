from fastapi import APIRouter,status,HTTPException, Depends
from typing import Optional,List
from ..model import UserCreate,UserOut,User
from sqlmodel import select,Session
from ..database import get_session
from ..utils import password_hash
router = APIRouter(
    prefix="/users",
    tags=['users']
)

#Create user 
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(user:UserCreate,session : Session = Depends(get_session)):
    
    statement = select(User).where(User.email == user.email)
    result = session.exec(statement).first()
    if result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
        
    #hash the password - user.password
    hashed_password = password_hash(user.password)
    user.password = hashed_password
    
    db_post = User.from_orm(user)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@router.get("/{user_id}",response_model=UserOut)
def get_user(user_id:int,session :Session = Depends(get_session)):
    query = session.get(User,user_id)
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return query