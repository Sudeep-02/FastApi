from fastapi import APIRouter,Depends,HTTPException,status,Response
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_session
from sqlmodel import Session,select
from ..model import UserCreate,User
from ..utils import verify
from ..oauth2 import create_access_token
from ..schemas import Token
router = APIRouter(
    tags=['Authentication']
)

@router.post("/login",response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),session:Session=Depends(get_session)):
    #OAuth2PasswordRequestForm has two parts username and passowrd
    # normally it is def login(user_credentials: UserCreate,session:Session=Depends(get_session)):
    #UserCreate is my pydantic model with email and password
    statement = select(User).where(User.email == user_credentials.username)
    # So above it should be user_credentials.email with my pydantic model but it is .username for oAuth2requestform
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    if not verify(user_credentials.password,result.password): # use result not user why because result has data from db 
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    #Create a token
    access_token = create_access_token(data = {"user_id":result.id})
    #return token
    return {"access_token":access_token,"token_type" : "bearer"} # this should be same not different key and value
    #otherwise OAuth2PasswordBearer in oauth2.py will fail