"""
Script to start the scraper and check its status.
"""

import requests
import time

def start_scraper():
    """Start the scraper and check its status."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("🚀 Starting Dawn.com Scraper...")
    print("=" * 50)
    
    # Check current status
    print("1. Checking current scraper status...")
    try:
        response = requests.get(f"{base_url}/scraper/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   Current status: {data.get('status')}")
            print(f"   Scraper running: {data.get('scraper_running')}")
            print(f"   Thread alive: {data.get('scraper_thread_alive')}")
        else:
            print(f"   ❌ Failed to get status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Start the scraper
    print("2. Starting the scraper...")
    try:
        response = requests.post(f"{base_url}/scraper/start", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Message: {data.get('message', 'No message')}")
            print("   ✅ Scraper start command sent")
        else:
            print(f"   ❌ Failed to start scraper: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Wait a moment and check status again
    print("3. Waiting 3 seconds and checking status again...")
    time.sleep(3)
    
    try:
        response = requests.get(f"{base_url}/scraper/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   New status: {data.get('status')}")
            print(f"   Scraper running: {data.get('scraper_running')}")
            print(f"   Thread alive: {data.get('scraper_thread_alive')}")
            
            if data.get('scraper_running'):
                print("   ✅ Scraper is now running!")
            else:
                print("   ❌ Scraper is still not running")
        else:
            print(f"   ❌ Failed to get status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Try to trigger a manual scrape
    print("4. Triggering manual scrape...")
    try:
        response = requests.post(f"{base_url}/scrape?max_articles=3", timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Message: {data.get('message', 'No message')}")
            print("   ✅ Manual scrape triggered")
        else:
            print(f"   ❌ Manual scrape failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 50)
    print("Scraper startup test completed!")

if __name__ == "__main__":
    start_scraper()
