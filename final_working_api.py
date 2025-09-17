# SIH 2025 - Final Working API
from flask import Flask, request, jsonify
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our working system
try:
    from working_crop_system import comprehensive_analysis
    SYSTEM_AVAILABLE = True
except ImportError:
    SYSTEM_AVAILABLE = False

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "🌾 SIH 2025 Crop Recommendation API",
        "status": "operational",
        "system_available": SYSTEM_AVAILABLE,
        "endpoints": ["/api/health", "/api/recommend", "/api/test"],
        "version": "1.0.0"
    })

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "SIH 2025 Crop Recommendation",
        "system_ready": SYSTEM_AVAILABLE,
        "crops_supported": 24,
        "languages": ["English", "Hindi", "Bengali"]
    })

@app.route('/api/test')
def test():
    if not SYSTEM_AVAILABLE:
        return jsonify({"error": "Core system not available"}), 500
    
    try:
        # Test with sample data
        result = comprehensive_analysis(90, 42, 43, 21, 82, 6.5, 203)
        primary = result['primary_recommendation']
        
        return jsonify({
            "status": "success",
            "test_result": {
                "crop": primary['crop'],
                "yield": primary['predicted_yield_kg_per_ha'],
                "sustainability": primary['sustainability_score']
            },
            "message": "System working perfectly!"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend():
    if not SYSTEM_AVAILABLE:
        return jsonify({"error": "Core system not available"}), 500
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract parameters
        N = float(data.get('N', 90))
        P = float(data.get('P', 42))
        K = float(data.get('K', 43))
        temperature = float(data.get('temperature', 21))
        humidity = float(data.get('humidity', 82))
        ph = float(data.get('ph', 6.5))
        rainfall = float(data.get('rainfall', 203))
        
        # Get recommendation
        result = comprehensive_analysis(N, P, K, temperature, humidity, ph, rainfall)
        
        # Hindi names
        hindi_names = {
            'rice': 'चावल', 'wheat': 'गेहूं', 'maize': 'मक्का', 'cotton': 'कपास',
            'mango': 'आम', 'banana': 'केला', 'apple': 'सेब', 'orange': 'संतरा'
        }
        
        primary = result['primary_recommendation']
        crop_name = primary['crop']
        
        response = {
            "status": "success",
            "recommendation": {
                "crop_english": crop_name,
                "crop_hindi": hindi_names.get(crop_name, crop_name),
                "predicted_yield": primary['predicted_yield_kg_per_ha'],
                "sustainability_score": primary['sustainability_score'],
                "confidence": primary['confidence_score']
            },
            "alternatives": [
                {
                    "crop": alt['crop'],
                    "yield": alt['predicted_yield_kg_per_ha'],
                    "sustainability": alt['sustainability_score']
                } for alt in result['alternative_crops'][:3]
            ]
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 SIH 2025 Final Working API")
    print(f"System Available: {SYSTEM_AVAILABLE}")
    print("Starting server on port 5002...")
    app.run(host='127.0.0.1', port=5002, debug=False)
