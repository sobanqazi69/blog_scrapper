"""
FastAPI application for Dawn.com article scraper.
This module provides REST API endpoints for accessing scraped articles.
"""

import logging
from datetime import datetime
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import (
    get_db, 
    Article, 
    get_article_by_id, 
    get_all_articles, 
    get_articles_by_category,
    get_article_count,
    search_articles,
    create_tables
)
from scraper import DawnScraper, run_dawn_scraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic models for API responses
class ArticleResponse(BaseModel):
    """Response model for article data."""
    id: int
    title: str
    content: str
    category: Optional[str]
    url: Optional[str]
    published_date: Optional[str]  # Changed to string for JSON serialization
    scraped_at: str  # Changed to string for JSON serialization
    is_processed: bool
    
    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    """Response model for paginated article list."""
    articles: List[ArticleResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int


class ScrapingStatsResponse(BaseModel):
    """Response model for scraping statistics."""
    total_scraped: int
    total_saved: int
    duplicates_skipped: int
    timestamp: str  # Changed to string for JSON serialization


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str
    detail: Optional[str] = None
    timestamp: str  # Changed to string for JSON serialization


def convert_article_to_response(article: Article) -> ArticleResponse:
    """Convert database Article to ArticleResponse with proper datetime serialization."""
    return ArticleResponse(
        id=article.id,
        title=article.title,
        content=article.content,
        category=article.category,
        url=article.url,
        published_date=article.published_date.isoformat() if article.published_date else None,
        scraped_at=article.scraped_at.isoformat(),
        is_processed=article.is_processed
    )


# Application lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events."""
    # Startup
    logger.info("Starting Dawn.com Article Scraper API")
    try:
        create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Dawn.com Article Scraper API")


# Create FastAPI application
app = FastAPI(
    title="Dawn.com Article Scraper API",
    description="A REST API for scraping and accessing articles from Dawn.com",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Endpoints
@app.get("/", response_model=dict)
async def root():
    """
    Root endpoint providing API information.
    """
    return {
        "message": "Dawn.com Article Scraper API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "articles": "/articles",
            "article_by_id": "/articles/{article_id}",
            "articles_by_category": "/articles/category/{category}",
            "search_articles": "/articles/search",
            "scrape_articles": "/scrape",
            "stats": "/stats"
        }
    }


@app.get("/articles", response_model=ArticleListResponse)
async def get_articles(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of articles per page"),
    db: Session = Depends(get_db)
):
    """
    Get all articles with pagination.
    
    Args:
        page: Page number (starts from 1)
        page_size: Number of articles per page (max 100)
        db: Database session
        
    Returns:
        Paginated list of articles
    """
    try:
        # Calculate offset
        skip = (page - 1) * page_size
        
        # Get articles and total count
        articles = get_all_articles(db, skip=skip, limit=page_size)
        total_count = get_article_count(db)
        
        # Calculate total pages
        total_pages = (total_count + page_size - 1) // page_size
        
        # Convert to response models
        article_responses = [convert_article_to_response(article) for article in articles]
        
        return ArticleListResponse(
            articles=article_responses,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
    except Exception as e:
        logger.error(f"Error getting articles: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific article by ID.
    
    Args:
        article_id: ID of the article to retrieve
        db: Database session
        
    Returns:
        Article data
    """
    try:
        article = get_article_by_id(db, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return convert_article_to_response(article)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting article {article_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/articles/category/{category}", response_model=ArticleListResponse)
async def get_articles_by_category_endpoint(
    category: str,
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of articles per page"),
    db: Session = Depends(get_db)
):
    """
    Get articles by category with pagination.
    
    Args:
        category: Category name to filter by
        page: Page number (starts from 1)
        page_size: Number of articles per page (max 100)
        db: Database session
        
    Returns:
        Paginated list of articles in the specified category
    """
    try:
        # Calculate offset
        skip = (page - 1) * page_size
        
        # Get articles by category
        articles = get_articles_by_category(db, category, skip=skip, limit=page_size)
        
        # Get total count for this category
        total_count = len(get_articles_by_category(db, category, skip=0, limit=10000))
        
        # Calculate total pages
        total_pages = (total_count + page_size - 1) // page_size
        
        # Convert to response models
        article_responses = [convert_article_to_response(article) for article in articles]
        
        return ArticleListResponse(
            articles=article_responses,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
    except Exception as e:
        logger.error(f"Error getting articles by category {category}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/articles/search", response_model=ArticleListResponse)
async def search_articles_endpoint(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of articles per page"),
    db: Session = Depends(get_db)
):
    """
    Search articles by title or content.
    
    Args:
        q: Search query string
        page: Page number (starts from 1)
        page_size: Number of articles per page (max 100)
        db: Database session
        
    Returns:
        Paginated list of articles matching the search query
    """
    try:
        # Calculate offset
        skip = (page - 1) * page_size
        
        # Search articles
        articles = search_articles(db, q, skip=skip, limit=page_size)
        
        # Get total count for search results
        total_count = len(search_articles(db, q, skip=0, limit=10000))
        
        # Calculate total pages
        total_pages = (total_count + page_size - 1) // page_size
        
        # Convert to response models
        article_responses = [convert_article_to_response(article) for article in articles]
        
        return ArticleListResponse(
            articles=article_responses,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
    except Exception as e:
        logger.error(f"Error searching articles: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/scrape", response_model=ScrapingStatsResponse)
async def scrape_articles(
    background_tasks: BackgroundTasks,
    max_articles: int = Query(50, ge=1, le=200, description="Maximum number of articles to scrape")
):
    """
    Trigger article scraping from Dawn.com.
    
    Args:
        background_tasks: FastAPI background tasks
        max_articles: Maximum number of articles to scrape
        
    Returns:
        Scraping statistics
    """
    try:
        logger.info(f"Starting scraping job with max_articles={max_articles}")
        
        # Run scraping in background
        def run_scraping():
            try:
                stats = run_dawn_scraper(max_articles)
                logger.info(f"Scraping completed: {stats}")
            except Exception as e:
                logger.error(f"Error in background scraping: {e}")
        
        background_tasks.add_task(run_scraping)
        
        return ScrapingStatsResponse(
            total_scraped=0,  # Will be updated by background task
            total_saved=0,
            duplicates_skipped=0,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error starting scraping job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/stats", response_model=dict)
async def get_stats(db: Session = Depends(get_db)):
    """
    Get database statistics.
    
    Args:
        db: Database session
        
    Returns:
        Database statistics
    """
    try:
        total_articles = get_article_count(db)
        
        # Get category distribution
        categories = {}
        articles = get_all_articles(db, skip=0, limit=10000)
        for article in articles:
            category = article.category or 'Uncategorized'
            categories[category] = categories.get(category, 0) + 1
        
        return {
            "total_articles": total_articles,
            "categories": categories,
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health", response_model=dict)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Dawn.com Article Scraper API"
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            error="Not Found",
            detail="The requested resource was not found",
            timestamp=datetime.utcnow().isoformat()
        ).dict()
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error",
            detail="An unexpected error occurred",
            timestamp=datetime.utcnow().isoformat()
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
