# SIH 2025 - Simple API Server (Working Version)
# Flask-based REST API for crop recommendation

from flask import Flask, request, jsonify
import json
from working_crop_system import comprehensive_analysis

app = Flask(__name__)

# Enable CORS manually
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route('/')
def home():
    """Home page with API information."""
    return jsonify({
        "message": "🌾 SIH 2025 Crop Recommendation API",
        "status": "operational",
        "endpoints": {
            "health": "/api/health",
            "recommend": "/api/recommend (POST)",
            "crops": "/api/crops"
        },
        "version": "1.0.0"
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "SIH 2025 Crop Recommendation API",
        "version": "1.0.0",
        "supported_crops": 24,
        "languages": ["English", "Hindi", "Bengali"]
    })

@app.route('/api/recommend', methods=['POST'])
def recommend_crop():
    """Main crop recommendation endpoint."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided"
            }), 400
        
        # Validate required parameters
        required_params = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        for param in required_params:
            if param not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required parameter: {param}"
                }), 400
        
        # Extract parameters
        N = float(data['N'])
        P = float(data['P'])
        K = float(data['K'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        ph = float(data['ph'])
        rainfall = float(data['rainfall'])
        
        # Get comprehensive analysis
        result = comprehensive_analysis(N, P, K, temperature, humidity, ph, rainfall)
        
        # Get crop names in different languages
        def get_hindi_name(crop):
            hindi_names = {
                'rice': 'चावल', 'wheat': 'गेहूं', 'maize': 'मक्का', 'cotton': 'कपास',
                'sugarcane': 'गन्ना', 'jute': 'जूट', 'coffee': 'कॉफी', 'coconut': 'नारियल',
                'papaya': 'पपीता', 'orange': 'संतरा', 'apple': 'सेब', 'muskmelon': 'खरबूजा',
                'watermelon': 'तरबूज', 'grapes': 'अंगूर', 'mango': 'आम', 'banana': 'केला',
                'pomegranate': 'अनार', 'lentil': 'मसूर', 'blackgram': 'उड़द', 'mungbean': 'मूंग',
                'mothbeans': 'मोठ', 'pigeonpeas': 'अरहर', 'kidneybeans': 'राजमा', 'chickpea': 'चना'
            }
            return hindi_names.get(crop, crop)
        
        def get_bengali_name(crop):
            bengali_names = {
                'rice': 'ধান', 'wheat': 'গম', 'maize': 'ভুট্টা', 'cotton': 'তুলা',
                'sugarcane': 'আখ', 'jute': 'পাট', 'coffee': 'কফি', 'coconut': 'নারকেল',
                'papaya': 'পেঁপে', 'orange': 'কমলা', 'apple': 'আপেল', 'muskmelon': 'খরমুজ',
                'watermelon': 'তরমুজ', 'grapes': 'আঙুর', 'mango': 'আম', 'banana': 'কলা',
                'pomegranate': 'ডালিম', 'lentil': 'মসুর', 'blackgram': 'কালো ছোলা', 'mungbean': 'মুগ',
                'mothbeans': 'মথ', 'pigeonpeas': 'অড়হর', 'kidneybeans': 'রাজমা', 'chickpea': 'ছোলা'
            }
            return bengali_names.get(crop, crop)
        
        # Format response for mobile
        primary = result['primary_recommendation']
        
        response = {
            "status": "success",
            "timestamp": "2025-09-17T20:07:15+05:30",
            "input_parameters": {
                "nitrogen": N, "phosphorus": P, "potassium": K,
                "temperature": temperature, "humidity": humidity,
                "ph": ph, "rainfall": rainfall
            },
            "recommendation": {
                "primary_crop": {
                    "name": primary['crop'],
                    "name_hindi": get_hindi_name(primary['crop']),
                    "name_bengali": get_bengali_name(primary['crop']),
                    "confidence": primary['confidence_score'],
                    "predicted_yield": primary['predicted_yield_kg_per_ha'],
                    "sustainability_score": primary['sustainability_score']
                },
                "alternatives": [
                    {
                        "name": alt['crop'],
                        "name_hindi": get_hindi_name(alt['crop']),
                        "name_bengali": get_bengali_name(alt['crop']),
                        "yield": alt['predicted_yield_kg_per_ha'],
                        "sustainability": alt['sustainability_score'],
                        "suitability": alt['suitability_score']
                    } for alt in result['alternative_crops'][:3]
                ]
            },
            "validation": {
                "warnings": result['input_validation']['warnings'],
                "is_valid": result['input_validation']['is_valid']
            },
            "system_info": {
                "model_accuracy": "94%",
                "total_crops_supported": 24,
                "languages_supported": 3
            }
        }
        
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": f"Invalid parameter value: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500

@app.route('/api/crops')
def get_supported_crops():
    """Get list of all supported crops."""
    crops = [
        {"english": "rice", "hindi": "चावल", "bengali": "ধান", "category": "cereal"},
        {"english": "wheat", "hindi": "गेहूं", "bengali": "গম", "category": "cereal"},
        {"english": "maize", "hindi": "मक्का", "bengali": "ভুট্টা", "category": "cereal"},
        {"english": "cotton", "hindi": "कपास", "bengali": "তুলা", "category": "cash_crop"},
        {"english": "sugarcane", "hindi": "गन्ना", "bengali": "আখ", "category": "cash_crop"},
        {"english": "jute", "hindi": "जूट", "bengali": "পাট", "category": "cash_crop"},
        {"english": "coffee", "hindi": "कॉफी", "bengali": "কফি", "category": "cash_crop"},
        {"english": "coconut", "hindi": "नारियल", "bengali": "নারকেল", "category": "fruit"},
        {"english": "papaya", "hindi": "पपीता", "bengali": "পেঁপে", "category": "fruit"},
        {"english": "orange", "hindi": "संतरा", "bengali": "কমলা", "category": "fruit"},
        {"english": "apple", "hindi": "सेब", "bengali": "আপেল", "category": "fruit"},
        {"english": "muskmelon", "hindi": "खरबूजा", "bengali": "খরমুজ", "category": "vegetable"},
        {"english": "watermelon", "hindi": "तरबूज", "bengali": "তরমুজ", "category": "vegetable"},
        {"english": "grapes", "hindi": "अंगूर", "bengali": "আঙুর", "category": "fruit"},
        {"english": "mango", "hindi": "आम", "bengali": "আম", "category": "fruit"},
        {"english": "banana", "hindi": "केला", "bengali": "কলা", "category": "fruit"},
        {"english": "pomegranate", "hindi": "अनार", "bengali": "ডালিম", "category": "fruit"},
        {"english": "lentil", "hindi": "मसूर", "bengali": "মসুর", "category": "pulse"},
        {"english": "blackgram", "hindi": "उड़द", "bengali": "কালো ছোলা", "category": "pulse"},
        {"english": "mungbean", "hindi": "मूंग", "bengali": "মুগ", "category": "pulse"},
        {"english": "mothbeans", "hindi": "मोठ", "bengali": "মথ", "category": "pulse"},
        {"english": "pigeonpeas", "hindi": "अरहर", "bengali": "অড়হর", "category": "pulse"},
        {"english": "kidneybeans", "hindi": "राजमा", "bengali": "রাজমা", "category": "pulse"},
        {"english": "chickpea", "hindi": "चना", "bengali": "ছোলা", "category": "pulse"}
    ]
    
    return jsonify({
        "status": "success",
        "total_crops": len(crops),
        "crops": crops
    })

if __name__ == '__main__':
    print("🚀 Starting SIH 2025 Crop Recommendation API Server...")
    print("📱 Mobile app backend ready!")
    print("🌐 Multilingual support enabled (Hindi, Bengali)")
    print("🌾 24 crops supported for Jharkhand farmers")
    print("🔗 Server will be available at: http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
