"""
Test script to check DawnScraper methods.
"""

import requests

def test_scraper_methods():
    """Test if the scraper methods are working."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("🔍 Testing Scraper Methods...")
    print("=" * 50)
    
    # Test 1: Check if the method exists by looking at the error
    print("1. Testing scraper/run endpoint...")
    try:
        response = requests.post(f"{base_url}/scraper/run", timeout=60)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Message: {data.get('message')}")
            print(f"   Articles scraped: {data.get('articles_scraped', 0)}")
            print(f"   Articles saved: {data.get('articles_saved', 0)}")
            print("   ✅ Scraper method working!")
        else:
            print(f"   ❌ Scraper failed: {response.text}")
            # Check if it's the method name error
            if "scrape_articles" in response.text:
                print("   🔍 Error: Method name issue - 'scrape_articles' not found")
                print("   💡 This suggests the old code is still deployed")
            elif "scrape_latest_articles" in response.text:
                print("   🔍 Error: Method name issue - 'scrape_latest_articles' not found")
                print("   💡 This suggests a different issue")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: Try the old scrape endpoint
    print("2. Testing old scrape endpoint...")
    try:
        response = requests.post(f"{base_url}/scrape?max_articles=3", timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Message: {data.get('message', 'No message')}")
            print("   ✅ Old scrape endpoint working!")
        else:
            print(f"   ❌ Old scrape failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 50)
    print("Scraper methods test completed!")

if __name__ == "__main__":
    test_scraper_methods()
