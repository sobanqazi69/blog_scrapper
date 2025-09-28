"""
Database configuration and models for Dawn.com article scraper.
This module defines the SQLAlchemy models and database setup.
"""

import logging
from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
import os
import tempfile

# Use appropriate database for the environment
if os.getenv("VERCEL"):
    # For Vercel deployment - use temporary file in /tmp directory
    db_path = "/tmp/dawn_articles.db"
    DATABASE_URL = f"sqlite:///{db_path}"
    connect_args = {}
else:
    # For local development - use file-based database
    DATABASE_URL = "sqlite:///./dawn_articles.db"
    connect_args = {"check_same_thread": False}

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args,
    echo=False  # Set to True for SQL query logging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


class Article(Base):
    """
    SQLAlchemy model for storing Dawn.com articles.
    Each article has a unique ID, title, content, category, and metadata.
    """
    __tablename__ = "articles"
    
    # Primary key - auto-incrementing integer
    id = Column(Integer, primary_key=True, index=True)
    
    # Article content fields
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=True, index=True)
    url = Column(String(1000), nullable=True, unique=True)
    
    # Metadata fields
    published_date = Column(DateTime, nullable=True, index=True)
    scraped_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_processed = Column(Boolean, default=False, nullable=False)
    
    # Ensure no duplicate articles based on title and URL
    __table_args__ = (
        UniqueConstraint('title', name='unique_title'),
        UniqueConstraint('url', name='unique_url'),
    )
    
    def __repr__(self):
        """String representation of Article object for debugging."""
        return f"<Article(id={self.id}, title='{self.title[:50]}...', category='{self.category}')>"


def create_tables():
    """
    Create all database tables based on the models.
    This function should be called when the application starts.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def ensure_tables_exist():
    """Ensure tables exist, create them if they don't."""
    try:
        # Simply try to create tables - SQLAlchemy handles if they already exist
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables ensured/created successfully")
    except Exception as e:
        logger.error(f"Error ensuring tables exist: {e}")
        # This is a critical error, but we'll continue
        pass


def get_db() -> Session:
    """
    Dependency function to get database session.
    This is used by FastAPI to inject database sessions into endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_article(db: Session, article_data: dict) -> Optional[Article]:
    """
    Add a new article to the database.
    
    Args:
        db: Database session
        article_data: Dictionary containing article information
        
    Returns:
        Article object if successfully added, None if duplicate or error
    """
    try:
        # Check if article already exists by title or URL
        existing_article = None
        if article_data.get('title'):
            existing_article = db.query(Article).filter(
                Article.title == article_data['title']
            ).first()
        
        if not existing_article and article_data.get('url'):
            existing_article = db.query(Article).filter(
                Article.url == article_data['url']
            ).first()
        
        if existing_article:
            logger.debug(f"Article already exists: {article_data.get('title', 'Unknown')}")
            return None
        
        # Create new article
        article = Article(
            title=article_data.get('title', ''),
            content=article_data.get('content', ''),
            category=article_data.get('category'),
            url=article_data.get('url'),
            published_date=article_data.get('published_date'),
            is_processed=article_data.get('is_processed', False)
        )
        
        db.add(article)
        db.commit()
        db.refresh(article)
        
        logger.info(f"Article added successfully: {article.title[:50]}...")
        return article
        
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Duplicate article detected: {e}")
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding article: {e}")
        return None


def get_article_by_id(db: Session, article_id: int) -> Optional[Article]:
    """
    Retrieve an article by its ID.
    
    Args:
        db: Database session
        article_id: ID of the article to retrieve
        
    Returns:
        Article object if found, None otherwise
    """
    try:
        return db.query(Article).filter(Article.id == article_id).first()
    except Exception as e:
        logger.error(f"Error retrieving article {article_id}: {e}")
        return None


def get_all_articles(db: Session, skip: int = 0, limit: int = 100) -> list[Article]:
    """
    Retrieve all articles with pagination.
    
    Args:
        db: Database session
        skip: Number of articles to skip (for pagination)
        limit: Maximum number of articles to return
        
    Returns:
        List of Article objects
    """
    try:
        return db.query(Article).order_by(Article.scraped_at.desc()).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error retrieving articles: {e}")
        # Return empty list instead of raising exception
        return []


def get_articles_by_category(db: Session, category: str, skip: int = 0, limit: int = 100) -> list[Article]:
    """
    Retrieve articles by category with pagination.
    
    Args:
        db: Database session
        category: Category to filter by
        skip: Number of articles to skip (for pagination)
        limit: Maximum number of articles to return
        
    Returns:
        List of Article objects in the specified category
    """
    try:
        return db.query(Article).filter(
            Article.category == category
        ).order_by(Article.scraped_at.desc()).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error retrieving articles by category {category}: {e}")
        return []


def get_article_count(db: Session) -> int:
    """
    Get total number of articles in the database.
    
    Args:
        db: Database session
        
    Returns:
        Total count of articles
    """
    try:
        return db.query(Article).count()
    except Exception as e:
        logger.error(f"Error getting article count: {e}")
        return 0


def search_articles(db: Session, query: str, skip: int = 0, limit: int = 100) -> list[Article]:
    """
    Search articles by title or content.
    
    Args:
        db: Database session
        query: Search query string
        skip: Number of articles to skip (for pagination)
        limit: Maximum number of articles to return
        
    Returns:
        List of Article objects matching the search query
    """
    try:
        search_pattern = f"%{query}%"
        return db.query(Article).filter(
            (Article.title.contains(search_pattern)) | 
            (Article.content.contains(search_pattern))
        ).order_by(Article.scraped_at.desc()).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error searching articles: {e}")
        return []
