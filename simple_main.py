"""
Simplified FastAPI application for Dawn.com article scraper.
This is a minimal version that should work reliably on Vercel.
"""

import logging
from datetime import datetime
from typing import List, Optional
import json

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Dawn.com Article Scraper API",
    description="A simple API for scraping Dawn.com articles",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple response models
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

# Mock data for testing
MOCK_ARTICLES = [
    {
        "id": 1,
        "title": "Sample Article 1",
        "content": "This is a sample article content for testing purposes.",
        "category": "Pakistan",
        "url": "https://example.com/article1",
        "published_date": "2024-01-01T10:00:00Z",
        "scraped_at": "2024-01-01T12:00:00Z",
        "is_processed": True
    },
    {
        "id": 2,
        "title": "Sample Article 2",
        "content": "This is another sample article content for testing purposes.",
        "category": "World",
        "url": "https://example.com/article2",
        "published_date": "2024-01-01T11:00:00Z",
        "scraped_at": "2024-01-01T12:00:00Z",
        "is_processed": True
    }
]

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

@app.get("/articles", response_model=List[ArticleResponse])
async def get_articles(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Articles per page")
):
    """Get all articles with pagination."""
    try:
        # Calculate pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Return paginated results
        articles = MOCK_ARTICLES[start_idx:end_idx]
        
        # Convert to response models
        response_articles = []
        for article in articles:
            response_articles.append(ArticleResponse(**article))
        
        return response_articles
        
    except Exception as e:
        logger.error(f"Error getting articles: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int):
    """Get a specific article by ID."""
    try:
        # Find article by ID
        article = None
        for a in MOCK_ARTICLES:
            if a["id"] == article_id:
                article = a
                break
        
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return ArticleResponse(**article)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting article {article_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/scrape")
async def scrape_articles(max_articles: int = Query(5, ge=1, le=50)):
    """Trigger article scraping (mock implementation)."""
    try:
        logger.info(f"Scraping triggered with max_articles={max_articles}")
        
        # Simulate scraping delay
        import time
        time.sleep(2)
        
        return {
            "message": "Scraping completed",
            "total_scraped": max_articles,
            "total_saved": max_articles,
            "duplicates_skipped": 0,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in scraping: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/stats")
async def get_stats():
    """Get database statistics."""
    try:
        return {
            "total_articles": len(MOCK_ARTICLES),
            "categories": {
                "Pakistan": 1,
                "World": 1
            },
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

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
