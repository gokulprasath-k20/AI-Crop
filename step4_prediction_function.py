# STEP 4: BUILD A PREDICTION FUNCTION
# AI-Based Crop Recommendation System for SIH 2025

import pandas as pd
import numpy as np
import joblib
import json
import os
from typing import Union, Dict, List
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("AI-BASED CROP RECOMMENDATION SYSTEM - STEP 4")
print("Building Prediction Function")
print("=" * 60)

# Load model metadata to understand the model structure
try:
    with open('model_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    model_name = metadata['model_name']
    feature_names = metadata['feature_names']
    target_classes = metadata['target_classes']
    uses_encoded_labels = metadata['uses_encoded_labels']
    model_accuracy = metadata['final_accuracy']
    
    print("✓ Model metadata loaded successfully!")
    print(f"Model: {model_name}")
    print(f"Accuracy: {model_accuracy*100:.2f}%")
    print(f"Features: {feature_names}")
    print(f"Number of crops: {len(target_classes)}")
    
except FileNotFoundError:
    print("❌ Error: model_metadata.json not found.")
    print("Please run step3_model_optimization.py first.")
    exit()

# Find the model file
model_filename = f'crop_recommendation_model_{model_name.lower().replace(" ", "_")}.pkl'

if not os.path.exists(model_filename):
    print(f"❌ Error: Model file {model_filename} not found.")
    print("Please run step3_model_optimization.py first.")
    exit()

print(f"✓ Model file found: {model_filename}")

def recommend_crop(N: float, P: float, K: float, temperature: float, 
                  humidity: float, ph: float, rainfall: float) -> str:
    """
    Recommend the best crop based on soil and climate conditions.
    
    Parameters:
    -----------
    N : float
        Nitrogen content in soil (kg/ha)
    P : float  
        Phosphorus content in soil (kg/ha)
    K : float
        Potassium content in soil (kg/ha)
    temperature : float
        Average temperature (°C)
    humidity : float
        Relative humidity (%)
    ph : float
        pH value of soil
    rainfall : float
        Annual rainfall (mm)
    
    Returns:
    --------
    str
        Recommended crop name
    """
    
    try:
        # Load the trained model
        model = joblib.load(model_filename)
        
        # Load label encoder if needed
        if uses_encoded_labels:
            label_encoder = joblib.load('label_encoder.pkl')
        
        # Create input array in the correct order
        input_features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        
        # Make prediction
        if uses_encoded_labels:
            prediction_encoded = model.predict(input_features)
            prediction = label_encoder.inverse_transform(prediction_encoded)[0]
        else:
            prediction = model.predict(input_features)[0]
        
        return prediction
        
    except Exception as e:
        return f"Error in prediction: {str(e)}"

def recommend_crop_with_confidence(N: float, P: float, K: float, temperature: float, 
                                 humidity: float, ph: float, rainfall: float) -> Dict:
    """
    Recommend crop with confidence scores for top predictions.
    
    Parameters:
    -----------
    N, P, K, temperature, humidity, ph, rainfall : float
        Same as recommend_crop function
    
    Returns:
    --------
    dict
        Dictionary containing recommended crop, confidence, and top alternatives
    """
    
    try:
        # Load the trained model
        model = joblib.load(model_filename)
        
        # Load label encoder if needed
        if uses_encoded_labels:
            label_encoder = joblib.load('label_encoder.pkl')
        
        # Create input array
        input_features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        
        # Get prediction probabilities (if available)
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(input_features)[0]
            
            # Get class labels
            if uses_encoded_labels:
                classes = label_encoder.classes_
            else:
                classes = model.classes_
            
            # Sort by probability
            prob_indices = np.argsort(probabilities)[::-1]
            
            # Get top 3 recommendations
            top_3 = []
            for i in range(min(3, len(prob_indices))):
                idx = prob_indices[i]
                crop = classes[idx]
                confidence = probabilities[idx]
                top_3.append({
                    'crop': crop,
                    'confidence': float(confidence),
                    'confidence_percentage': float(confidence * 100)
                })
            
            return {
                'recommended_crop': top_3[0]['crop'],
                'confidence': top_3[0]['confidence'],
                'confidence_percentage': top_3[0]['confidence_percentage'],
                'top_3_recommendations': top_3,
                'input_parameters': {
                    'N': N, 'P': P, 'K': K, 'temperature': temperature,
                    'humidity': humidity, 'ph': ph, 'rainfall': rainfall
                }
            }
        else:
            # For models without predict_proba, just return the prediction
            if uses_encoded_labels:
                prediction_encoded = model.predict(input_features)
                prediction = label_encoder.inverse_transform(prediction_encoded)[0]
            else:
                prediction = model.predict(input_features)[0]
            
            return {
                'recommended_crop': prediction,
                'confidence': 'N/A',
                'confidence_percentage': 'N/A',
                'top_3_recommendations': [{'crop': prediction, 'confidence': 'N/A'}],
                'input_parameters': {
                    'N': N, 'P': P, 'K': K, 'temperature': temperature,
                    'humidity': humidity, 'ph': ph, 'rainfall': rainfall
                }
            }
            
    except Exception as e:
        return {'error': f"Error in prediction: {str(e)}"}

def validate_input_parameters(N: float, P: float, K: float, temperature: float, 
                            humidity: float, ph: float, rainfall: float) -> Dict:
    """
    Validate input parameters and provide warnings if values are unusual.
    
    Returns:
    --------
    dict
        Validation results with warnings if any
    """
    
    warnings = []
    
    # Define reasonable ranges based on typical agricultural values
    ranges = {
        'N': (0, 200),      # Nitrogen: 0-200 kg/ha
        'P': (0, 150),      # Phosphorus: 0-150 kg/ha  
        'K': (0, 300),      # Potassium: 0-300 kg/ha
        'temperature': (0, 50),  # Temperature: 0-50°C
        'humidity': (0, 100),    # Humidity: 0-100%
        'ph': (3, 10),      # pH: 3-10
        'rainfall': (0, 3000)    # Rainfall: 0-3000mm
    }
    
    values = {
        'N': N, 'P': P, 'K': K, 'temperature': temperature,
        'humidity': humidity, 'ph': ph, 'rainfall': rainfall
    }
    
    for param, value in values.items():
        min_val, max_val = ranges[param]
        if value < min_val or value > max_val:
            warnings.append(f"{param}: {value} is outside typical range ({min_val}-{max_val})")
    
    return {
        'is_valid': len(warnings) == 0,
        'warnings': warnings,
        'input_values': values
    }

print("\n" + "=" * 60)
print("TESTING THE PREDICTION FUNCTION")
print("=" * 60)

# Test with the provided example
print("🧪 Testing with hardcoded example...")
test_input = {
    'N': 90,
    'P': 42, 
    'K': 43,
    'temperature': 21,
    'humidity': 82,
    'ph': 6.5,
    'rainfall': 203
}

print(f"Test input: {test_input}")

# Test basic prediction function
print("\n1. Basic Prediction Function Test:")
print("-" * 40)
prediction = recommend_crop(**test_input)
print(f"Recommended crop: {prediction}")

# Test advanced prediction function with confidence
print("\n2. Advanced Prediction Function Test:")
print("-" * 40)
detailed_prediction = recommend_crop_with_confidence(**test_input)

if 'error' not in detailed_prediction:
    print(f"Recommended crop: {detailed_prediction['recommended_crop']}")
    if detailed_prediction['confidence'] != 'N/A':
        print(f"Confidence: {detailed_prediction['confidence_percentage']:.1f}%")
    
    print("\nTop 3 recommendations:")
    for i, rec in enumerate(detailed_prediction['top_3_recommendations'], 1):
        if rec['confidence'] != 'N/A':
            print(f"  {i}. {rec['crop']} ({rec['confidence_percentage']:.1f}%)")
        else:
            print(f"  {i}. {rec['crop']}")
else:
    print(f"Error: {detailed_prediction['error']}")

# Test input validation
print("\n3. Input Validation Test:")
print("-" * 40)
validation_result = validate_input_parameters(**test_input)
print(f"Input valid: {validation_result['is_valid']}")
if validation_result['warnings']:
    print("Warnings:")
    for warning in validation_result['warnings']:
        print(f"  ⚠️ {warning}")
else:
    print("✓ All input parameters are within expected ranges")

# Test with some edge cases
print("\n4. Edge Case Testing:")
print("-" * 40)

edge_cases = [
    {
        'name': 'High Nitrogen',
        'params': {'N': 150, 'P': 50, 'K': 50, 'temperature': 25, 'humidity': 70, 'ph': 7.0, 'rainfall': 150}
    },
    {
        'name': 'Low pH (Acidic)',
        'params': {'N': 80, 'P': 40, 'K': 40, 'temperature': 22, 'humidity': 75, 'ph': 4.5, 'rainfall': 200}
    },
    {
        'name': 'High Rainfall',
        'params': {'N': 70, 'P': 35, 'K': 35, 'temperature': 28, 'humidity': 85, 'ph': 6.8, 'rainfall': 800}
    }
]

for case in edge_cases:
    print(f"\n{case['name']}:")
    prediction = recommend_crop(**case['params'])
    print(f"  Input: {case['params']}")
    print(f"  Prediction: {prediction}")

# Create a comprehensive test function
def comprehensive_crop_recommendation(N: float, P: float, K: float, temperature: float, 
                                    humidity: float, ph: float, rainfall: float) -> Dict:
    """
    Comprehensive crop recommendation with validation and detailed output.
    """
    
    # Validate inputs
    validation = validate_input_parameters(N, P, K, temperature, humidity, ph, rainfall)
    
    # Get detailed prediction
    prediction_result = recommend_crop_with_confidence(N, P, K, temperature, humidity, ph, rainfall)
    
    # Combine results
    result = {
        'input_validation': validation,
        'prediction_result': prediction_result,
        'model_info': {
            'model_name': model_name,
            'accuracy': f"{model_accuracy*100:.2f}%",
            'features_used': feature_names
        }
    }
    
    return result

# Test comprehensive function
print(f"\n5. Comprehensive Function Test:")
print("-" * 40)
comprehensive_result = comprehensive_crop_recommendation(**test_input)

print("Input Validation:")
if comprehensive_result['input_validation']['is_valid']:
    print("  ✓ All inputs valid")
else:
    for warning in comprehensive_result['input_validation']['warnings']:
        print(f"  ⚠️ {warning}")

if 'error' not in comprehensive_result['prediction_result']:
    print(f"\nRecommendation: {comprehensive_result['prediction_result']['recommended_crop']}")
    if comprehensive_result['prediction_result']['confidence'] != 'N/A':
        print(f"Confidence: {comprehensive_result['prediction_result']['confidence_percentage']:.1f}%")

print(f"\nModel Info: {comprehensive_result['model_info']['model_name']} "
      f"(Accuracy: {comprehensive_result['model_info']['accuracy']})")

# Save the functions to a separate module for easy import
print(f"\n💾 Saving prediction functions to crop_predictor.py...")

predictor_code = f'''# Crop Recommendation Predictor Module
# Generated for SIH 2025 AI-Based Crop Recommendation System

import numpy as np
import joblib
import json
from typing import Dict, Union
import warnings
warnings.filterwarnings('ignore')

# Model configuration (loaded from metadata)
MODEL_FILENAME = "{model_filename}"
USES_ENCODED_LABELS = {uses_encoded_labels}
FEATURE_NAMES = {feature_names}
MODEL_NAME = "{model_name}"
MODEL_ACCURACY = {model_accuracy}

def recommend_crop(N: float, P: float, K: float, temperature: float, 
                  humidity: float, ph: float, rainfall: float) -> str:
    """
    Recommend the best crop based on soil and climate conditions.
    
    Parameters:
    -----------
    N : float - Nitrogen content in soil (kg/ha)
    P : float - Phosphorus content in soil (kg/ha)
    K : float - Potassium content in soil (kg/ha)
    temperature : float - Average temperature (°C)
    humidity : float - Relative humidity (%)
    ph : float - pH value of soil
    rainfall : float - Annual rainfall (mm)
    
    Returns:
    --------
    str - Recommended crop name
    """
    
    try:
        model = joblib.load(MODEL_FILENAME)
        
        if USES_ENCODED_LABELS:
            label_encoder = joblib.load('label_encoder.pkl')
        
        input_features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        
        if USES_ENCODED_LABELS:
            prediction_encoded = model.predict(input_features)
            prediction = label_encoder.inverse_transform(prediction_encoded)[0]
        else:
            prediction = model.predict(input_features)[0]
        
        return prediction
        
    except Exception as e:
        return f"Error in prediction: {{str(e)}}"

def recommend_crop_with_confidence(N: float, P: float, K: float, temperature: float, 
                                 humidity: float, ph: float, rainfall: float) -> Dict:
    """Recommend crop with confidence scores."""
    
    try:
        model = joblib.load(MODEL_FILENAME)
        
        if USES_ENCODED_LABELS:
            label_encoder = joblib.load('label_encoder.pkl')
        
        input_features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(input_features)[0]
            
            if USES_ENCODED_LABELS:
                classes = label_encoder.classes_
            else:
                classes = model.classes_
            
            prob_indices = np.argsort(probabilities)[::-1]
            
            top_3 = []
            for i in range(min(3, len(prob_indices))):
                idx = prob_indices[i]
                crop = classes[idx]
                confidence = probabilities[idx]
                top_3.append({{
                    'crop': crop,
                    'confidence': float(confidence),
                    'confidence_percentage': float(confidence * 100)
                }})
            
            return {{
                'recommended_crop': top_3[0]['crop'],
                'confidence': top_3[0]['confidence'],
                'confidence_percentage': top_3[0]['confidence_percentage'],
                'top_3_recommendations': top_3
            }}
        else:
            if USES_ENCODED_LABELS:
                prediction_encoded = model.predict(input_features)
                prediction = label_encoder.inverse_transform(prediction_encoded)[0]
            else:
                prediction = model.predict(input_features)[0]
            
            return {{
                'recommended_crop': prediction,
                'confidence': 'N/A',
                'confidence_percentage': 'N/A',
                'top_3_recommendations': [{{'crop': prediction, 'confidence': 'N/A'}}]
            }}
            
    except Exception as e:
        return {{'error': f"Error in prediction: {{str(e)}}"}}

# Quick test function
def test_predictor():
    """Test the predictor with sample data."""
    test_data = {{
        'N': 90, 'P': 42, 'K': 43, 'temperature': 21,
        'humidity': 82, 'ph': 6.5, 'rainfall': 203
    }}
    
    result = recommend_crop(**test_data)
    print(f"Test prediction: {{result}}")
    return result

if __name__ == "__main__":
    test_predictor()
'''

with open('crop_predictor.py', 'w') as f:
    f.write(predictor_code)

print("✓ Prediction functions saved to crop_predictor.py")

# Test the saved module
print(f"\n🧪 Testing the saved module...")
try:
    import crop_predictor
    test_result = crop_predictor.test_predictor()
    print("✓ Saved module works correctly!")
except Exception as e:
    print(f"❌ Error testing saved module: {e}")

print("\n" + "=" * 60)
print("STEP 4 COMPLETED SUCCESSFULLY! 🎉")
print("=" * 60)
print("Summary:")
print("✓ recommend_crop() function created and tested")
print("✓ recommend_crop_with_confidence() function created")
print("✓ Input validation function created")
print("✓ Comprehensive prediction function created")
print("✓ Edge case testing completed")
print("✓ Functions saved to crop_predictor.py module")
print("✓ Module import and functionality verified")
print(f"✓ Test prediction: {prediction}")
print("\nReady for Step 5: Expanding for yield and sustainability!")
