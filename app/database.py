import os
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

dot_env_path = find_dotenv()
print(dot_env_path)
print(load_dotenv(dotenv_path=dot_env_path))


DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)
# print(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
