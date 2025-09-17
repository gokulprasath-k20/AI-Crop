# Quick API Test
import requests
import time

def quick_test():
    print("🧪 Quick API Test")
    print("=" * 30)
    
    try:
        # Test home page
        response = requests.get("http://localhost:5000", timeout=3)
        print(f"Home page status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Working: {data['message']}")
            print(f"Supported crops: {data['supported_crops']}")
        else:
            print(f"❌ Status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - server may not be running")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    time.sleep(2)  # Wait for server
    quick_test()
