"""
Quick test to check if scraper is working.
"""

import requests

def quick_test():
    """Quick test of the scraper."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("🔍 QUICK SCRAPER TEST")
    print("=" * 30)
    
    # Test 1: Run scraper
    print("1. Running scraper...")
    try:
        response = requests.post(f"{base_url}/scraper/run", timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS!")
            print(f"   Articles scraped: {data.get('articles_scraped', 0)}")
            print(f"   Articles saved: {data.get('articles_saved', 0)}")
        else:
            print(f"   ❌ FAILED: {response.text}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    print()
    
    # Test 2: Check articles
    print("2. Checking articles...")
    try:
        response = requests.get(f"{base_url}/articles", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {len(data)} articles")
            if data:
                article = data[0]
                print(f"   Latest: {article.get('title', 'No title')[:50]}...")
        else:
            print(f"   ❌ FAILED: {response.text}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    print()
    print("=" * 30)
    print("✅ SCRAPER IS WORKING!" if response.status_code == 200 else "❌ SCRAPER HAS ISSUES")

if __name__ == "__main__":
    quick_test()
