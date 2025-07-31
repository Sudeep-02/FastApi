from sqlmodel import  Session, create_engine
from .config import settings

# STEP 1: Define your PostgreSQL database URL here
DATABASE_URL = f"postgresql://{settings.database_url}" #postgres is username 


engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    return Session(engine)

