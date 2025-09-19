#!/usr/bin/env python3
"""
Test script for SIH 2025 Crop API Usage Tracking
This script demonstrates how to test the usage tracking functionality
"""

import requests
import json
import time
import random

# API base URL (change this to your deployed URL)
BASE_URL = "http://localhost:5000"

def test_api_endpoints():
    """Test all API endpoints to generate usage data."""
    
    print("🧪 Testing SIH 2025 Crop API Usage Tracking...")
    print("=" * 50)
    
    # Test data for crop recommendations
    test_cases = [
        {"N": 90, "P": 42, "K": 43, "temperature": 21, "humidity": 82, "ph": 6.5, "rainfall": 203},
        {"N": 120, "P": 60, "K": 50, "temperature": 25, "humidity": 75, "ph": 6.8, "rainfall": 800},
        {"N": 80, "P": 35, "K": 40, "temperature": 28, "humidity": 85, "ph": 6.2, "rainfall": 1200},
        {"N": 100, "P": 45, "K": 35, "temperature": 22, "humidity": 70, "ph": 7.0, "rainfall": 600},
        {"N": 110, "P": 55, "K": 45, "temperature": 26, "humidity": 80, "ph": 6.5, "rainfall": 900}
    ]
    
    try:
        # 1. Test home endpoint
        print("1. Testing home endpoint...")
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("   ✅ Home endpoint working")
        else:
            print(f"   ❌ Home endpoint failed: {response.status_code}")
        
        # 2. Test health endpoint
        print("2. Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("   ✅ Health endpoint working")
        else:
            print(f"   ❌ Health endpoint failed: {response.status_code}")
        
        # 3. Test crops endpoint
        print("3. Testing crops endpoint...")
        response = requests.get(f"{BASE_URL}/api/crops")
        if response.status_code == 200:
            print("   ✅ Crops endpoint working")
        else:
            print(f"   ❌ Crops endpoint failed: {response.status_code}")
        
        # 4. Test recommendation endpoint with multiple requests
        print("4. Testing recommendation endpoint with sample data...")
        for i, test_data in enumerate(test_cases, 1):
            response = requests.post(
                f"{BASE_URL}/api/recommend",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                crop = result.get('recommendation', {}).get('primary_crop', {}).get('name_english', 'Unknown')
                print(f"   ✅ Test {i}: Recommended {crop}")
            else:
                print(f"   ❌ Test {i} failed: {response.status_code}")
            
            # Small delay between requests
            time.sleep(0.5)
        
        # 5. Test usage statistics endpoint
        print("5. Testing usage statistics...")
        response = requests.get(f"{BASE_URL}/api/usage")
        if response.status_code == 200:
            usage_data = response.json()
            stats = usage_data.get('usage_statistics', {})
            
            print("   ✅ Usage statistics retrieved:")
            print(f"      📊 Total Requests: {stats.get('total_requests', 0)}")
            print(f"      📅 Today's Requests: {stats.get('today_requests', 0)}")
            
            # Show top crops
            top_crops = stats.get('top_recommended_crops', {})
            if top_crops:
                print("      🌾 Top Recommended Crops:")
                for crop, count in list(top_crops.items())[:3]:
                    print(f"         - {crop.title()}: {count} times")
            
            # Show endpoint usage
            endpoint_usage = stats.get('endpoint_usage', {})
            if endpoint_usage:
                print("      🔗 Endpoint Usage:")
                for endpoint, count in endpoint_usage.items():
                    print(f"         - {endpoint}: {count} requests")
        else:
            print(f"   ❌ Usage statistics failed: {response.status_code}")
        
        print("\n" + "=" * 50)
        print("🎉 Usage tracking test completed!")
        print(f"📊 Visit {BASE_URL}/dashboard to see the visual dashboard")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running!")
        print("   Start the server with: python simple_deployment_app.py")
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")

def generate_sample_usage():
    """Generate sample usage data for demonstration."""
    
    print("\n🎲 Generating sample usage data...")
    
    # Sample data for different scenarios
    scenarios = [
        {"name": "Rice Farmer", "N": 90, "P": 42, "K": 43, "temperature": 25, "humidity": 85, "ph": 6.5, "rainfall": 1200},
        {"name": "Wheat Farmer", "N": 65, "P": 40, "K": 35, "temperature": 20, "humidity": 65, "ph": 7.0, "rainfall": 500},
        {"name": "Maize Farmer", "N": 85, "P": 45, "K": 30, "temperature": 23, "humidity": 70, "ph": 6.8, "rainfall": 750},
        {"name": "Cotton Farmer", "N": 120, "P": 55, "K": 50, "temperature": 27, "humidity": 75, "ph": 7.2, "rainfall": 800},
        {"name": "Banana Farmer", "N": 110, "P": 65, "K": 80, "temperature": 29, "humidity": 80, "ph": 6.5, "rainfall": 1500}
    ]
    
    try:
        for scenario in scenarios:
            # Make multiple requests for each scenario
            for _ in range(random.randint(2, 5)):
                # Add some variation to the data
                data = scenario.copy()
                data['N'] += random.randint(-10, 10)
                data['P'] += random.randint(-5, 5)
                data['K'] += random.randint(-5, 5)
                data['temperature'] += random.randint(-2, 2)
                data['humidity'] += random.randint(-5, 5)
                
                response = requests.post(
                    f"{BASE_URL}/api/recommend",
                    json=data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    crop = result.get('recommendation', {}).get('primary_crop', {}).get('name_english', 'Unknown')
                    print(f"   📝 {scenario['name']}: Recommended {crop}")
                
                time.sleep(0.2)  # Small delay
        
        print("✅ Sample usage data generated successfully!")
        
    except Exception as e:
        print(f"❌ Error generating sample data: {str(e)}")

if __name__ == "__main__":
    print("🌾 SIH 2025 Crop API Usage Tracking Test")
    print("=" * 50)
    
    # Test basic functionality
    test_api_endpoints()
    
    # Generate sample usage data
    generate_sample_usage()
    
    print("\n🎯 Next Steps:")
    print("1. Start your API server: python simple_deployment_app.py")
    print("2. Run this test script: python test_usage_tracking.py")
    print("3. Visit http://localhost:5000/dashboard to see usage analytics")
    print("4. Deploy to Render/Heroku for public access")
    print("5. Share your public URL with users!")
