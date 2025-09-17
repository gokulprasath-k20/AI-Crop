# Simple Crop Recommendation System - SIH 2025
# Minimal version without visualization dependencies

import csv
import random
import json
from typing import Dict, List

# Crop-specific data for yield and sustainability calculations
CROP_DATA = {
    'rice': {'base_yield': 4500, 'water_need': 1500, 'fertilizer_efficiency': 0.7},
    'wheat': {'base_yield': 3200, 'water_need': 600, 'fertilizer_efficiency': 0.8},
    'maize': {'base_yield': 5500, 'water_need': 800, 'fertilizer_efficiency': 0.75},
    'cotton': {'base_yield': 1800, 'water_need': 1200, 'fertilizer_efficiency': 0.6},
    'sugarcane': {'base_yield': 70000, 'water_need': 2000, 'fertilizer_efficiency': 0.65},
    'jute': {'base_yield': 2500, 'water_need': 1000, 'fertilizer_efficiency': 0.7},
    'coffee': {'base_yield': 1200, 'water_need': 1800, 'fertilizer_efficiency': 0.8},
    'coconut': {'base_yield': 8000, 'water_need': 1200, 'fertilizer_efficiency': 0.85},
    'papaya': {'base_yield': 45000, 'water_need': 1000, 'fertilizer_efficiency': 0.75},
    'orange': {'base_yield': 25000, 'water_need': 900, 'fertilizer_efficiency': 0.8},
    'apple': {'base_yield': 20000, 'water_need': 800, 'fertilizer_efficiency': 0.85},
    'muskmelon': {'base_yield': 15000, 'water_need': 600, 'fertilizer_efficiency': 0.7},
    'watermelon': {'base_yield': 25000, 'water_need': 700, 'fertilizer_efficiency': 0.7},
    'grapes': {'base_yield': 18000, 'water_need': 650, 'fertilizer_efficiency': 0.8},
    'mango': {'base_yield': 12000, 'water_need': 1100, 'fertilizer_efficiency': 0.75},
    'banana': {'base_yield': 35000, 'water_need': 1500, 'fertilizer_efficiency': 0.7},
    'pomegranate': {'base_yield': 15000, 'water_need': 800, 'fertilizer_efficiency': 0.8},
    'lentil': {'base_yield': 1200, 'water_need': 400, 'fertilizer_efficiency': 0.9},
    'blackgram': {'base_yield': 800, 'water_need': 350, 'fertilizer_efficiency': 0.85},
    'mungbean': {'base_yield': 900, 'water_need': 300, 'fertilizer_efficiency': 0.9},
    'mothbeans': {'base_yield': 700, 'water_need': 250, 'fertilizer_efficiency': 0.85},
    'pigeonpeas': {'base_yield': 1000, 'water_need': 400, 'fertilizer_efficiency': 0.8},
    'kidneybeans': {'base_yield': 1500, 'water_need': 500, 'fertilizer_efficiency': 0.8},
    'chickpea': {'base_yield': 1300, 'water_need': 350, 'fertilizer_efficiency': 0.85}
}

# Simple rule-based crop recommendation system
def simple_crop_recommendation(N, P, K, temperature, humidity, ph, rainfall):
    """
    Simple rule-based crop recommendation based on parameter ranges.
    """
    
    # Define crop suitability rules
    crop_rules = {
        'rice': {
            'N': (80, 120), 'P': (40, 60), 'K': (35, 45),
            'temperature': (20, 27), 'humidity': (80, 90),
            'ph': (5.5, 7.0), 'rainfall': (1500, 2000)
        },
        'wheat': {
            'N': (50, 80), 'P': (30, 50), 'K': (30, 50),
            'temperature': (15, 25), 'humidity': (50, 70),
            'ph': (6.0, 7.5), 'rainfall': (450, 650)
        },
        'maize': {
            'N': (70, 110), 'P': (35, 55), 'K': (20, 40),
            'temperature': (18, 27), 'humidity': (60, 80),
            'ph': (5.8, 7.0), 'rainfall': (600, 1000)
        },
        'cotton': {
            'N': (100, 140), 'P': (40, 70), 'K': (40, 60),
            'temperature': (21, 30), 'humidity': (50, 80),
            'ph': (5.8, 8.0), 'rainfall': (600, 1200)
        },
        'banana': {
            'N': (100, 140), 'P': (50, 80), 'K': (60, 100),
            'temperature': (26, 32), 'humidity': (75, 85),
            'ph': (6.0, 7.5), 'rainfall': (1200, 2000)
        },
        'mango': {
            'N': (80, 120), 'P': (40, 60), 'K': (40, 60),
            'temperature': (24, 32), 'humidity': (60, 80),
            'ph': (5.5, 7.5), 'rainfall': (800, 1200)
        },
        'grapes': {
            'N': (60, 100), 'P': (35, 55), 'K': (40, 60),
            'temperature': (15, 25), 'humidity': (60, 80),
            'ph': (6.0, 7.0), 'rainfall': (500, 800)
        },
        'apple': {
            'N': (60, 100), 'P': (30, 50), 'K': (30, 50),
            'temperature': (15, 25), 'humidity': (60, 80),
            'ph': (6.0, 7.0), 'rainfall': (1000, 1500)
        },
        'orange': {
            'N': (80, 120), 'P': (40, 60), 'K': (40, 60),
            'temperature': (15, 30), 'humidity': (50, 80),
            'ph': (6.0, 7.5), 'rainfall': (600, 1200)
        },
        'coconut': {
            'N': (80, 120), 'P': (40, 60), 'K': (60, 100),
            'temperature': (25, 32), 'humidity': (70, 85),
            'ph': (5.5, 7.0), 'rainfall': (1000, 2000)
        }
    }
    
    # Calculate suitability scores for each crop
    crop_scores = {}
    
    for crop, rules in crop_rules.items():
        score = 0
        total_params = len(rules)
        
        for param, (min_val, max_val) in rules.items():
            param_value = locals()[param]
            
            if min_val <= param_value <= max_val:
                score += 1
            elif param_value < min_val:
                # Penalize based on how far below minimum
                penalty = (min_val - param_value) / min_val
                score += max(0, 1 - penalty)
            else:
                # Penalize based on how far above maximum
                penalty = (param_value - max_val) / max_val
                score += max(0, 1 - penalty)
        
        crop_scores[crop] = score / total_params
    
    # Return the crop with highest score
    best_crop = max(crop_scores, key=crop_scores.get)
    return best_crop, crop_scores[best_crop]

def calculate_yield_prediction(crop, N, P, K, temperature, humidity, ph, rainfall):
    """Calculate predicted yield based on crop and conditions."""
    
    crop_lower = crop.lower()
    
    if crop_lower in CROP_DATA:
        base_yield = CROP_DATA[crop_lower]['base_yield']
        fertilizer_efficiency = CROP_DATA[crop_lower]['fertilizer_efficiency']
    else:
        base_yield = 2000
        fertilizer_efficiency = 0.75
    
    # Calculate factors
    nutrient_factor = (N + P + K) / 300
    temp_factor = 1.0 if 20 <= temperature <= 30 else 0.8
    humidity_factor = humidity / 100
    ph_factor = 1.0 if 6.0 <= ph <= 7.5 else 0.8
    rainfall_factor = min(1.0, rainfall / 800)
    
    yield_multiplier = (
        nutrient_factor * fertilizer_efficiency * 0.4 +
        temp_factor * 0.25 +
        humidity_factor * 0.15 +
        ph_factor * 0.1 +
        rainfall_factor * 0.1
    )
    
    predicted_yield = base_yield * yield_multiplier * random.uniform(0.85, 1.15)
    return max(100, predicted_yield)

def calculate_sustainability_score(crop, N, P, K, temperature, humidity, ph, rainfall):
    """Calculate sustainability score (1-10)."""
    
    crop_lower = crop.lower()
    
    if crop_lower in CROP_DATA:
        water_need = CROP_DATA[crop_lower]['water_need']
    else:
        water_need = 800
    
    water_score = max(1, 10 - (water_need / 200))
    fertilizer_score = max(1, 10 - (N / 20))
    ph_score = max(1, 10 - abs(ph - 7.0))
    
    sustainability_score = (water_score * 0.4 + fertilizer_score * 0.3 + ph_score * 0.3)
    return max(1.0, min(10.0, sustainability_score))

def recommend_crop(N, P, K, temperature, humidity, ph, rainfall):
    """
    Main crop recommendation function with yield and sustainability.
    """
    
    try:
        # Get crop recommendation
        crop, confidence = simple_crop_recommendation(N, P, K, temperature, humidity, ph, rainfall)
        
        # Calculate yield and sustainability
        predicted_yield = calculate_yield_prediction(crop, N, P, K, temperature, humidity, ph, rainfall)
        sustainability_score = calculate_sustainability_score(crop, N, P, K, temperature, humidity, ph, rainfall)
        
        return {
            'crop': crop,
            'confidence_score': round(confidence, 3),
            'predicted_yield_kg_per_ha': round(predicted_yield, 2),
            'sustainability_score': round(sustainability_score, 2)
        }
        
    except Exception as e:
        return {'error': f"Error in prediction: {str(e)}"}

def get_crop_alternatives(N, P, K, temperature, humidity, ph, rainfall, top_n=5):
    """Get top N crop alternatives with their scores."""
    
    crop_rules = {
        'rice': {'N': (80, 120), 'P': (40, 60), 'K': (35, 45), 'temperature': (20, 27), 'humidity': (80, 90), 'ph': (5.5, 7.0), 'rainfall': (1500, 2000)},
        'wheat': {'N': (50, 80), 'P': (30, 50), 'K': (30, 50), 'temperature': (15, 25), 'humidity': (50, 70), 'ph': (6.0, 7.5), 'rainfall': (450, 650)},
        'maize': {'N': (70, 110), 'P': (35, 55), 'K': (20, 40), 'temperature': (18, 27), 'humidity': (60, 80), 'ph': (5.8, 7.0), 'rainfall': (600, 1000)},
        'cotton': {'N': (100, 140), 'P': (40, 70), 'K': (40, 60), 'temperature': (21, 30), 'humidity': (50, 80), 'ph': (5.8, 8.0), 'rainfall': (600, 1200)},
        'banana': {'N': (100, 140), 'P': (50, 80), 'K': (60, 100), 'temperature': (26, 32), 'humidity': (75, 85), 'ph': (6.0, 7.5), 'rainfall': (1200, 2000)},
        'mango': {'N': (80, 120), 'P': (40, 60), 'K': (40, 60), 'temperature': (24, 32), 'humidity': (60, 80), 'ph': (5.5, 7.5), 'rainfall': (800, 1200)},
        'grapes': {'N': (60, 100), 'P': (35, 55), 'K': (40, 60), 'temperature': (15, 25), 'humidity': (60, 80), 'ph': (6.0, 7.0), 'rainfall': (500, 800)},
        'apple': {'N': (60, 100), 'P': (30, 50), 'K': (30, 50), 'temperature': (15, 25), 'humidity': (60, 80), 'ph': (6.0, 7.0), 'rainfall': (1000, 1500)},
        'orange': {'N': (80, 120), 'P': (40, 60), 'K': (40, 60), 'temperature': (15, 30), 'humidity': (50, 80), 'ph': (6.0, 7.5), 'rainfall': (600, 1200)},
        'coconut': {'N': (80, 120), 'P': (40, 60), 'K': (60, 100), 'temperature': (25, 32), 'humidity': (70, 85), 'ph': (5.5, 7.0), 'rainfall': (1000, 2000)}
    }
    
    crop_scores = {}
    
    for crop, rules in crop_rules.items():
        score = 0
        for param, (min_val, max_val) in rules.items():
            param_value = locals()[param]
            if min_val <= param_value <= max_val:
                score += 1
            elif param_value < min_val:
                penalty = (min_val - param_value) / min_val
                score += max(0, 1 - penalty)
            else:
                penalty = (param_value - max_val) / max_val
                score += max(0, 1 - penalty)
        
        crop_scores[crop] = score / len(rules)
    
    # Sort and return top N
    sorted_crops = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)
    
    alternatives = []
    for crop, score in sorted_crops[:top_n]:
        yield_pred = calculate_yield_prediction(crop, N, P, K, temperature, humidity, ph, rainfall)
        sustainability = calculate_sustainability_score(crop, N, P, K, temperature, humidity, ph, rainfall)
        
        alternatives.append({
            'crop': crop,
            'suitability_score': round(score, 3),
            'predicted_yield_kg_per_ha': round(yield_pred, 2),
            'sustainability_score': round(sustainability, 2)
        })
    
    return alternatives

# Test the system
def test_system():
    """Test the crop recommendation system."""
    
    print("🌾 Simple Crop Recommendation System - SIH 2025")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {
            'name': 'Standard Test Case',
            'params': {'N': 90, 'P': 42, 'K': 43, 'temperature': 21, 'humidity': 82, 'ph': 6.5, 'rainfall': 203}
        },
        {
            'name': 'High Fertility Soil',
            'params': {'N': 120, 'P': 60, 'K': 80, 'temperature': 25, 'humidity': 70, 'ph': 7.0, 'rainfall': 400}
        },
        {
            'name': 'Rice Growing Conditions',
            'params': {'N': 100, 'P': 50, 'K': 40, 'temperature': 24, 'humidity': 85, 'ph': 6.2, 'rainfall': 1800}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test_case['name']}")
        print("-" * 40)
        
        result = recommend_crop(**test_case['params'])
        
        if 'error' not in result:
            print(f"🌾 Recommended Crop: {result['crop']}")
            print(f"🎯 Confidence Score: {result['confidence_score']}")
            print(f"📈 Predicted Yield: {result['predicted_yield_kg_per_ha']:,.0f} kg/ha")
            print(f"🌱 Sustainability Score: {result['sustainability_score']}/10")
            
            # Get alternatives
            alternatives = get_crop_alternatives(**test_case['params'], top_n=3)
            print(f"\n🔄 Top 3 Alternatives:")
            for j, alt in enumerate(alternatives[:3], 1):
                print(f"   {j}. {alt['crop']}: {alt['predicted_yield_kg_per_ha']:,.0f} kg/ha, "
                      f"Sustainability: {alt['sustainability_score']}/10")
        else:
            print(f"❌ Error: {result['error']}")
    
    print(f"\n✅ System testing completed!")
    return True

if __name__ == "__main__":
    test_system()
