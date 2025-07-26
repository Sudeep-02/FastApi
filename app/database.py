from sqlmodel import  Session, create_engine

# STEP 1: Define your PostgreSQL database URL here
DATABASE_URL = "postgresql://postgres:9362@localhost:5432/fastapi" #postgres is username 


engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    return Session(engine)

