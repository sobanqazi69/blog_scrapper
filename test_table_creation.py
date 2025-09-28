"""
Test script to verify table creation fix works.
"""

import requests
import time

def test_table_creation():
    """Test if the table creation fix works."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("🔧 Testing Table Creation Fix...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Health check passed")
        else:
            print(f"   ❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: Articles endpoint (this was failing with "no such table: articles")
    print("2. Testing articles endpoint...")
    try:
        response = requests.get(f"{base_url}/articles", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Articles endpoint works!")
            print(f"   Found {len(data)} articles")
            
            if data:
                print("   Sample article:")
                article = data[0]
                print(f"     - Title: {article.get('title', 'No title')[:50]}...")
                print(f"     - Category: {article.get('category')}")
                print(f"     - Scraped At: {article.get('scraped_at')}")
        else:
            print(f"   ❌ Articles endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 3: Stats endpoint
    print("3. Testing stats endpoint...")
    try:
        response = requests.get(f"{base_url}/stats", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Stats endpoint works!")
            print(f"   Total articles: {data.get('total_articles', 0)}")
            print(f"   Categories: {list(data.get('categories', {}).keys())}")
        else:
            print(f"   ❌ Stats endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 4: Trigger scraping to test database write
    print("4. Testing scraping (database write)...")
    try:
        response = requests.post(f"{base_url}/scrape?max_articles=3", timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Scraping endpoint works!")
            print(f"   Message: {data.get('message', 'No message')}")
        else:
            print(f"   ❌ Scraping failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 50)
    print("Table creation fix test completed!")
    
    # Summary
    print("\n📊 SUMMARY:")
    print("- If all endpoints return 200 = ✅ Table creation fix successful")
    print("- If articles endpoint works = ✅ 'no such table: articles' error fixed")
    print("- If scraping works = ✅ Database write operations work")
    print("- If you see articles = ✅ Database is fully functional")

if __name__ == "__main__":
    test_table_creation()
