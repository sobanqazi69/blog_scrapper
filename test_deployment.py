"""
Test script to verify Vercel deployment.
Run this after deploying to test all endpoints.
"""

import requests
import json
import time

def test_deployment(base_url):
    """Test all API endpoints on the deployed application."""
    
    print(f"Testing deployment at: {base_url}")
    print("=" * 50)
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Health check error: {e}")
    
    print()
    
    # Test 2: Get Articles (should be empty initially)
    print("2. Testing Get Articles...")
    try:
        response = requests.get(f"{base_url}/articles", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✓ Get articles passed")
            print(f"  Total articles: {data.get('total_count', 0)}")
        else:
            print(f"✗ Get articles failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Get articles error: {e}")
    
    print()
    
    # Test 3: Trigger Scraping
    print("3. Testing Scraping...")
    try:
        response = requests.post(f"{base_url}/scrape?max_articles=3", timeout=60)
        if response.status_code == 200:
            print("✓ Scraping triggered successfully")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Scraping failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Scraping error: {e}")
    
    print()
    
    # Wait a bit for scraping to complete
    print("Waiting 30 seconds for scraping to complete...")
    time.sleep(30)
    
    # Test 4: Check if articles were scraped
    print("4. Checking scraped articles...")
    try:
        response = requests.get(f"{base_url}/articles", timeout=10)
        if response.status_code == 200:
            data = response.json()
            article_count = data.get('total_count', 0)
            print(f"✓ Found {article_count} articles")
            
            if article_count > 0:
                print("  Sample articles:")
                for article in data.get('articles', [])[:3]:
                    print(f"    - {article.get('title', 'No title')[:50]}...")
                    print(f"      Category: {article.get('category', 'Unknown')}")
            else:
                print("  No articles found yet")
        else:
            print(f"✗ Failed to get articles: {response.status_code}")
    except Exception as e:
        print(f"✗ Error getting articles: {e}")
    
    print()
    
    # Test 5: Get Statistics
    print("5. Testing Statistics...")
    try:
        response = requests.get(f"{base_url}/stats", timeout=10)
        if response.status_code == 200:
            print("✓ Statistics retrieved")
            stats = response.json()
            print(f"  Total articles: {stats.get('total_articles', 0)}")
            print(f"  Categories: {list(stats.get('categories', {}).keys())}")
        else:
            print(f"✗ Statistics failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Statistics error: {e}")
    
    print()
    print("=" * 50)
    print("Deployment test completed!")

if __name__ == "__main__":
    # Replace with your actual Vercel URL
    vercel_url = input("Enter your Vercel deployment URL (e.g., https://your-app.vercel.app): ").strip()
    
    if not vercel_url:
        print("Please provide a valid URL")
        exit(1)
    
    if not vercel_url.startswith("http"):
        vercel_url = f"https://{vercel_url}"
    
    test_deployment(vercel_url)
