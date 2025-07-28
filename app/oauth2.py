from datetime import datetime, timedelta, timezone  # for token expiration
import jwt                                         # for encoding/decoding JWT
from fastapi import HTTPException, status,Depends
from fastapi.security import OAuth2PasswordBearer
from .schemas import TokenData          # for API error handling
from .database import get_session
from sqlmodel import Session,select
from . import model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#this searching for access_token generated for first time when logged in 
#so it  is "login" endpoint same as login page or acess_token creation function 


SECRET_KEY = "2|[e%VCkE8Vw2e6"
ALGORITHM = "HS256"                # the algorithm used to sign the token
ACCESS_TOKEN_EXPIRE_MINUTES = 30   # how long a token lasts, here: 30 minutes


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()  # e.g., {'sub': username}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})   # set expiration claim
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
                raise credentials_exception
        token_data = TokenData(id=id)
    except jwt.InvalidTokenError:
        raise credentials_exception
    return token_data
    
def get_current_user(token:str = Depends(oauth2_scheme),session: Session = Depends(get_session)):
    # (token: Annotated[str, Depends(oauth2_scheme)]):
    #this is how annotated works
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token_data = verify_access_token(token,credentials_exception)
    
    statement = select(model.User).where(model.User.id == token_data.id)
    result = session.exec(statement).first()
    return result