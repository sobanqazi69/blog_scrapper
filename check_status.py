"""
Check scraper status.
"""

import requests

def check_status():
    """Check the current scraper status."""
    
    base_url = "https://blog-scrapper-teal.vercel.app"
    
    print("📊 SCRAPER STATUS CHECK")
    print("=" * 30)
    
    try:
        response = requests.get(f"{base_url}/scraper/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Running: {data.get('scraper_running')}")
            print(f"Thread Alive: {data.get('scraper_thread_alive')}")
            print(f"Timestamp: {data.get('timestamp')}")
            
            if data.get('scraper_running'):
                print("✅ Scraper is RUNNING")
            else:
                print("⏸️ Scraper is STOPPED")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Also check articles count
    try:
        response = requests.get(f"{base_url}/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"📈 STATISTICS:")
            print(f"Total Articles: {data.get('total_articles', 0)}")
            print(f"Categories: {list(data.get('categories', {}).keys())}")
        else:
            print(f"❌ Stats Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Stats Error: {e}")

if __name__ == "__main__":
    check_status()
