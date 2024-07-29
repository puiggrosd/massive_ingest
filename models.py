from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


POSTGRES_HOST=os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_USER=os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB=os.getenv("POSTGRES_DB", "mydatabase")

DATABASE_URL = f"postgresql://user:password@{POSTGRES_HOST}/mydatabase"

Base = declarative_base()

class JSONData(Base):
    __tablename__ = "json_data"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True)
    name = Column(String)
    description = Column(String)
    timestamp = Column(DateTime)

engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    Base.metadata.create_all(bind=engine)