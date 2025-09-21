from working_crop_system import CropRecommendationSystem

def test_pomegranate():
    # Initialize the crop system
    crop_system = CropRecommendationSystem()
    
    # Pomegranate ideal conditions
    N, P, K = 100, 50, 50
    temperature, humidity = 25, 50
    ph, rainfall = 7.0, 600
    
    # Get recommendation
    recommendation = crop_system.recommend_crop(N, P, K, temperature, humidity, ph, rainfall)
    
    print("🌱 Testing Pomegranate Recommendation")
    print("=" * 50)
    print(f"Input Conditions:")
    print(f"- N: {N}, P: {P}, K: {K}")
    print(f"- Temperature: {temperature}°C, Humidity: {humidity}%")
    print(f"- pH: {ph}, Rainfall: {rainfall}mm")
    print("\nRecommendation:")
    print(f"- Primary Crop: {recommendation['crop'].title()}")
    print(f"- Confidence: {recommendation['confidence_score']*100:.1f}%")
    print(f"- Predicted Yield: {recommendation['predicted_yield_kg_per_ha']:.2f} kg/ha")
    print(f"- Sustainability Score: {recommendation['sustainability_score']:.1f}/10")
    
    # Check if pomegranate is in the top 3 recommendations
    alternatives = crop_system.get_top_recommendations(N, P, K, temperature, humidity, ph, rainfall, 3)
    print("\nTop 3 Recommendations:")
    for i, crop in enumerate(alternatives, 1):
        print(f"{i}. {crop['crop'].title()} (Score: {crop['suitability_score']*100:.1f}%)")
    
    # Check if pomegranate is in the top 3
    pomegranate_rank = [i for i, crop in enumerate(alternatives, 1) if crop['crop'] == 'pomegranate']
    if pomegranate_rank:
        print(f"\n✅ Pomegranate is in the top {pomegranate_rank[0]} recommendations!")
    else:
        print("\n❌ Pomegranate is not in the top 3 recommendations.")

if __name__ == "__main__":
    test_pomegranate()
