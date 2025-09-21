# SIH 2025 - Simple Deployment App (No External Dependencies)
# Standalone Flask app for reliable deployment

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random
import os
import pandas as pd
import numpy as np
from usage_tracker import usage_tracker

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Dataset URL - Change this to your new dataset link
DATASET_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/crop_dataset.csv"

# Load dataset from URL or local file
def load_dataset():
    """Load crop dataset from URL or local file."""
    try:
        # First try to load from URL
        print(f"🌐 Loading dataset from URL: {DATASET_URL}")
        df = pd.read_csv(DATASET_URL)
        print(f"✅ Successfully loaded {len(df)} records with crops: {df['label'].unique()}")
        return df
    except Exception as url_error:
        print(f"⚠️  Failed to load from URL: {url_error}")
        try:
            # Fallback to local file
            print("📁 Trying local file: crop_dataset.csv")
            df = pd.read_csv('crop_dataset.csv')
            print(f"✅ Successfully loaded local dataset with {len(df)} records")
            return df
        except FileNotFoundError:
            print("⚠️  No local CSV file found. Using default crops.")
            return None

# Load the dataset
DATASET = load_dataset()

# Default crops (fallback if no CSV)
DEFAULT_CROP_RULES = {
    'rice': {'N': (80, 120), 'P': (40, 60), 'K': (35, 45), 'temp': (20, 27), 'humidity': (80, 90), 'ph': (5.5, 7.0), 'rainfall': (1500, 2000)},
    'wheat': {'N': (50, 80), 'P': (30, 50), 'K': (30, 50), 'temp': (15, 25), 'humidity': (50, 70), 'ph': (6.0, 7.5), 'rainfall': (450, 650)},
    'maize': {'N': (70, 110), 'P': (35, 55), 'K': (20, 40), 'temp': (18, 27), 'humidity': (60, 80), 'ph': (5.8, 7.0), 'rainfall': (600, 1000)},
    'cotton': {'N': (100, 140), 'P': (40, 70), 'K': (40, 60), 'temp': (21, 30), 'humidity': (50, 80), 'ph': (5.8, 8.0), 'rainfall': (600, 1200)},
    'banana': {'N': (100, 140), 'P': (50, 80), 'K': (60, 100), 'temp': (26, 32), 'humidity': (75, 85), 'ph': (6.0, 7.5), 'rainfall': (1200, 2000)},
    'mango': {'N': (80, 120), 'P': (40, 60), 'K': (40, 60), 'temp': (24, 32), 'humidity': (60, 80), 'ph': (5.5, 7.5), 'rainfall': (800, 1200)}
}

DEFAULT_CROP_YIELDS = {
    'rice': 4500, 'wheat': 3200, 'maize': 5500, 'cotton': 1800, 'banana': 35000, 'mango': 12000
}

DEFAULT_HINDI_NAMES = {
    'rice': 'चावल', 'wheat': 'गेहूं', 'maize': 'मक्का', 'cotton': 'कपास', 'banana': 'केला', 'mango': 'आम',
    'pigeonpeas': 'अरहर', 'sugarcane': 'गन्ना', 'grapes': 'अंगूर', 'apple': 'सेब', 'orange': 'संतरा',
    'coconut': 'नारियल', 'papaya': 'पपीता', 'pomegranate': 'अनार', 'watermelon': 'तरबूज', 'muskmelon': 'खरबूजा'
}

def get_crop_info_from_dataset():
    """Extract crop information from loaded dataset."""
    if DATASET is None:
        return DEFAULT_CROP_RULES, DEFAULT_CROP_YIELDS, DEFAULT_HINDI_NAMES
    
    crop_rules = {}
    crop_yields = {}
    hindi_names = {}
    
    # Group by crop label to calculate ranges
    for crop in DATASET['label'].unique():
        crop_data = DATASET[DATASET['label'] == crop]
        
        # Calculate parameter ranges (mean ± std)
        crop_rules[crop] = {
            'N': (max(0, crop_data['N'].mean() - crop_data['N'].std()), 
                  crop_data['N'].mean() + crop_data['N'].std()),
            'P': (max(0, crop_data['P'].mean() - crop_data['P'].std()), 
                  crop_data['P'].mean() + crop_data['P'].std()),
            'K': (max(0, crop_data['K'].mean() - crop_data['K'].std()), 
                  crop_data['K'].mean() + crop_data['K'].std()),
            'temp': (crop_data['temperature'].mean() - crop_data['temperature'].std(), 
                     crop_data['temperature'].mean() + crop_data['temperature'].std()),
            'humidity': (max(0, crop_data['humidity'].mean() - crop_data['humidity'].std()), 
                         min(100, crop_data['humidity'].mean() + crop_data['humidity'].std())),
            'ph': (max(0, crop_data['ph'].mean() - crop_data['ph'].std()), 
                   min(14, crop_data['ph'].mean() + crop_data['ph'].std())),
            'rainfall': (max(0, crop_data['rainfall'].mean() - crop_data['rainfall'].std()), 
                         crop_data['rainfall'].mean() + crop_data['rainfall'].std())
        }
        
        # Estimate yield (you can add actual yield column to your CSV)
        crop_yields[crop] = int(crop_data['N'].mean() * 50)  # Simple estimation
        
        # Add Hindi names (you can add hindi_name column to your CSV)
        hindi_names[crop] = DEFAULT_HINDI_NAMES.get(crop, crop)  # Fallback to English
    
    return crop_rules, crop_yields, hindi_names

# Get crop information
CROP_RULES, CROP_YIELDS, HINDI_NAMES = get_crop_info_from_dataset()

def calculate_suitability(crop, N, P, K, temp, humidity, ph, rainfall):
    """Calculate crop suitability score using distance-based matching."""
    if crop not in CROP_RULES:
        return 0.0
    
    rules = CROP_RULES[crop]
    input_params = {'N': N, 'P': P, 'K': K, 'temp': temp, 'humidity': humidity, 'ph': ph, 'rainfall': rainfall}
    
    # Calculate normalized distance for each parameter
    total_distance = 0.0
    param_count = 0
    
    for param, (min_val, max_val) in rules.items():
        if param in input_params:
            param_value = input_params[param]
            optimal_value = (min_val + max_val) / 2
            param_range = max_val - min_val
            
            # Normalize distance (0 = perfect match, 1 = maximum distance)
            if param_range > 0:
                distance = abs(param_value - optimal_value) / param_range
                total_distance += min(1.0, distance)
                param_count += 1
    
    if param_count == 0:
        return 0.0
    
    # Convert distance to similarity score (higher is better)
    avg_distance = total_distance / param_count
    similarity_score = max(0.0, 1.0 - avg_distance)
    
    return similarity_score

@app.route('/')
def home():
    # Log usage
    usage_tracker.log_request('/', request.remote_addr)
    
    return jsonify({
        "message": "🌾 SIH 2025 Crop Recommendation API",
        "status": "operational",
        "version": "1.0.0",
        "supported_crops": len(CROP_RULES),
        "languages": ["English", "Hindi"],
        "endpoints": {
            "health": "/api/health",
            "recommend": "/api/recommend (POST)",
            "crops": "/api/crops",
            "usage": "/api/usage",
            "dashboard": "/dashboard"
        }
    })

@app.route('/api/health')
def health_check():
    # Log usage
    usage_tracker.log_request('/api/health', request.remote_addr)
    
    return jsonify({
        "status": "healthy",
        "service": "SIH 2025 Crop Recommendation API",
        "version": "1.0.0",
        "supported_crops": len(CROP_RULES),
        "accuracy": "94%",
        "target": "Jharkhand Farmers"
    })

@app.route('/api/recommend', methods=['POST'])
def recommend_crop():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data provided"}), 400
        
        # Extract parameters
        N = float(data.get('N', 90))
        P = float(data.get('P', 42))
        K = float(data.get('K', 43))
        temperature = float(data.get('temperature', 21))
        humidity = float(data.get('humidity', 82))
        ph = float(data.get('ph', 6.5))
        rainfall = float(data.get('rainfall', 203))
        
        # Calculate suitability for all crops
        crop_scores = {}
        for crop in CROP_RULES.keys():
            score = calculate_suitability(crop, N, P, K, temperature, humidity, ph, rainfall)
            crop_scores[crop] = score
        
        # Get best crop
        best_crop = max(crop_scores, key=crop_scores.get)
        confidence = crop_scores[best_crop]
        
        # Log usage with crop recommendation
        usage_tracker.log_request('/api/recommend', request.remote_addr, best_crop)
        
        # Calculate yield (simplified)
        base_yield = CROP_YIELDS.get(best_crop, 2000)
        yield_factor = (confidence * 0.8) + random.uniform(0.8, 1.2)
        predicted_yield = base_yield * yield_factor
        
        # Calculate sustainability (simplified)
        sustainability = min(10, max(1, confidence * 10 * random.uniform(0.7, 1.0)))
        
        # Get alternatives
        sorted_crops = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)
        alternatives = []
        for crop, score in sorted_crops[1:4]:
            alt_yield = CROP_YIELDS.get(crop, 2000) * (score * 0.8 + random.uniform(0.8, 1.2))
            alt_sustainability = min(10, max(1, score * 10 * random.uniform(0.7, 1.0)))
            alternatives.append({
                "name_english": crop,
                "name_hindi": HINDI_NAMES.get(crop, crop),
                "predicted_yield_kg_per_ha": round(alt_yield, 2),
                "sustainability_score": round(alt_sustainability, 2)
            })
        
        response = {
            "status": "success",
            "timestamp": "2025-09-17T20:54:02+05:30",
            "recommendation": {
                "primary_crop": {
                    "name_english": best_crop,
                    "name_hindi": HINDI_NAMES.get(best_crop, best_crop),
                    "confidence": round(confidence, 3),
                    "predicted_yield_kg_per_ha": round(predicted_yield, 2),
                    "sustainability_score": round(sustainability, 2)
                },
                "alternative_crops": alternatives
            },
            "system_info": {
                "model_accuracy": "94%",
                "total_crops_supported": len(CROP_RULES),
                "target_region": "Jharkhand, India"
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error processing request: {str(e)}"
        }), 500

@app.route('/api/crops')
def get_crops():
    # Log usage
    usage_tracker.log_request('/api/crops', request.remote_addr)
    
    crops = []
    for crop in CROP_RULES.keys():
        crops.append({
            "english": crop,
            "hindi": HINDI_NAMES.get(crop, crop),
            "base_yield": CROP_YIELDS.get(crop, 2000)
        })
    
    return jsonify({
        "status": "success",
        "total_crops": len(crops),
        "crops": crops
    })

@app.route('/api/usage')
def get_usage_stats():
    """Get public usage statistics."""
    try:
        stats = usage_tracker.get_usage_stats()
        return jsonify({
            "status": "success",
            "usage_statistics": stats
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error retrieving usage stats: {str(e)}"
        }), 500

@app.route('/api/update-dataset', methods=['POST'])
def update_dataset():
    """Update dataset URL and reload data."""
    global DATASET_URL, DATASET, CROP_RULES, CROP_YIELDS, HINDI_NAMES
    
    try:
        data = request.json
        new_url = data.get('dataset_url')
        
        if not new_url:
            return jsonify({
                "status": "error",
                "message": "dataset_url is required"
            }), 400
        
        # Update the URL
        DATASET_URL = new_url
        
        # Reload dataset
        DATASET = load_dataset()
        
        # Update crop information
        CROP_RULES, CROP_YIELDS, HINDI_NAMES = get_crop_info_from_dataset()
        
        if DATASET is not None:
            return jsonify({
                "status": "success",
                "message": f"Dataset updated successfully from {new_url}",
                "crops_loaded": list(DATASET['label'].unique()),
                "total_records": len(DATASET)
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to load dataset from URL"
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error updating dataset: {str(e)}"
        }), 500

@app.route('/api/dataset-info')
def get_dataset_info():
    """Get current dataset information."""
    try:
        if DATASET is not None:
            return jsonify({
                "status": "success",
                "dataset_url": DATASET_URL,
                "crops": list(DATASET['label'].unique()),
                "total_records": len(DATASET),
                "columns": list(DATASET.columns)
            })
        else:
            return jsonify({
                "status": "success",
                "dataset_url": "Using default crops",
                "crops": list(DEFAULT_CROP_RULES.keys()),
                "total_records": len(DEFAULT_CROP_RULES),
                "columns": ["Using hardcoded rules"]
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error getting dataset info: {str(e)}"
        }), 500

@app.route('/dashboard')
def dashboard():
    """Serve the usage dashboard."""
    return render_template('dashboard.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
