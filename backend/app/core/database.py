from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base

database_url = "sqlite:///./data/app.db"  # Replace with your actual database URL
engine = create_engine(database_url, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  
