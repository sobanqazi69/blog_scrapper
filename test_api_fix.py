"""
Test script to verify the API datetime serialization fix.
"""

import requests
import json

def test_api_fix():
    """Test the API to ensure datetime serialization works."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("Testing API datetime serialization fix...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print("   ✗ Health check failed")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test 2: Get articles (should work now)
    print("2. Testing articles endpoint...")
    try:
        response = requests.get(f"{base_url}/articles", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   ✓ Articles endpoint works!")
            print(f"   Total articles: {data.get('total_count', 0)}")
            
            # Check if datetime fields are properly serialized
            if data.get('articles'):
                article = data['articles'][0]
                print("   Sample article fields:")
                print(f"     - ID: {article.get('id')}")
                print(f"     - Title: {article.get('title', 'No title')[:50]}...")
                print(f"     - Published Date: {article.get('published_date')}")
                print(f"     - Scraped At: {article.get('scraped_at')}")
                print(f"     - Category: {article.get('category')}")
        else:
            print(f"   ✗ Articles endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test 3: Trigger scraping
    print("3. Testing scraping endpoint...")
    try:
        response = requests.post(f"{base_url}/scrape?max_articles=3", timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   ✓ Scraping endpoint works!")
            print(f"   Response: {data}")
        else:
            print(f"   ✗ Scraping failed: {response.text}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    print("=" * 50)
    print("API fix test completed!")

if __name__ == "__main__":
    test_api_fix()
