"""
Dawn.com web scraper module.
This module handles scraping articles from Dawn.com's latest news section.
"""

import logging
import re
import time
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from database import Article, add_article, get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dawn.com configuration
DAWN_BASE_URL = "https://www.dawn.com"
DAWN_LATEST_NEWS_URL = "https://www.dawn.com/latest-news"

# Request headers to mimic a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Category mapping based on common keywords in titles
CATEGORY_KEYWORDS = {
    'Pakistan': ['pakistan', 'pakistani', 'islamabad', 'karachi', 'lahore', 'punjab', 'sindh', 'balochistan', 'kpk'],
    'World': ['world', 'international', 'global', 'china', 'india', 'america', 'europe', 'afghanistan', 'iran'],
    'Business': ['business', 'economy', 'economic', 'market', 'trade', 'finance', 'bank', 'rupee', 'dollar', 'inflation'],
    'Sports': ['sports', 'cricket', 'football', 'hockey', 'tennis', 'olympics', 'asia cup', 'world cup', 'match'],
    'Technology': ['technology', 'tech', 'digital', 'ai', 'artificial intelligence', 'cyber', 'internet', 'social media'],
    'Health': ['health', 'medical', 'doctor', 'hospital', 'vaccine', 'covid', 'disease', 'treatment'],
    'Politics': ['politics', 'political', 'government', 'minister', 'parliament', 'election', 'vote', 'democracy'],
    'Crime': ['crime', 'criminal', 'police', 'court', 'jail', 'arrest', 'murder', 'theft', 'fraud'],
    'Education': ['education', 'school', 'university', 'student', 'teacher', 'exam', 'degree', 'college'],
    'Entertainment': ['entertainment', 'movie', 'music', 'celebrity', 'actor', 'singer', 'film', 'show']
}


class DawnScraper:
    """
    Main scraper class for Dawn.com articles.
    Handles fetching, parsing, and storing articles from the latest news section.
    """
    
    def __init__(self):
        """Initialize the scraper with session and configuration."""
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.base_url = DAWN_BASE_URL
        self.latest_news_url = DAWN_LATEST_NEWS_URL
        
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object if successful, None otherwise
        """
        try:
            logger.debug(f"Fetching URL: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")
            return None
    
    def extract_article_links(self, soup: BeautifulSoup) -> List[str]:
        """
        Extract article links from the latest news page.
        
        Args:
            soup: BeautifulSoup object of the latest news page
            
        Returns:
            List of article URLs
        """
        article_links = []
        
        try:
            # Look for article links - Dawn.com uses various selectors
            # Try different selectors to find article links
            selectors = [
                'article a[href*="/"]',  # Links within article tags
                '.story__link',  # Story links
                'a[href*="/news/"]',  # News links
                'a[href*="/story/"]',  # Story links
                '.media__item a',  # Media item links
                'h2 a',  # Headline links
                'h3 a',  # Sub-headline links
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        # Convert relative URLs to absolute URLs
                        full_url = urljoin(self.base_url, href)
                        if full_url not in article_links:
                            article_links.append(full_url)
            
            # Filter out non-article links
            article_links = [url for url in article_links if self.is_valid_article_url(url)]
            
            logger.info(f"Found {len(article_links)} article links")
            return article_links
            
        except Exception as e:
            logger.error(f"Error extracting article links: {e}")
            return []
    
    def is_valid_article_url(self, url: str) -> bool:
        """
        Check if a URL is a valid article URL.
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid article URL, False otherwise
        """
        try:
            parsed_url = urlparse(url)
            
            # Must be from dawn.com
            if 'dawn.com' not in parsed_url.netloc:
                return False
            
            # Must have a path (not just the domain)
            if not parsed_url.path or parsed_url.path == '/':
                return False
            
            # Exclude certain paths that are not articles
            excluded_paths = [
                '/latest-news',
                '/home',
                '/opinion',
                '/business',
                '/sport',
                '/world',
                '/pakistan',
                '/images',
                '/videos',
                '/search',
                '/subscribe',
                '/advertise',
                '/contact',
                '/about',
                '/privacy',
                '/terms',
                '/cookies',
                '/rss',
                '/sitemap'
            ]
            
            for excluded_path in excluded_paths:
                if parsed_url.path.startswith(excluded_path):
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating URL {url}: {e}")
            return False
    
    def extract_article_content(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract article content from a single article page.
        
        Args:
            soup: BeautifulSoup object of the article page
            
        Returns:
            Dictionary containing article data
        """
        article_data = {
            'title': '',
            'content': '',
            'category': '',
            'url': '',
            'published_date': None
        }
        
        try:
            # Extract title
            title_selectors = [
                'h1.story__title',
                'h1.media__title',
                'h1',
                '.story__headline',
                '.media__headline'
            ]
            
            for selector in title_selectors:
                title_element = soup.select_one(selector)
                if title_element:
                    article_data['title'] = title_element.get_text(strip=True)
                    break
            
            # Extract content
            content_selectors = [
                '.story__content',
                '.media__content',
                '.article-content',
                '.story__body',
                '.media__body',
                'article .content',
                '.entry-content'
            ]
            
            content_parts = []
            for selector in content_selectors:
                content_elements = soup.select(selector)
                for element in content_elements:
                    # Extract text from paragraphs
                    paragraphs = element.find_all('p')
                    for p in paragraphs:
                        text = p.get_text(strip=True)
                        if text and len(text) > 20:  # Filter out very short text
                            content_parts.append(text)
            
            article_data['content'] = ' '.join(content_parts)
            
            # Extract category from title or content
            article_data['category'] = self.categorize_article(
                article_data['title'], 
                article_data['content']
            )
            
            # Extract published date
            date_selectors = [
                '.story__time',
                '.media__time',
                '.story__date',
                '.media__date',
                'time',
                '.timestamp'
            ]
            
            for selector in date_selectors:
                date_element = soup.select_one(selector)
                if date_element:
                    date_text = date_element.get_text(strip=True)
                    article_data['published_date'] = self.parse_date(date_text)
                    break
            
            # Clean up content
            article_data['content'] = self.clean_content(article_data['content'])
            
            return article_data
            
        except Exception as e:
            logger.error(f"Error extracting article content: {e}")
            return article_data
    
    def categorize_article(self, title: str, content: str) -> str:
        """
        Categorize an article based on its title and content.
        
        Args:
            title: Article title
            content: Article content
            
        Returns:
            Category name
        """
        try:
            # Combine title and content for analysis
            text = f"{title} {content}".lower()
            
            # Count keyword matches for each category
            category_scores = {}
            for category, keywords in CATEGORY_KEYWORDS.items():
                score = sum(1 for keyword in keywords if keyword in text)
                if score > 0:
                    category_scores[category] = score
            
            # Return category with highest score, or 'General' if no matches
            if category_scores:
                return max(category_scores, key=category_scores.get)
            else:
                return 'General'
                
        except Exception as e:
            logger.error(f"Error categorizing article: {e}")
            return 'General'
    
    def parse_date(self, date_text: str) -> Optional[datetime]:
        """
        Parse date string to datetime object.
        
        Args:
            date_text: Date string to parse
            
        Returns:
            Datetime object if successful, None otherwise
        """
        try:
            # Common date formats used by Dawn.com
            date_formats = [
                '%d %b, %Y %I:%M%p',
                '%d %B, %Y %I:%M%p',
                '%d %b %Y %I:%M%p',
                '%d %B %Y %I:%M%p',
                '%Y-%m-%d %H:%M:%S',
                '%d/%m/%Y %H:%M',
                '%d-%m-%Y %H:%M'
            ]
            
            for date_format in date_formats:
                try:
                    return datetime.strptime(date_text, date_format)
                except ValueError:
                    continue
            
            # If no format matches, try to extract date-like patterns
            date_pattern = r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})'
            match = re.search(date_pattern, date_text)
            if match:
                day, month, year = match.groups()
                return datetime(int(year), int(month), int(day))
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing date '{date_text}': {e}")
            return None
    
    def clean_content(self, content: str) -> str:
        """
        Clean and normalize article content.
        
        Args:
            content: Raw content string
            
        Returns:
            Cleaned content string
        """
        try:
            # Remove extra whitespace
            content = re.sub(r'\s+', ' ', content)
            
            # Remove common unwanted patterns
            unwanted_patterns = [
                r'Published \d+ \w+ \d+',
                r'Updated \d+ \w+ \d+',
                r'Last updated \d+ \w+ \d+',
                r'Follow Dawn\.com on.*',
                r'Read more.*',
                r'Advertisement.*',
                r'Sponsored.*'
            ]
            
            for pattern in unwanted_patterns:
                content = re.sub(pattern, '', content, flags=re.IGNORECASE)
            
            # Remove extra spaces and newlines
            content = content.strip()
            
            return content
            
        except Exception as e:
            logger.error(f"Error cleaning content: {e}")
            return content
    
    def scrape_article(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrape a single article from its URL.
        
        Args:
            url: Article URL to scrape
            
        Returns:
            Dictionary containing article data if successful, None otherwise
        """
        try:
            soup = self.fetch_page(url)
            if not soup:
                return None
            
            article_data = self.extract_article_content(soup)
            article_data['url'] = url
            
            # Validate article data
            if not article_data['title'] or not article_data['content']:
                logger.warning(f"Incomplete article data for {url}")
                return None
            
            # Ensure content is substantial
            if len(article_data['content']) < 100:
                logger.warning(f"Article content too short for {url}")
                return None
            
            return article_data
            
        except Exception as e:
            logger.error(f"Error scraping article {url}: {e}")
            return None
    
    def scrape_latest_articles(self, max_articles: int = 50) -> List[Dict[str, str]]:
        """
        Scrape the latest articles from Dawn.com, prioritizing recent articles.
        
        Args:
            max_articles: Maximum number of articles to scrape
            
        Returns:
            List of article data dictionaries
        """
        try:
            logger.info("🔍 Starting to scrape latest articles from Dawn.com")
            
            # Fetch the latest news page
            soup = self.fetch_page(self.latest_news_url)
            if not soup:
                logger.error("❌ Failed to fetch latest news page")
                return []
            
            # Extract article links
            article_links = self.extract_article_links(soup)
            if not article_links:
                logger.warning("⚠️ No article links found")
                return []
            
            # Limit the number of articles to scrape
            article_links = article_links[:max_articles]
            logger.info(f"📰 Found {len(article_links)} article links to check")
            
            # Scrape each article
            articles = []
            new_articles = 0
            recent_articles = 0  # Articles from last 10 minutes
            
            for i, url in enumerate(article_links, 1):
                logger.info(f"🔍 Checking article {i}/{len(article_links)}: {url}")
                
                article_data = self.scrape_article(url)
                if article_data:
                    articles.append(article_data)
                    new_articles += 1
                    
                    # Check if article is from last 10 minutes
                    if self.is_recent_article(article_data):
                        recent_articles += 1
                        logger.info(f"🆕 RECENT: {article_data['title'][:50]}...")
                    else:
                        logger.info(f"✅ Scraped: {article_data['title'][:50]}...")
                else:
                    logger.debug(f"⏭️ Skipped: {url}")
                
                # Add small delay to be respectful to the server
                time.sleep(0.3)  # Even faster for recent article detection
            
            logger.info(f"🎉 Scraping completed: {len(articles)} articles found, {new_articles} new, {recent_articles} recent")
            return articles
            
        except Exception as e:
            logger.error(f"❌ Error scraping latest articles: {e}")
            return []
    
    def is_recent_article(self, article_data: Dict[str, str]) -> bool:
        """
        Check if an article was published in the last 10 minutes.
        
        Args:
            article_data: Article data dictionary
            
        Returns:
            True if article is from last 10 minutes, False otherwise
        """
        try:
            published_date = article_data.get('published_date')
            if not published_date:
                return False
            
            # Parse the published date
            if isinstance(published_date, str):
                from datetime import datetime
                try:
                    # Try different date formats
                    for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%d %b, %Y %I:%M%p']:
                        try:
                            pub_date = datetime.strptime(published_date, fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        return False
                except:
                    return False
            else:
                pub_date = published_date
            
            # Check if article is from last 10 minutes
            now = datetime.utcnow()
            time_diff = (now - pub_date).total_seconds()
            
            return time_diff <= 600  # 600 seconds = 10 minutes
            
        except Exception as e:
            logger.debug(f"Error checking if article is recent: {e}")
            return False
    
    def save_articles_to_db(self, articles: List[Dict[str, str]]) -> int:
        """
        Save scraped articles to the database.
        
        Args:
            articles: List of article data dictionaries
            
        Returns:
            Number of articles successfully saved
        """
        try:
            db = next(get_db())
            saved_count = 0
            
            for article_data in articles:
                try:
                    article = add_article(db, article_data)
                    if article:
                        saved_count += 1
                        logger.info(f"Saved article: {article.title[:50]}...")
                    else:
                        logger.debug(f"Article already exists or failed to save: {article_data.get('title', 'Unknown')}")
                except Exception as e:
                    logger.error(f"Error saving article: {e}")
                    continue
            
            logger.info(f"Successfully saved {saved_count} articles to database")
            return saved_count
            
        except Exception as e:
            logger.error(f"Error saving articles to database: {e}")
            return 0
        finally:
            if 'db' in locals():
                db.close()
    
    def run_scraping_job(self, max_articles: int = 50) -> Dict[str, int]:
        """
        Run a complete scraping job.
        
        Args:
            max_articles: Maximum number of articles to scrape
            
        Returns:
            Dictionary with scraping statistics
        """
        try:
            logger.info("Starting Dawn.com scraping job")
            
            # Scrape articles
            articles = self.scrape_latest_articles(max_articles)
            
            # Save to database
            saved_count = self.save_articles_to_db(articles)
            
            stats = {
                'total_scraped': len(articles),
                'total_saved': saved_count,
                'duplicates_skipped': len(articles) - saved_count
            }
            
            logger.info(f"Scraping job completed. Stats: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error in scraping job: {e}")
            return {'total_scraped': 0, 'total_saved': 0, 'duplicates_skipped': 0}


# Convenience function for running the scraper
def run_dawn_scraper(max_articles: int = 50) -> Dict[str, int]:
    """
    Convenience function to run the Dawn scraper.
    
    Args:
        max_articles: Maximum number of articles to scrape
        
    Returns:
        Dictionary with scraping statistics
    """
    scraper = DawnScraper()
    return scraper.run_scraping_job(max_articles)
