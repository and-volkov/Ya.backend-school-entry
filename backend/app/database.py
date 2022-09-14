from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.settings import db_settings

DB_URL = db_settings.uri

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
