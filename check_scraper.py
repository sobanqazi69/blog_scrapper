"""
Script to check if the continuous scraper is working.
"""

import requests
import time
import json

def check_scraper_status():
    """Check if the background scraper is running."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("🔍 Checking Dawn.com Scraper Status...")
    print("=" * 50)
    
    # Check 1: Scraper status
    print("1. Checking scraper status...")
    try:
        response = requests.get(f"{base_url}/scraper/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Scraper Status: {data.get('status')}")
            print(f"   ✓ Running: {data.get('scraper_running')}")
            print(f"   ✓ Thread Alive: {data.get('scraper_thread_alive')}")
        else:
            print(f"   ✗ Status check failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Check 2: Current article count
    print("2. Checking current article count...")
    try:
        response = requests.get(f"{base_url}/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            total_articles = data.get('total_articles', 0)
            print(f"   ✓ Total Articles: {total_articles}")
            
            if total_articles > 0:
                print("   ✓ Database has articles - scraper has been working!")
                categories = data.get('categories', {})
                print(f"   ✓ Categories: {list(categories.keys())}")
            else:
                print("   ⚠ No articles yet - scraper may be starting up")
        else:
            print(f"   ✗ Stats check failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Check 3: Recent articles
    print("3. Checking recent articles...")
    try:
        response = requests.get(f"{base_url}/articles", timeout=10)
        if response.status_code == 200:
            articles = response.json()
            print(f"   ✓ Found {len(articles)} articles")
            
            if articles:
                latest = articles[0]
                print(f"   ✓ Latest Article: {latest.get('title', 'No title')[:50]}...")
                print(f"   ✓ Scraped At: {latest.get('scraped_at')}")
                print(f"   ✓ Category: {latest.get('category')}")
            else:
                print("   ⚠ No articles found")
        else:
            print(f"   ✗ Articles check failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    print("=" * 50)
    
    # Summary
    print("📊 SUMMARY:")
    print("- If scraper status shows 'running' = ✅ Continuous scraping is ON")
    print("- If you see articles in the database = ✅ Scraper has been working")
    print("- If no articles yet = ⚠ Scraper may be starting up (wait 1 hour)")
    print("- Check again in 1 hour to see if new articles appear")

def monitor_scraper():
    """Monitor scraper for 10 minutes to see if it's working."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("🔄 Monitoring scraper for 10 minutes...")
    print("=" * 50)
    
    initial_count = 0
    initial_time = None
    
    # Get initial count
    try:
        response = requests.get(f"{base_url}/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            initial_count = data.get('total_articles', 0)
            initial_time = data.get('last_updated')
            print(f"Initial article count: {initial_count}")
            print(f"Last updated: {initial_time}")
    except:
        print("Could not get initial count")
    
    # Monitor for 10 minutes
    for i in range(10):
        print(f"\nMinute {i+1}/10:")
        
        try:
            response = requests.get(f"{base_url}/stats", timeout=10)
            if response.status_code == 200:
                data = response.json()
                current_count = data.get('total_articles', 0)
                current_time = data.get('last_updated')
                print(f"  Current articles: {current_count}")
                print(f"  Last updated: {current_time}")
                
                if current_count > initial_count:
                    print(f"  🎉 NEW ARTICLES FOUND! (+{current_count - initial_count})")
                    print(f"  📈 Scraper is working! Found {current_count - initial_count} new articles")
                    return True
                else:
                    print("  No new articles yet...")
            else:
                print("  Could not check stats")
        except Exception as e:
            print(f"  Error: {e}")
        
        if i < 9:  # Don't wait after the last check
            time.sleep(60)  # Wait 1 minute
    
    print("\n⏰ 10 minutes completed. No new articles detected.")
    print("This could mean:")
    print("- Scraper is not running")
    print("- No new articles on Dawn.com in the last 10 minutes")
    print("- Scraper checks every 3-5 minutes, so wait a bit longer")
    print("- Check the scraper status to see if it's running")
    
    return False

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Check scraper status")
    print("2. Monitor scraper for 5 minutes")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        check_scraper_status()
    elif choice == "2":
        monitor_scraper()
    else:
        print("Invalid choice. Running status check...")
        check_scraper_status()
