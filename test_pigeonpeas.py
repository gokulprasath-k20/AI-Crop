#!/usr/bin/env python3
"""
Test script to verify pigeonpeas prediction with exact values from user's data
"""

import requests
import json

# Your exact values from the image
test_data = {
    "N": 22,
    "P": 62, 
    "K": 16,
    "temperature": 34.64554,
    "humidity": 54.32343,
    "ph": 4.828936,
    "rainfall": 180.901
}

def test_local_api():
    """Test with local API"""
    try:
        print("🧪 Testing Local API...")
        response = requests.post('http://localhost:5000/api/recommend', 
                               json=test_data, 
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Local API Response:")
            print(f"   Primary Crop: {result['recommendation']['primary_crop']['name_english']}")
            print(f"   Hindi Name: {result['recommendation']['primary_crop']['name_hindi']}")
            print(f"   Confidence: {result['confidence']}")
            return True
        else:
            print(f"❌ Local API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Local API Failed: {e}")
        return False

def test_render_api():
    """Test with Render API"""
    try:
        print("\n🌐 Testing Render API...")
        response = requests.post('https://crop-advisor-4lmd.onrender.com/api/recommend', 
                               json=test_data, 
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Render API Response:")
            print(f"   Primary Crop: {result['recommendation']['primary_crop']['name_english']}")
            print(f"   Hindi Name: {result['recommendation']['primary_crop']['name_hindi']}")
            print(f"   Confidence: {result['confidence']}")
            return True
        else:
            print(f"❌ Render API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Render API Failed: {e}")
        return False

if __name__ == "__main__":
    print("🌾 Testing Pigeonpeas Prediction")
    print("=" * 50)
    print("Input Values:")
    for key, value in test_data.items():
        print(f"   {key}: {value}")
    print("=" * 50)
    
    # Test both APIs
    local_success = test_local_api()
    render_success = test_render_api()
    
    print("\n📊 Test Summary:")
    print(f"   Local API: {'✅ PASS' if local_success else '❌ FAIL'}")
    print(f"   Render API: {'✅ PASS' if render_success else '❌ FAIL'}")
    
    if not local_success and not render_success:
        print("\n⚠️  Both APIs failed. Please check if servers are running.")
    elif local_success or render_success:
        print("\n🎯 Expected Result: pigeonpeas (अरहर)")
        print("   If you're getting cotton instead, the algorithm needs improvement.")
