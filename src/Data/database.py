from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")
# Create the SQLAlchemy engine
engine=create_engine(DATABASE_URL)
Base=declarative_base()
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()