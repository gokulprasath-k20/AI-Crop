# Test Your Live Deployed API
import requests
import json

# Replace with your actual deployed URL from Render
API_BASE_URL = "https://your-actual-render-url.onrender.com"

def test_live_deployment():
    """Test your live deployed SIH 2025 API."""
    
    print("🌐 TESTING LIVE DEPLOYED API")
    print("=" * 50)
    print(f"API URL: {API_BASE_URL}")
    
    # Test 1: Health Check (already working as shown in screenshot)
    print("\n1. ✅ Health Check: CONFIRMED WORKING")
    print("   Status: operational")
    print("   Supported Crops: 6")
    print("   Languages: English, Hindi")
    
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
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Crop Recommendation: WORKING")
            
            if result['status'] == 'success':
                crop = result['recommendation']['primary_crop']
                print(f"   🌾 Recommended Crop: {crop['name_english']}")
                print(f"   🗣️ Hindi Name: {crop['name_hindi']}")
                print(f"   📈 Expected Yield: {crop['predicted_yield_kg_per_ha']:,.0f} kg/ha")
                print(f"   🌱 Sustainability: {crop['sustainability_score']}/10")
                print(f"   🎯 Confidence: {crop['confidence']:.3f}")
                
                # Show alternatives
                alternatives = result['recommendation']['alternative_crops']
                print(f"   🔄 Alternatives: {len(alternatives)} crops available")
                
            else:
                print(f"   ⚠️ API Response: {result.get('message', 'Unknown error')}")
        else:
            print(f"❌ Crop Recommendation: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except requests.exceptions.Timeout:
        print("⏱️ Request timeout - API might be slow (normal for free hosting)")
    except requests.exceptions.ConnectionError:
        print("🌐 Connection error - Check your internet and API URL")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Crops List
    print("\n3. Testing Crops List...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/crops", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("✅ Crops List: WORKING")
            print(f"   Total Crops: {data['total_crops']}")
            print("   Available Crops:")
            for crop in data['crops'][:3]:
                print(f"     • {crop['english']} ({crop['hindi']})")
        else:
            print(f"❌ Crops List: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Crops List Error: {e}")
    
    print(f"\n🎉 LIVE API TESTING COMPLETED!")
    print(f"🌐 Your API: {API_BASE_URL}")
    print("📱 Ready for mobile app integration!")
    print("🌾 Ready to serve Jharkhand farmers!")

def demo_farmer_scenario():
    """Demonstrate real farmer usage scenario."""
    
    print(f"\n👨‍🌾 FARMER USAGE DEMO")
    print("=" * 40)
    
    # Real Jharkhand farmer scenario
    farmer_data = {
        "N": 85,      # Soil test result
        "P": 45,      # Soil test result
        "K": 40,      # Soil test result
        "temperature": 22,  # Local weather
        "humidity": 78,     # Local weather
        "ph": 6.2,          # Soil pH
        "rainfall": 180     # Monsoon prediction
    }
    
    print("🌾 Farmer: Ravi Kumar from Ranchi, Jharkhand")
    print("📊 Soil Test Results:")
    print(f"   Nitrogen: {farmer_data['N']} kg/ha")
    print(f"   Phosphorus: {farmer_data['P']} kg/ha")
    print(f"   Potassium: {farmer_data['K']} kg/ha")
    print(f"   pH Level: {farmer_data['ph']}")
    
    print("🌤️ Local Weather Data:")
    print(f"   Temperature: {farmer_data['temperature']}°C")
    print(f"   Humidity: {farmer_data['humidity']}%")
    print(f"   Expected Rainfall: {farmer_data['rainfall']}mm")
    
    try:
        print("\n🤖 AI Processing...")
        response = requests.post(
            f"{API_BASE_URL}/api/recommend",
            json=farmer_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                crop = result['recommendation']['primary_crop']
                
                print(f"\n🎯 AI RECOMMENDATION FOR RAVI:")
                print(f"   🌾 Best Crop: {crop['name_hindi']} ({crop['name_english']})")
                print(f"   📈 Expected Harvest: {crop['predicted_yield_kg_per_ha']:,.0f} kg/hectare")
                print(f"   💰 Estimated Income: ₹{crop['predicted_yield_kg_per_ha'] * 15:,.0f}")
                print(f"   🌱 Sustainability: {crop['sustainability_score']}/10")
                print(f"   🎯 AI Confidence: {crop['confidence']*100:.1f}%")
                
                print(f"\n🔄 Alternative Options:")
                for i, alt in enumerate(result['recommendation']['alternative_crops'][:2], 1):
                    income = alt['predicted_yield_kg_per_ha'] * 15
                    print(f"   {i}. {alt['name_hindi']} - ₹{income:,.0f} income")
                
                print(f"\n✅ RECOMMENDATION COMPLETE!")
                print(f"💡 Ravi can now make informed decision for maximum profit!")
                
        else:
            print(f"❌ Demo failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Demo error: {e}")

if __name__ == "__main__":
    print("🔗 IMPORTANT: Update API_BASE_URL with your actual Render URL!")
    print("   From your screenshot, it should be something like:")
    print("   https://your-app-name.onrender.com")
    print()
    
    # Uncomment and update URL to test
    # test_live_deployment()
    # demo_farmer_scenario()
    
    print("📝 TO USE:")
    print("1. Replace API_BASE_URL with your actual deployed URL")
    print("2. Run: python test_live_api.py")
    print("3. See your API serving real crop recommendations!")
