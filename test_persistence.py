"""
Test script to check database persistence issue.
"""

import requests
import time

def test_persistence():
    """Test database persistence across multiple requests."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("🔍 TESTING DATABASE PERSISTENCE")
    print("=" * 50)
    
    # Test 1: Check database info
    print("1. Checking database info...")
    try:
        response = requests.get(f"{base_url}/db-info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            db_info = data.get('database_info', {})
            print(f"   Database URL: {db_info.get('database_url')}")
            print(f"   Table exists: {db_info.get('table_exists')}")
            print(f"   Article count: {db_info.get('article_count', 0)}")
            if db_info.get('error'):
                print(f"   Error: {db_info.get('error')}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: Check articles multiple times
    print("2. Checking articles persistence (3 times)...")
    for i in range(3):
        try:
            response = requests.get(f"{base_url}/articles", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"   Attempt {i+1}: Found {len(data)} articles")
                if data:
                    article = data[0]
                    print(f"      Latest: {article.get('title', 'No title')[:50]}...")
            else:
                print(f"   Attempt {i+1}: Failed - {response.status_code}")
        except Exception as e:
            print(f"   Attempt {i+1}: Error - {e}")
        
        time.sleep(2)  # Wait 2 seconds between requests
    
    print()
    
    # Test 3: Run scraper and check persistence
    print("3. Running scraper and checking persistence...")
    try:
        # Run scraper
        response = requests.post(f"{base_url}/scraper/run", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   Scraper result: {data.get('articles_scraped', 0)} scraped, {data.get('articles_saved', 0)} saved")
        else:
            print(f"   Scraper failed: {response.status_code}")
    except Exception as e:
        print(f"   Scraper error: {e}")
    
    # Wait and check again
    time.sleep(3)
    try:
        response = requests.get(f"{base_url}/articles", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   After scraper: Found {len(data)} articles")
        else:
            print(f"   After scraper: Failed - {response.status_code}")
    except Exception as e:
        print(f"   After scraper: Error - {e}")
    
    print()
    print("=" * 50)
    print("Persistence test completed!")

if __name__ == "__main__":
    test_persistence()
