"""
Test script to activate database and check persistence.
"""

import requests
import time

def test_db_activate():
    """Test the database activation endpoint."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("🔧 TESTING DATABASE ACTIVATION")
    print("=" * 50)
    
    # Test 1: Check current database status
    print("1. Checking current database status...")
    try:
        response = requests.get(f"{base_url}/db-info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            db_info = data.get('database_info', {})
            print(f"   Status: {data.get('status')}")
            print(f"   Table exists: {db_info.get('table_exists')}")
            print(f"   Article count: {db_info.get('article_count', 0)}")
            print(f"   Database URL: {db_info.get('database_url')}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: Activate database
    print("2. Activating database...")
    try:
        response = requests.post(f"{base_url}/db-activate", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Current articles: {data.get('current_articles', 0)}")
            
            db_info = data.get('database_info', {})
            print(f"   Table exists: {db_info.get('table_exists')}")
            print(f"   Article count: {db_info.get('article_count', 0)}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 3: Check articles after activation
    print("3. Checking articles after activation...")
    try:
        response = requests.get(f"{base_url}/articles", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data)} articles")
            if data:
                article = data[0]
                print(f"   Latest: {article.get('title', 'No title')[:60]}...")
                print(f"   Category: {article.get('category')}")
                print(f"   Scraped: {article.get('scraped_at')}")
            else:
                print("   No articles found")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 4: Run scraper to add more data
    print("4. Running scraper to test persistence...")
    try:
        response = requests.post(f"{base_url}/scraper/run", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   Scraper result: {data.get('articles_scraped', 0)} scraped, {data.get('articles_saved', 0)} saved")
        else:
            print(f"   ❌ Scraper failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Scraper error: {e}")
    
    print()
    
    # Test 5: Check articles again
    print("5. Checking articles after scraper...")
    try:
        response = requests.get(f"{base_url}/articles", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data)} articles")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 50)
    print("Database activation test completed!")

if __name__ == "__main__":
    test_db_activate()
