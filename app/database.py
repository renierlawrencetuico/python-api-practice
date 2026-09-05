from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# Connection to db using SQLalchemy
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()



# Connection to db normal sql (PostgreSQL)
# while True:
#     try: 
#         conn = psycopg2.connect(host='localhost', database='projectone', user='postgres', password='lance1248', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database Connected!")
#         break
#     except Exception as err:
#         print("Connect Failed")
#         print("Error:", err)
#         time.sleep(2)        