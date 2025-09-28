"""
Script to fix database issues and test article fetching.
"""

import requests
import time

def fix_database():
    """Fix database and test article fetching."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("🔧 FIXING DATABASE ISSUES")
    print("=" * 50)
    
    # Step 1: Check current status
    print("1. Checking current database status...")
    try:
        response = requests.get(f"{base_url}/db-info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            db_info = data.get('database_info', {})
            print(f"   Status: {data.get('status')}")
            print(f"   Table exists: {db_info.get('table_exists')}")
            print(f"   Article count: {db_info.get('article_count', 0)}")
            if db_info.get('error'):
                print(f"   Error: {db_info.get('error')}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Step 2: Fix database completely
    print("2. Fixing database completely...")
    try:
        response = requests.post(f"{base_url}/db-fix", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Current articles: {data.get('current_articles', 0)}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Step 3: Run scraper to add data
    print("3. Running scraper to add data...")
    try:
        response = requests.post(f"{base_url}/scraper/run", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Articles scraped: {data.get('articles_scraped', 0)}")
            print(f"   Articles saved: {data.get('articles_saved', 0)}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Step 4: Check articles
    print("4. Checking articles after fix...")
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
    
    # Step 5: Check database info again
    print("5. Checking database info after fix...")
    try:
        response = requests.get(f"{base_url}/db-info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            db_info = data.get('database_info', {})
            print(f"   Status: {data.get('status')}")
            print(f"   Table exists: {db_info.get('table_exists')}")
            print(f"   Article count: {db_info.get('article_count', 0)}")
            if db_info.get('error'):
                print(f"   Error: {db_info.get('error')}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 50)
    print("Database fix completed!")

if __name__ == "__main__":
    fix_database()
