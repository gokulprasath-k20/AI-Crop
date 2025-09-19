# Test Your Deployed SIH 2025 API
import requests
import json

# Replace with your actual Render URL
API_BASE_URL = "https://your-app-name.onrender.com"

def test_deployed_api():
    """Test all endpoints of your deployed API."""
    
    print("🧪 TESTING DEPLOYED SIH 2025 API")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health Check: WORKING")
            print(f"   Service: {data['service']}")
            print(f"   Status: {data['status']}")
            print(f"   Supported Crops: {data['supported_crops']}")
        else:
            print(f"❌ Health Check: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Health Check: ERROR - {e}")
    
    # Test 2: Crop Recommendation
    print("\n2. Testing Crop Recommendation...")
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
            f"{API_BASE_URL}/api/recommend",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Crop Recommendation: WORKING")
            
            if result['status'] == 'success':
                crop = result['recommendation']['primary_crop']
                print(f"   Recommended: {crop['name_english']} ({crop['name_hindi']})")
                print(f"   Yield: {crop['predicted_yield_kg_per_ha']:,.0f} kg/ha")
                print(f"   Sustainability: {crop['sustainability_score']}/10")
                print(f"   Confidence: {crop['confidence']:.3f}")
                
                # Show alternatives
                alternatives = result['recommendation']['alternative_crops']
                print(f"   Alternatives: {len(alternatives)} crops")
                for i, alt in enumerate(alternatives[:2], 1):
                    print(f"     {i}. {alt['name_english']} ({alt['name_hindi']})")
            else:
                print(f"   Error: {result['message']}")
        else:
            print(f"❌ Crop Recommendation: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Crop Recommendation: ERROR - {e}")
    
    # Test 3: Crops List
    print("\n3. Testing Crops List...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/crops")
        if response.status_code == 200:
            data = response.json()
            print("✅ Crops List: WORKING")
            print(f"   Total Crops: {data['total_crops']}")
            print("   Available Crops:")
            for crop in data['crops'][:3]:
                print(f"     • {crop['english']} ({crop['hindi']}) - {crop['base_yield']} kg/ha")
        else:
            print(f"❌ Crops List: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Crops List: ERROR - {e}")
    
    print(f"\n🎉 API TESTING COMPLETED!")
    print(f"🌐 Your API URL: {API_BASE_URL}")
    print("📱 Ready for mobile app integration!")

def demo_farmer_usage():
    """Demonstrate how a farmer would use the API."""
    
    print("\n🌾 FARMER USAGE DEMO")
    print("=" * 30)
    
    # Sample farmer data from Jharkhand
    farmer_data = {
        "N": 85,      # Nitrogen from soil test
        "P": 45,      # Phosphorus from soil test  
        "K": 40,      # Potassium from soil test
        "temperature": 22,  # Average temperature in °C
        "humidity": 78,     # Relative humidity %
        "ph": 6.2,          # Soil pH
        "rainfall": 180     # Expected rainfall in mm
    }
    
    print("👨‍🌾 Farmer Input:")
    print(f"   Nitrogen: {farmer_data['N']} kg/ha")
    print(f"   Phosphorus: {farmer_data['P']} kg/ha")
    print(f"   Potassium: {farmer_data['K']} kg/ha")
    print(f"   Temperature: {farmer_data['temperature']}°C")
    print(f"   Humidity: {farmer_data['humidity']}%")
    print(f"   Soil pH: {farmer_data['ph']}")
    print(f"   Rainfall: {farmer_data['rainfall']}mm")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/recommend",
            json=farmer_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                crop = result['recommendation']['primary_crop']
                
                print(f"\n🎯 AI Recommendation:")
                print(f"   Best Crop: {crop['name_hindi']} ({crop['name_english']})")
                print(f"   Expected Harvest: {crop['predicted_yield_kg_per_ha']:,.0f} kg/hectare")
                print(f"   Sustainability Rating: {crop['sustainability_score']}/10")
                print(f"   Confidence Level: {crop['confidence']*100:.1f}%")
                
                print(f"\n🔄 Alternative Options:")
                for i, alt in enumerate(result['recommendation']['alternative_crops'][:2], 1):
                    print(f"   {i}. {alt['name_hindi']} ({alt['name_english']}) - {alt['predicted_yield_kg_per_ha']:,.0f} kg/ha")
                
                print(f"\n✅ Recommendation Complete!")
                print(f"💡 This helps the farmer choose the best crop for maximum yield and sustainability!")
                
    except Exception as e:
        print(f"❌ Demo Error: {e}")

if __name__ == "__main__":
    # Update this with your actual Render URL
    print("🔗 UPDATE API_BASE_URL with your actual Render URL!")
    print("   Example: https://sih2025-crop-api.onrender.com")
    
    test_deployed_api()
    demo_farmer_usage()
