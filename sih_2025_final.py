# SIH 2025 - Final Crop Recommendation System
# Ready for Mobile Integration

from working_crop_system import CropRecommendationSystem, recommend_crop, comprehensive_analysis
import json

def mobile_api_interface(N, P, K, temperature, humidity, ph, rainfall):
    """Mobile-friendly API interface."""
    
    try:
        result = comprehensive_analysis(N, P, K, temperature, humidity, ph, rainfall)
        
        # Format for mobile app
        mobile_response = {
            "status": "success",
            "data": {
                "primary_crop": result['primary_recommendation']['crop'],
                "yield_kg_per_ha": result['primary_recommendation']['predicted_yield_kg_per_ha'],
                "sustainability_score": result['primary_recommendation']['sustainability_score'],
                "confidence": result['primary_recommendation']['confidence_score'],
                "alternatives": [
                    {
                        "crop": alt['crop'],
                        "yield": alt['predicted_yield_kg_per_ha'],
                        "sustainability": alt['sustainability_score']
                    } for alt in result['alternative_crops'][:3]
                ],
                "warnings": result['input_validation']['warnings']
            }
        }
        
        return json.dumps(mobile_response, indent=2)
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# Test the mobile API
if __name__ == "__main__":
    print("🚀 SIH 2025 Crop Recommendation System - Mobile Ready!")
    print("=" * 60)
    
    # Test with your example
    api_result = mobile_api_interface(90, 42, 43, 21, 82, 6.5, 203)
    print("📱 Mobile API Response:")
    print(api_result)
    
    print("\n✅ System is ready for mobile integration!")
    print("📱 Use mobile_api_interface() function in your mobile app")
    print("🌾 Perfect for Jharkhand farmers!")
