"""
Test script for Dawn.com article scraper.
This script tests the scraper functionality without running the full API.
"""

import logging
from database import create_tables, get_db, get_article_count
from scraper import DawnScraper, run_dawn_scraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_database():
    """Test database functionality."""
    try:
        logger.info("Testing database functionality...")
        
        # Create tables
        create_tables()
        logger.info("✓ Database tables created successfully")
        
        # Get initial count
        db = next(get_db())
        initial_count = get_article_count(db)
        logger.info(f"✓ Initial article count: {initial_count}")
        
        db.close()
        return True
        
    except Exception as e:
        logger.error(f"✗ Database test failed: {e}")
        return False


def test_scraper():
    """Test scraper functionality."""
    try:
        logger.info("Testing scraper functionality...")
        
        # Create scraper instance
        scraper = DawnScraper()
        logger.info("✓ Scraper instance created successfully")
        
        # Test fetching latest news page
        soup = scraper.fetch_page(DAWN_LATEST_NEWS_URL)
        if soup:
            logger.info("✓ Successfully fetched latest news page")
        else:
            logger.error("✗ Failed to fetch latest news page")
            return False
        
        # Test extracting article links
        links = scraper.extract_article_links(soup)
        logger.info(f"✓ Found {len(links)} article links")
        
        if links:
            # Test scraping a single article
            test_url = links[0]
            logger.info(f"Testing article scraping: {test_url}")
            
            article_data = scraper.scrape_article(test_url)
            if article_data and article_data.get('title') and article_data.get('content'):
                logger.info(f"✓ Successfully scraped article: {article_data['title'][:50]}...")
                logger.info(f"✓ Article category: {article_data.get('category', 'Unknown')}")
                logger.info(f"✓ Content length: {len(article_data.get('content', ''))} characters")
            else:
                logger.error("✗ Failed to scrape article content")
                return False
        else:
            logger.warning("⚠ No article links found to test")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Scraper test failed: {e}")
        return False


def test_full_scraping():
    """Test full scraping workflow."""
    try:
        logger.info("Testing full scraping workflow...")
        
        # Get initial count
        db = next(get_db())
        initial_count = get_article_count(db)
        db.close()
        
        # Run scraper with limited articles
        logger.info("Running scraper with max 5 articles...")
        stats = run_dawn_scraper(max_articles=5)
        
        # Check results
        db = next(get_db())
        final_count = get_article_count(db)
        db.close()
        
        new_articles = final_count - initial_count
        logger.info(f"✓ Scraping completed:")
        logger.info(f"  - Total scraped: {stats['total_scraped']}")
        logger.info(f"  - Total saved: {stats['total_saved']}")
        logger.info(f"  - Duplicates skipped: {stats['duplicates_skipped']}")
        logger.info(f"  - New articles in DB: {new_articles}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Full scraping test failed: {e}")
        return False


def main():
    """Run all tests."""
    logger.info("Starting Dawn.com scraper tests...")
    
    tests = [
        ("Database", test_database),
        ("Scraper", test_scraper),
        ("Full Scraping", test_full_scraping)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running {test_name} test...")
        logger.info(f"{'='*50}")
        
        if test_func():
            logger.info(f"✓ {test_name} test PASSED")
            passed += 1
        else:
            logger.error(f"✗ {test_name} test FAILED")
    
    logger.info(f"\n{'='*50}")
    logger.info(f"Test Results: {passed}/{total} tests passed")
    logger.info(f"{'='*50}")
    
    if passed == total:
        logger.info("🎉 All tests passed! The scraper is working correctly.")
    else:
        logger.error("❌ Some tests failed. Please check the logs above.")
    
    return passed == total


if __name__ == "__main__":
    # Import the URL constant
    from scraper import DAWN_LATEST_NEWS_URL
    
    success = main()
    exit(0 if success else 1)
