"""
Test script for the simplified API.
"""

import requests
import json

def test_simple_api():
    """Test the simplified API."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("Testing Simplified API...")
    print("=" * 50)
    
    # Test 1: Root endpoint
    print("1. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   ✓ Root endpoint works!")
            print(f"   Message: {data.get('message')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Status: {data.get('status')}")
        else:
            print(f"   ✗ Root endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test 2: Health check
    print("2. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   ✓ Health check works!")
            print(f"   Status: {data.get('status')}")
            print(f"   Service: {data.get('service')}")
        else:
            print(f"   ✗ Health check failed: {response.text}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test 3: Get articles
    print("3. Testing articles endpoint...")
    try:
        response = requests.get(f"{base_url}/articles", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   ✓ Articles endpoint works!")
            print(f"   Number of articles: {len(data)}")
            
            if data:
                article = data[0]
                print("   Sample article:")
                print(f"     - ID: {article.get('id')}")
                print(f"     - Title: {article.get('title')}")
                print(f"     - Category: {article.get('category')}")
                print(f"     - Published: {article.get('published_date')}")
        else:
            print(f"   ✗ Articles endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test 4: Get specific article
    print("4. Testing specific article endpoint...")
    try:
        response = requests.get(f"{base_url}/articles/1", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   ✓ Specific article endpoint works!")
            print(f"   Title: {data.get('title')}")
            print(f"   Category: {data.get('category')}")
        else:
            print(f"   ✗ Specific article endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test 5: Scraping endpoint
    print("5. Testing scraping endpoint...")
    try:
        response = requests.post(f"{base_url}/scrape?max_articles=3", timeout=15)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   ✓ Scraping endpoint works!")
            print(f"   Message: {data.get('message')}")
            print(f"   Total scraped: {data.get('total_scraped')}")
        else:
            print(f"   ✗ Scraping endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test 6: Stats endpoint
    print("6. Testing stats endpoint...")
    try:
        response = requests.get(f"{base_url}/stats", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("   ✓ Stats endpoint works!")
            print(f"   Total articles: {data.get('total_articles')}")
            print(f"   Categories: {data.get('categories')}")
        else:
            print(f"   ✗ Stats endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    print("=" * 50)
    print("Simplified API test completed!")

if __name__ == "__main__":
    test_simple_api()
