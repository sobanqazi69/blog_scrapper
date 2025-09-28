"""
Test script to verify the database table creation fix.
"""

import requests
import time

def test_database_fix():
    """Test if the database table creation fix works."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("🔧 Testing Database Table Creation Fix...")
    print("=" * 60)
    
    # Test 1: Database test endpoint
    print("1. Testing database connection...")
    try:
        response = requests.get(f"{base_url}/db-test", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Table exists: {data.get('table_exists')}")
            print(f"   Articles count: {data.get('articles_count', 0)}")
            
            if data.get('status') == 'success':
                print("   ✅ Database connection working!")
            else:
                print("   ❌ Database connection failed")
        else:
            print(f"   ❌ Request failed: {response.text}")
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
    
    # Test 3: Health check
    print("3. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Health check passed")
            print(f"   Service: {data.get('service')}")
        else:
            print(f"   ❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 60)
    print("Database table creation fix test completed!")
    
    # Summary
    print("\n📊 SUMMARY:")
    print("- If db-test shows 'success' = ✅ Table creation fix working")
    print("- If articles endpoint works = ✅ 'no such table: articles' error fixed")
    print("- If all endpoints return 200 = ✅ Database fully functional")

if __name__ == "__main__":
    test_database_fix()
