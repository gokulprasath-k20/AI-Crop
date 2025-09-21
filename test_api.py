#!/usr/bin/env python3
# Test script to check API response

from mobile_app_backend import app
import json

def test_api():
    with app.test_client() as client:
        # Test data
        test_data = {
            'N': 90, 'P': 42, 'K': 43, 
            'temperature': 21, 'humidity': 82, 
            'ph': 6.5, 'rainfall': 203
        }
        
        print("🌾 API Test Results:")
        print("=" * 60)
        
        # Make API call
        response = client.post('/api/recommend', json=test_data)
        data = response.get_json()
        
        # Print results
        print(f"Status: {data['status']}")
        print(f"Primary crop: {data['recommendation']['primary_crop']['name']}")
        print(f"Number of alternatives: {len(data['recommendation']['alternatives'])}")
        print(f"Total crops supported: {data['system_info']['total_crops_supported']}")
        
        print("\n🏆 PRIMARY RECOMMENDATION:")
        primary = data['recommendation']['primary_crop']
        print(f"   🌾 Crop: {primary['name']} ({primary['name_hindi']})")
        print(f"   📈 Yield: {primary['predicted_yield']:.0f} kg/ha")
        print(f"   🌱 Sustainability: {primary['sustainability_score']}/10")
        
        print("\n🔄 ALTERNATIVE CROPS:")
        for i, alt in enumerate(data['recommendation']['alternatives'], 1):
            print(f"   {i}. {alt['name']} ({alt['name_hindi']}) - {alt['yield']:.0f} kg/ha")
        
        print("\n" + "=" * 60)
        
        # Test crops endpoint
        print("📋 Testing /api/crops endpoint...")
        crops_response = client.get('/api/crops')
        crops_data = crops_response.get_json()
        print(f"✅ Crops endpoint returns: {crops_data['total_crops']} crops")
        
        print("\n🌾 All supported crops:")
        for i, crop in enumerate(crops_data['crops'], 1):
            print(f"   {i:2d}. {crop['english']} ({crop['hindi']}) - {crop['category']}")

if __name__ == "__main__":
    test_api()
