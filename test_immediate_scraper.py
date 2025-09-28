"""
Test script to run the scraper immediately and check results.
"""

import requests
import time

def test_immediate_scraper():
    """Test the immediate scraper functionality."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("🚀 Testing Immediate Scraper...")
    print("=" * 50)
    
    # Test 1: Run scraper immediately
    print("1. Running scraper immediately...")
    try:
        response = requests.post(f"{base_url}/scraper/run", timeout=60)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Message: {data.get('message')}")
            print(f"   Articles scraped: {data.get('articles_scraped', 0)}")
            print(f"   Status: {data.get('status')}")
            print("   ✅ Scraper completed successfully!")
        else:
            print(f"   ❌ Scraper failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: Check articles in database
    print("2. Checking articles in database...")
    try:
        response = requests.get(f"{base_url}/articles", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data)} articles in database")
            
            if data:
                print("   Recent articles:")
                for i, article in enumerate(data[:3]):  # Show first 3
                    print(f"     {i+1}. {article.get('title', 'No title')[:60]}...")
                    print(f"        Category: {article.get('category')}")
                    print(f"        Scraped: {article.get('scraped_at')}")
            else:
                print("   No articles found in database")
        else:
            print(f"   ❌ Failed to get articles: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 3: Check stats
    print("3. Checking article statistics...")
    try:
        response = requests.get(f"{base_url}/stats", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total articles: {data.get('total_articles', 0)}")
            print(f"   Categories: {list(data.get('categories', {}).keys())}")
        else:
            print(f"   ❌ Failed to get stats: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 50)
    print("Immediate scraper test completed!")
    
    # Summary
    print("\n📊 SUMMARY:")
    print("- If scraper/run works = ✅ Immediate scraping functional")
    print("- If articles are found = ✅ Scraping and database storage working")
    print("- If stats show data = ✅ Full pipeline working")

if __name__ == "__main__":
    test_immediate_scraper()
