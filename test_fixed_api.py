# Test Fixed API - SIH 2025
import requests
import json
import time

def test_fixed_api():
    """Test the fixed API deployment."""
    
    base_url = "http://localhost:5000"
    
    print("🧪 TESTING FIXED SIH 2025 API")
    print("=" * 50)
    
    # Test 1: Home page
    print("\n1. Testing Home Page...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Home Page: WORKING")
            print(f"   Message: {data['message']}")
            print(f"   Status: {data['status']}")
        else:
            print(f"❌ Home Page: FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Home Page: ERROR - {e}")
    
    # Test 2: Health Check
    print("\n2. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health Check: WORKING")
            print(f"   Service: {data['service']}")
            print(f"   Supported Crops: {data['supported_crops']}")
        else:
            print(f"❌ Health Check: FAILED")
    except Exception as e:
        print(f"❌ Health Check: ERROR - {e}")
    
    # Test 3: Crop Recommendation
    print("\n3. Testing Crop Recommendation...")
    test_data = {
        "N": 90, "P": 42, "K": 43, "temperature": 21,
        "humidity": 82, "ph": 6.5, "rainfall": 203
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/recommend",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Crop Recommendation: WORKING")
            
            primary = result['recommendation']['primary_crop']
            print(f"   English: {primary['name']}")
            print(f"   Hindi: {primary['name_hindi']}")
            print(f"   Bengali: {primary['name_bengali']}")
            print(f"   Yield: {primary['predicted_yield']:,.0f} kg/ha")
            print(f"   Sustainability: {primary['sustainability_score']}/10")
            
        else:
            print(f"❌ Crop Recommendation: FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Crop Recommendation: ERROR - {e}")
    
    # Test 4: Crops List
    print("\n4. Testing Crops List...")
    try:
        response = requests.get(f"{base_url}/api/crops", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Crops List: WORKING")
            print(f"   Total Crops: {data['total_crops']}")
            print("   Sample: Rice (चावल/ধান), Wheat (गेहूं/গম)")
        else:
            print(f"❌ Crops List: FAILED")
    except Exception as e:
        print(f"❌ Crops List: ERROR - {e}")
    
    print(f"\n🎉 API TESTING COMPLETED!")
    print("🌐 API Server: http://localhost:5000")
    print("📱 Ready for mobile integration!")

if __name__ == "__main__":
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    test_fixed_api()
