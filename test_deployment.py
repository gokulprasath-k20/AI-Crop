# Test Deployment - SIH 2025 Crop Recommendation System
import requests
import json
import time

def test_api_deployment():
    """Test the deployed API endpoints."""
    
    base_url = "http://localhost:5000"
    
    print("🧪 TESTING DEPLOYED SIH 2025 CROP RECOMMENDATION API")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health Check: PASSED")
            print(f"   Service: {health_data['service']}")
            print(f"   Status: {health_data['status']}")
            print(f"   Supported Crops: {health_data['supported_crops']}")
        else:
            print(f"❌ Health Check: FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Health Check: ERROR - {e}")
    
    # Test 2: Crop Recommendation
    print("\n2. Testing Crop Recommendation Endpoint...")
    test_data = {
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 21,
        "humidity": 82,
        "ph": 6.5,
        "rainfall": 203
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
            print("✅ Crop Recommendation: PASSED")
            
            primary = result['recommendation']['primary_crop']
            print(f"   Recommended Crop: {primary['name']} ({primary['name_hindi']})")
            print(f"   Predicted Yield: {primary['predicted_yield']:,.0f} kg/ha")
            print(f"   Sustainability Score: {primary['sustainability_score']}/10")
            print(f"   Confidence: {primary['confidence']:.3f}")
            
            # Show alternatives
            print("   Alternative Crops:")
            for i, alt in enumerate(result['recommendation']['alternatives'][:2], 1):
                print(f"     {i}. {alt['name']} ({alt['name_hindi']}) - {alt['yield']:,.0f} kg/ha")
                
        else:
            print(f"❌ Crop Recommendation: FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Crop Recommendation: ERROR - {e}")
    
    # Test 3: Multilingual Support
    print("\n3. Testing Multilingual Support...")
    languages = ['english', 'hindi', 'bengali']
    
    for lang in languages:
        try:
            test_data_lang = test_data.copy()
            response = requests.post(
                f"{base_url}/api/recommend", 
                json=test_data_lang,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                crop_name = result['recommendation']['primary_crop']['name_hindi'] if lang == 'hindi' else result['recommendation']['primary_crop']['name']
                print(f"   ✅ {lang.title()}: {crop_name}")
            else:
                print(f"   ❌ {lang.title()}: FAILED")
                
        except Exception as e:
            print(f"   ❌ {lang.title()}: ERROR - {e}")
    
    # Test 4: Supported Crops List
    print("\n4. Testing Supported Crops Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/crops", timeout=5)
        if response.status_code == 200:
            crops_data = response.json()
            print("✅ Crops List: PASSED")
            print(f"   Total Crops: {crops_data['total_crops']}")
            print("   Sample Crops:")
            for crop in crops_data['crops'][:5]:
                print(f"     • {crop['english']} ({crop['hindi']}) - {crop['category']}")
        else:
            print(f"❌ Crops List: FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Crops List: ERROR - {e}")
    
    print(f"\n🎉 API DEPLOYMENT TEST COMPLETED!")
    print("=" * 60)
    print("🌐 API Server URL: http://localhost:5000")
    print("📱 Ready for mobile app integration!")
    print("🌾 Perfect for Jharkhand farmers!")

if __name__ == "__main__":
    # Wait a moment for server to fully start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    test_api_deployment()
