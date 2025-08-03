from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings

# Database engine
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SocialMediaPost(Base):
    __tablename__ = "social_media_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)  # instagram, facebook, twitter, etc.
    post_id = Column(String, unique=True, index=True)
    username = Column(String)
    caption = Column(Text)
    media_type = Column(String)  # image, video, carousel
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    views = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    posted_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class CompetitorPost(Base):
    __tablename__ = "competitor_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    post_id = Column(String, unique=True, index=True)
    username = Column(String)
    caption = Column(Text)
    media_type = Column(String)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    views = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    posted_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class ContentIdea(Base):
    __tablename__ = "content_ideas"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    idea_type = Column(String)  # image, caption, video
    content = Column(Text)
    strategy = Column(Text)
    brand_guidelines = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow) 