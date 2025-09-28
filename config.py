"""
Configuration settings for Dawn.com article scraper.
"""

import os
from typing import Dict, Any

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dawn_articles.db")

# Dawn.com scraping configuration
DAWN_BASE_URL = "https://www.dawn.com"
DAWN_LATEST_NEWS_URL = "https://www.dawn.com/latest-news"

# Scraping settings
DEFAULT_MAX_ARTICLES = int(os.getenv("DEFAULT_MAX_ARTICLES", "50"))
SCRAPING_DELAY = float(os.getenv("SCRAPING_DELAY", "1.0"))  # seconds between requests
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))  # seconds

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_DEBUG = os.getenv("API_DEBUG", "false").lower() == "true"

# Scheduler settings
SCHEDULER_ENABLED = os.getenv("SCHEDULER_ENABLED", "true").lower() == "true"
SCHEDULER_MAX_ARTICLES = int(os.getenv("SCHEDULER_MAX_ARTICLES", "30"))

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Request headers for web scraping
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Category keywords for article classification
CATEGORY_KEYWORDS = {
    'Pakistan': [
        'pakistan', 'pakistani', 'islamabad', 'karachi', 'lahore', 'punjab', 
        'sindh', 'balochistan', 'kpk', 'khyber', 'pakhtunkhwa', 'azad kashmir',
        'gilgit', 'baltistan', 'federal', 'provincial', 'assembly', 'senate'
    ],
    'World': [
        'world', 'international', 'global', 'china', 'india', 'america', 
        'europe', 'afghanistan', 'iran', 'saudi', 'uae', 'turkey', 'russia',
        'ukraine', 'israel', 'palestine', 'gaza', 'united nations', 'un'
    ],
    'Business': [
        'business', 'economy', 'economic', 'market', 'trade', 'finance', 
        'bank', 'rupee', 'dollar', 'inflation', 'gdp', 'budget', 'tax',
        'investment', 'stock', 'share', 'company', 'corporate', 'industry'
    ],
    'Sports': [
        'sports', 'cricket', 'football', 'hockey', 'tennis', 'olympics', 
        'asia cup', 'world cup', 'match', 'player', 'team', 'tournament',
        'championship', 'league', 'game', 'score', 'victory', 'defeat'
    ],
    'Technology': [
        'technology', 'tech', 'digital', 'ai', 'artificial intelligence', 
        'cyber', 'internet', 'social media', 'computer', 'software', 'app',
        'mobile', 'smartphone', 'innovation', 'startup', 'data', 'privacy'
    ],
    'Health': [
        'health', 'medical', 'doctor', 'hospital', 'vaccine', 'covid', 
        'disease', 'treatment', 'patient', 'medicine', 'pharmacy', 'clinic',
        'surgery', 'therapy', 'mental health', 'pandemic', 'epidemic'
    ],
    'Politics': [
        'politics', 'political', 'government', 'minister', 'parliament', 
        'election', 'vote', 'democracy', 'party', 'leader', 'president',
        'prime minister', 'opposition', 'coalition', 'policy', 'law'
    ],
    'Crime': [
        'crime', 'criminal', 'police', 'court', 'jail', 'arrest', 'murder', 
        'theft', 'fraud', 'robbery', 'kidnapping', 'terrorism', 'terrorist',
        'bomb', 'attack', 'violence', 'investigation', 'trial', 'sentence'
    ],
    'Education': [
        'education', 'school', 'university', 'student', 'teacher', 'exam', 
        'degree', 'college', 'academic', 'study', 'research', 'scholarship',
        'curriculum', 'institute', 'learning', 'knowledge', 'literacy'
    ],
    'Entertainment': [
        'entertainment', 'movie', 'music', 'celebrity', 'actor', 'singer', 
        'film', 'show', 'drama', 'comedy', 'theater', 'concert', 'festival',
        'award', 'artist', 'performer', 'audience', 'culture', 'arts'
    ],
    'Environment': [
        'environment', 'climate', 'weather', 'pollution', 'green', 'sustainable',
        'renewable', 'energy', 'carbon', 'emission', 'conservation', 'wildlife',
        'forest', 'ocean', 'air quality', 'global warming', 'ecosystem'
    ],
    'Religion': [
        'religion', 'islam', 'muslim', 'christian', 'hindu', 'sikh', 'buddhist',
        'prayer', 'mosque', 'church', 'temple', 'faith', 'spiritual', 'religious',
        'holy', 'sacred', 'worship', 'pilgrimage', 'festival', 'ritual'
    ]
}

# Date parsing formats
DATE_FORMATS = [
    '%d %b, %Y %I:%M%p',
    '%d %B, %Y %I:%M%p',
    '%d %b %Y %I:%M%p',
    '%d %B %Y %I:%M%p',
    '%Y-%m-%d %H:%M:%S',
    '%d/%m/%Y %H:%M',
    '%d-%m-%Y %H:%M',
    '%B %d, %Y',
    '%b %d, %Y',
    '%d %B %Y',
    '%d %b %Y'
]

# Content cleaning patterns
UNWANTED_PATTERNS = [
    r'Published \d+ \w+ \d+',
    r'Updated \d+ \w+ \d+',
    r'Last updated \d+ \w+ \d+',
    r'Follow Dawn\.com on.*',
    r'Read more.*',
    r'Advertisement.*',
    r'Sponsored.*',
    r'Click here.*',
    r'For more.*',
    r'Also read.*',
    r'Related.*',
    r'Tags:.*',
    r'Category:.*'
]

# API response settings
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100
DEFAULT_PAGE = 1

# CORS settings
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://your-frontend-domain.com"
]

# Error messages
ERROR_MESSAGES = {
    'ARTICLE_NOT_FOUND': 'Article not found',
    'INVALID_PAGE': 'Invalid page number',
    'INVALID_PAGE_SIZE': 'Invalid page size',
    'INVALID_CATEGORY': 'Invalid category',
    'INVALID_SEARCH_QUERY': 'Invalid search query',
    'SCRAPING_FAILED': 'Scraping failed',
    'DATABASE_ERROR': 'Database error',
    'INTERNAL_ERROR': 'Internal server error'
}

def get_config() -> Dict[str, Any]:
    """
    Get all configuration settings as a dictionary.
    
    Returns:
        Dictionary containing all configuration settings
    """
    return {
        'database_url': DATABASE_URL,
        'dawn_base_url': DAWN_BASE_URL,
        'dawn_latest_news_url': DAWN_LATEST_NEWS_URL,
        'default_max_articles': DEFAULT_MAX_ARTICLES,
        'scraping_delay': SCRAPING_DELAY,
        'request_timeout': REQUEST_TIMEOUT,
        'api_host': API_HOST,
        'api_port': API_PORT,
        'api_debug': API_DEBUG,
        'scheduler_enabled': SCHEDULER_ENABLED,
        'scheduler_max_articles': SCHEDULER_MAX_ARTICLES,
        'log_level': LOG_LEVEL,
        'log_format': LOG_FORMAT,
        'request_headers': REQUEST_HEADERS,
        'category_keywords': CATEGORY_KEYWORDS,
        'date_formats': DATE_FORMATS,
        'unwanted_patterns': UNWANTED_PATTERNS,
        'default_page_size': DEFAULT_PAGE_SIZE,
        'max_page_size': MAX_PAGE_SIZE,
        'default_page': DEFAULT_PAGE,
        'cors_origins': CORS_ORIGINS,
        'error_messages': ERROR_MESSAGES
    }
