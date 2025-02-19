from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from config import settings as ss

# Define your database URL with MySQL connector
DATABASE_URL = f'postgresql+psycopg2://{ss.DATABASE_USERNAME}:{ss.DATABASE_PASSWORD}@{ss.DATABASE_HOSTNAME}:{ss.DATABASE_PORT}/{ss.DATABASE_NAME}'
DATABASE_URL2 = f'postgresql+psycopg2://{ss.DATABASE_USERNAME2}:{ss.DATABASE_PASSWORD2}@{ss.DATABASE_HOSTNAME2}:{ss.DATABASE_PORT2}/{ss.DATABASE_NAME}'

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)
engine2 = create_engine(DATABASE_URL2, echo=True)

# Base class for declarative models
Base = declarative_base()
Base2 = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
def get_db2():
    db = SessionLocal2()
    try:
        yield db
    finally:
        db.close()

