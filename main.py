"""
Production-ready FastAPI application for Dawn.com article scraper.
This is the final, robust version with real scraping functionality.
"""

import logging
from datetime import datetime
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
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
from scraper import DawnScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for API responses
class ArticleResponse(BaseModel):
    """Response model for article data."""
    id: int
    title: str
    content: str
    category: Optional[str] = None
    url: Optional[str] = None
    published_date: Optional[str] = None
    scraped_at: str
    is_processed: bool = False

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    timestamp: str
    service: str

class ScrapingStatsResponse(BaseModel):
    """Response model for scraping statistics."""
    total_scraped: int
    total_saved: int
    duplicates_skipped: int
    timestamp: str

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
@app.get("/", response_model=dict)
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "Dawn.com Article Scraper API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "health": "/health",
            "articles": "/articles",
            "articles_by_id": "/articles/{article_id}",
            "articles_by_category": "/articles/category/{category}",
            "search_articles": "/articles/search",
            "scrape_articles": "/scrape",
            "stats": "/stats",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        service="Dawn.com Article Scraper API"
    )

@app.get("/favicon.ico")
async def favicon():
    """Handle favicon requests to prevent 500 errors."""
    return JSONResponse(
        status_code=404,
        content={"message": "Favicon not found"}
    )

@app.get("/favicon.png")
async def favicon_png():
    """Handle favicon.png requests to prevent 500 errors."""
    return JSONResponse(
        status_code=404,
        content={"message": "Favicon not found"}
    )

@app.get("/robots.txt")
async def robots():
    """Handle robots.txt requests."""
    return JSONResponse(
        status_code=404,
        content={"message": "Robots.txt not found"}
    )

@app.get("/articles", response_model=List[ArticleResponse])
async def get_articles(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Articles per page"),
    db: Session = Depends(get_db)
):
    """Get all articles with pagination."""
    try:
        # Get articles from database
        skip = (page - 1) * page_size
        articles = get_all_articles(db, skip=skip, limit=page_size)
        
        # Convert to response models
        response_articles = []
        for article in articles:
            response_articles.append(convert_article_to_response(article))
        
        return response_articles
        
    except Exception as e:
        logger.error(f"Error getting articles: {e}")
        # Return empty list if database fails
        return []

@app.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get a specific article by ID."""
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

@app.get("/articles/category/{category}", response_model=List[ArticleResponse])
async def get_articles_by_category_endpoint(
    category: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Articles per page"),
    db: Session = Depends(get_db)
):
    """Get articles by category with pagination."""
    try:
        skip = (page - 1) * page_size
        articles = get_articles_by_category(db, category, skip=skip, limit=page_size)
        
        response_articles = []
        for article in articles:
            response_articles.append(convert_article_to_response(article))
        
        return response_articles
        
    except Exception as e:
        logger.error(f"Error getting articles by category {category}: {e}")
        return []

@app.get("/articles/search", response_model=List[ArticleResponse])
async def search_articles_endpoint(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Articles per page"),
    db: Session = Depends(get_db)
):
    """Search articles by title or content."""
    try:
        skip = (page - 1) * page_size
        articles = search_articles(db, q, skip=skip, limit=page_size)
        
        response_articles = []
        for article in articles:
            response_articles.append(convert_article_to_response(article))
        
        return response_articles
        
    except Exception as e:
        logger.error(f"Error searching articles: {e}")
        return []

@app.post("/scrape", response_model=ScrapingStatsResponse)
async def scrape_articles(
    background_tasks: BackgroundTasks,
    max_articles: int = Query(5, ge=1, le=50, description="Maximum number of articles to scrape")
):
    """Trigger article scraping from Dawn.com."""
    try:
        logger.info(f"Starting scraping job with max_articles={max_articles}")
        
        # Run scraping in background
        def run_scraping():
            try:
                scraper = DawnScraper()
                articles = scraper.scrape_latest_articles(max_articles)
                saved_count = scraper.save_articles_to_db(articles)
                
                logger.info(f"Scraping completed: {len(articles)} scraped, {saved_count} saved")
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
    """Get database statistics."""
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
        return {
            "total_articles": 0,
            "categories": {},
            "last_updated": datetime.utcnow().isoformat(),
            "error": "Database unavailable"
        }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "detail": "The requested resource was not found",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)