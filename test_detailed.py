from working_crop_system import CropRecommendationSystem

def print_crop_scores(crop_system, N, P, K, temperature, humidity, ph, rainfall, top_n=5):
    """Print detailed scores for all crops."""
    print("\n🌱 Detailed Crop Suitability Scores")
    print("=" * 60)
    
    # Calculate scores for all crops
    scores = []
    for crop in crop_system.crop_rules.keys():
        score = crop_system.calculate_crop_suitability(crop, N, P, K, temperature, humidity, ph, rainfall)
        scores.append((crop, score))
    
    # Sort by score (descending)
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Print top N crops
    for i, (crop, score) in enumerate(scores[:top_n], 1):
        print(f"{i}. {crop.title():<15} Score: {score*100:.1f}%")
    
    # Print pomegranate's position if not in top N
    pomegranate_score = next((s for c, s in scores if c == 'pomegranate'), None)
    if pomegranate_score and pomegranate_score not in [s for c, s in scores[:top_n]]:
        pomegranate_rank = [i for i, (c, s) in enumerate(scores, 1) if c == 'pomegranate'][0]
        print(f"\nℹ️  Pomegranate is ranked #{pomegranate_rank} with score: {pomegranate_score*100:.1f}%")

def test_ideal_conditions():
    """Test with ideal pomegranate conditions."""
    print("\n🌿 Testing Ideal Pomegranate Conditions")
    print("=" * 60)
    
    # Initialize the crop system
    crop_system = CropRecommendationSystem()
    
    # Pomegranate ideal conditions
    N, P, K = 100, 50, 50
    temperature, humidity = 25, 50
    ph, rainfall = 7.0, 600
    
    # Get recommendation
    recommendation = crop_system.recommend_crop(N, P, K, temperature, humidity, ph, rainfall)
    
    print("\n🌡️  Input Conditions:")
    print(f"- N: {N}, P: {P}, K: {K}")
    print(f"- Temperature: {temperature}°C, Humidity: {humidity}%")
    print(f"- pH: {ph}, Rainfall: {rainfall}mm")
    
    print("\n🎯 Recommendation:")
    print(f"- Primary Crop: {recommendation['crop'].title()}")
    print(f"- Confidence: {recommendation['confidence_score']*100:.1f}%")
    
    # Print detailed scores
    print_crop_scores(crop_system, N, P, K, temperature, humidity, ph, rainfall, 10)

def test_edge_cases():
    """Test with edge cases."""
    print("\n🔍 Testing Edge Cases")
    print("=" * 60)
    
    crop_system = CropRecommendationSystem()
    
    # Test with high humidity (pomegranate prefers 35-70%)
    print("\n🌧️  High Humidity (80%)")
    print_crop_scores(crop_system, 100, 50, 50, 25, 80, 7.0, 600, 5)
    
    # Test with low temperature (pomegranate prefers 15-30°C)
    print("\n❄️  Low Temperature (10°C)")
    print_crop_scores(crop_system, 100, 50, 50, 10, 50, 7.0, 600, 5)
    
    # Test with high temperature (pomegranate prefers 15-30°C)
    print("\n🔥 High Temperature (35°C)")
    print_crop_scores(crop_system, 100, 50, 50, 35, 50, 7.0, 600, 5)

if __name__ == "__main__":
    print("🌱 Crop Recommendation System - Detailed Testing")
    print("=" * 60)
    test_ideal_conditions()
    test_edge_cases()
