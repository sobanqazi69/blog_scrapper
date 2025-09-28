"""
Startup script for Dawn.com article scraper.
This script initializes the database and starts the FastAPI server.
"""

import logging
import uvicorn
from database import create_tables
from config import get_config, API_HOST, API_PORT, API_DEBUG, SCHEDULER_ENABLED, SCHEDULER_MAX_ARTICLES
from scheduler import start_scheduled_scraping

# Configure logging
config = get_config()
logging.basicConfig(
    level=getattr(logging, config['log_level']),
    format=config['log_format']
)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to start the application.
    """
    try:
        logger.info("Starting Dawn.com Article Scraper")
        
        # Create database tables
        logger.info("Creating database tables...")
        create_tables()
        logger.info("Database tables created successfully")
        
        # Start scheduler if enabled
        if SCHEDULER_ENABLED:
            logger.info("Starting scheduled scraping...")
            start_scheduled_scraping(max_articles=SCHEDULER_MAX_ARTICLES)
            logger.info("Scheduled scraping started")
        else:
            logger.info("Scheduled scraping is disabled")
        
        # Start FastAPI server
        logger.info(f"Starting FastAPI server on {API_HOST}:{API_PORT}")
        uvicorn.run(
            "main:app",
            host=API_HOST,
            port=API_PORT,
            reload=API_DEBUG,
            log_level=config['log_level'].lower()
        )
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        raise


if __name__ == "__main__":
    main()
