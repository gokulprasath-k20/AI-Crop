from working_crop_system import CropRecommendationSystem

def test_pomegranate():
    crop_system = CropRecommendationSystem()
    
    # Pomegranate ideal conditions
    N, P, K = 100, 50, 50
    temperature, humidity = 25, 50
    ph, rainfall = 7.0, 600
    
    # Calculate score for pomegranate
    pom_score = crop_system.calculate_crop_suitability('pomegranate', N, P, K, temperature, humidity, ph, rainfall)
    
    # Calculate score for rice (for comparison)
    rice_score = crop_system.calculate_crop_suitability('rice', N, P, K, temperature, humidity, ph, rainfall)
    
    # Get recommendation
    recommendation = crop_system.recommend_crop(N, P, K, temperature, humidity, ph, rainfall)
    
    print("Pomegranate Score:", pom_score)
    print("Rice Score:", rice_score)
    print("\nRecommendation:")
    print(f"- Crop: {recommendation['crop']}")
    print(f"- Confidence: {recommendation['confidence_score']}")
    
    # Get top 5 crops
    print("\nTop 5 Crops:")
    for i, crop in enumerate(crop_system.get_top_recommendations(N, P, K, temperature, humidity, ph, rainfall, 5), 1):
        print(f"{i}. {crop['crop']} (Score: {crop['suitability_score']})")

if __name__ == "__main__":
    test_pomegranate()
