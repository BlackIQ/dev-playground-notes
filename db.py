# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Settings
from settings import settings

# Database Connection String
DATABASE_URL = settings.postgres_url

# Create Engine
engine = create_engine(DATABASE_URL)

# Create Session
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
