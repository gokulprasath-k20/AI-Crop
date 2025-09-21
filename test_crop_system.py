from working_crop_system import CropRecommendationSystem, comprehensive_analysis
import random

def test_pomegranate_conditions():
    """Test with ideal pomegranate growing conditions."""
    print("\n🌱 Testing Pomegranate Ideal Conditions")
    print("=" * 50)
    
    # Ideal pomegranate conditions
    test_case = {
        'N': 100, 'P': 50, 'K': 50, 
        'temperature': 25, 'humidity': 50, 
        'ph': 7.0, 'rainfall': 600
    }
    
    result = comprehensive_analysis(**test_case)
    print_result(test_case, result)

def test_rice_conditions():
    """Test with ideal rice growing conditions."""
    print("\n🌾 Testing Rice Ideal Conditions")
    print("=" * 50)
    
    # Ideal rice conditions
    test_case = {
        'N': 100, 'P': 50, 'K': 40, 
        'temperature': 24, 'humidity': 85, 
        'ph': 6.2, 'rainfall': 1800
    }
    
    result = comprehensive_analysis(**test_case)
    print_result(test_case, result)

def test_random_conditions():
    """Test with random conditions."""
    print("\n🎲 Testing Random Conditions")
    print("=" * 50)
    
    # Random conditions
    test_case = {
        'N': random.randint(20, 120),
        'P': random.randint(10, 80),
        'K': random.randint(10, 100),
        'temperature': random.uniform(10, 35),
        'humidity': random.uniform(30, 90),
        'ph': round(random.uniform(5.5, 8.0), 1),
        'rainfall': random.randint(200, 2000)
    }
    
    result = comprehensive_analysis(**test_case)
    print_result(test_case, result)

def print_result(inputs, result):
    """Print the test results in a readable format."""
    print("\n📊 Input Parameters:")
    for param, value in inputs.items():
        print(f"  - {param}: {value}")
    
    print("\n🌿 Recommendation:")
    primary = result['primary_recommendation']
    print(f"  Primary: {primary['crop'].title()} (Confidence: {primary['confidence_score']*100:.1f}%)")
    
    print("\n🌱 Alternatives:")
    for i, alt in enumerate(result['alternative_crops'], 1):
        print(f"  {i}. {alt['crop'].title()} (Score: {alt['suitability_score']*100:.1f}%)")
    
    print("\n✅ Input Validation:")
    print(f"  Is Valid: {result['input_validation']['is_valid']}")
    if result['input_validation']['warnings']:
        print("  Warnings:")
        for warning in result['input_validation']['warnings']:
            print(f"    - {warning}")

def run_all_tests():
    """Run all test cases."""
    test_pomegranate_conditions()
    test_rice_conditions()
    test_random_conditions()

if __name__ == "__main__":
    print("🌱 Crop Recommendation System - Test Suite")
    print("=" * 50)
    run_all_tests()
