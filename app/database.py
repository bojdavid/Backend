from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Settings

SQL_ALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://root:{Settings.database_password}@{Settings.database_hostname}/fastApiTutorial"
# Create an engine
engine = create_engine(SQL_ALCHEMY_DATABASE_URI)

# Create a session
SessionLocal = sessionmaker(autocommit=False  ,autoflush=False, bind=engine)

# Define a base class for the models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()