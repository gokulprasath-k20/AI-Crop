# SIH 2025 - Multilingual Support System
# Hindi, Bengali, and English language support

import json
from typing import Dict, List

class MultilingualSupport:
    """Comprehensive multilingual support for the crop recommendation system."""
    
    def __init__(self):
        self.supported_languages = ['english', 'hindi', 'bengali']
        self.current_language = 'english'
        
        # Complete translations
        self.translations = {
            'english': {
                # UI Elements
                'app_title': 'Smart Crop Recommendation System',
                'welcome_message': 'Welcome to the Smart Crop Recommendation System for Jharkhand farmers!',
                'input_parameters': 'Input Parameters',
                'results': 'Recommendation Results',
                'alternatives': 'Alternative Crops',
                
                # Parameter Labels
                'nitrogen': 'Nitrogen (N)',
                'phosphorus': 'Phosphorus (P)',
                'potassium': 'Potassium (K)',
                'temperature': 'Temperature',
                'humidity': 'Humidity',
                'ph_level': 'pH Level',
                'rainfall': 'Rainfall',
                
                # Units
                'kg_per_hectare': 'kg/hectare',
                'celsius': '°C',
                'percentage': '%',
                'millimeters': 'mm',
                
                # Results
                'recommended_crop': 'Recommended Crop',
                'predicted_yield': 'Predicted Yield',
                'sustainability_score': 'Sustainability Score',
                'confidence_level': 'Confidence Level',
                
                # Actions
                'get_recommendation': 'Get Recommendation',
                'clear_inputs': 'Clear Inputs',
                'voice_input': 'Voice Input',
                'save_results': 'Save Results',
                
                # Messages
                'processing': 'Processing your data...',
                'success': 'Recommendation generated successfully!',
                'error': 'Error occurred. Please check your inputs.',
                'invalid_input': 'Please enter valid values for all parameters.',
                
                # Crop Categories
                'cereals': 'Cereals',
                'pulses': 'Pulses',
                'cash_crops': 'Cash Crops',
                'fruits': 'Fruits',
                'vegetables': 'Vegetables',
                
                # Help Text
                'help_nitrogen': 'Nitrogen content in soil (typical range: 0-200 kg/ha)',
                'help_phosphorus': 'Phosphorus content in soil (typical range: 0-150 kg/ha)',
                'help_potassium': 'Potassium content in soil (typical range: 0-300 kg/ha)',
                'help_temperature': 'Average temperature (typical range: 15-35°C)',
                'help_humidity': 'Relative humidity percentage (0-100%)',
                'help_ph': 'Soil pH level (typical range: 4-9)',
                'help_rainfall': 'Annual rainfall in millimeters (typical range: 200-2000mm)'
            },
            
            'hindi': {
                # UI Elements
                'app_title': 'स्मार्ट फसल सिफारिश प्रणाली',
                'welcome_message': 'झारखंड के किसानों के लिए स्मार्ट फसल सिफारिश प्रणाली में आपका स्वागत है!',
                'input_parameters': 'इनपुट पैरामीटर',
                'results': 'सिफारिश परिणाम',
                'alternatives': 'वैकल्पिक फसलें',
                
                # Parameter Labels
                'nitrogen': 'नाइट्रोजन (N)',
                'phosphorus': 'फास्फोरस (P)',
                'potassium': 'पोटेशियम (K)',
                'temperature': 'तापमान',
                'humidity': 'आर्द्रता',
                'ph_level': 'पीएच स्तर',
                'rainfall': 'वर्षा',
                
                # Units
                'kg_per_hectare': 'किग्रा/हेक्टेयर',
                'celsius': '°सेल्सियस',
                'percentage': '%',
                'millimeters': 'मिमी',
                
                # Results
                'recommended_crop': 'सुझाई गई फसल',
                'predicted_yield': 'अनुमानित उत्पादन',
                'sustainability_score': 'स्थिरता स्कोर',
                'confidence_level': 'विश्वास स्तर',
                
                # Actions
                'get_recommendation': 'सिफारिश प्राप्त करें',
                'clear_inputs': 'इनपुट साफ़ करें',
                'voice_input': 'आवाज़ इनपुट',
                'save_results': 'परिणाम सहेजें',
                
                # Messages
                'processing': 'आपका डेटा प्रोसेस कर रहे हैं...',
                'success': 'सिफारिश सफलतापूर्वक तैयार की गई!',
                'error': 'त्रुटि हुई। कृपया अपने इनपुट जांचें।',
                'invalid_input': 'कृपया सभी पैरामीटर के लिए मान्य मान दर्ज करें।',
                
                # Crop Categories
                'cereals': 'अनाज',
                'pulses': 'दालें',
                'cash_crops': 'नकदी फसलें',
                'fruits': 'फल',
                'vegetables': 'सब्जियां',
                
                # Help Text
                'help_nitrogen': 'मिट्टी में नाइट्रोजन की मात्रा (सामान्य सीमा: 0-200 किग्रा/हेक्टेयर)',
                'help_phosphorus': 'मिट्टी में फास्फोरस की मात्रा (सामान्य सीमा: 0-150 किग्रा/हेक्टेयर)',
                'help_potassium': 'मिट्टी में पोटेशियम की मात्रा (सामान्य सीमा: 0-300 किग्रा/हेक्टेयर)',
                'help_temperature': 'औसत तापमान (सामान्य सीमा: 15-35°सेल्सियस)',
                'help_humidity': 'सापेक्ष आर्द्रता प्रतिशत (0-100%)',
                'help_ph': 'मिट्टी का पीएच स्तर (सामान्य सीमा: 4-9)',
                'help_rainfall': 'वार्षिक वर्षा मिलीमीटर में (सामान्य सीमा: 200-2000मिमी)'
            },
            
            'bengali': {
                # UI Elements
                'app_title': 'স্মার্ট ফসল সুপারিশ সিস্টেম',
                'welcome_message': 'ঝাড়খণ্ডের কৃষকদের জন্য স্মার্ট ফসল সুপারিশ সিস্টেমে আপনাকে স্বাগতম!',
                'input_parameters': 'ইনপুট প্যারামিটার',
                'results': 'সুপারিশ ফলাফল',
                'alternatives': 'বিকল্প ফসল',
                
                # Parameter Labels
                'nitrogen': 'নাইট্রোজেন (N)',
                'phosphorus': 'ফসফরাস (P)',
                'potassium': 'পটাসিয়াম (K)',
                'temperature': 'তাপমাত্রা',
                'humidity': 'আর্দ্রতা',
                'ph_level': 'পিএইচ স্তর',
                'rainfall': 'বৃষ্টিপাত',
                
                # Units
                'kg_per_hectare': 'কেজি/হেক্টর',
                'celsius': '°সেলসিয়াস',
                'percentage': '%',
                'millimeters': 'মিমি',
                
                # Results
                'recommended_crop': 'প্রস্তাবিত ফসল',
                'predicted_yield': 'প্রত্যাশিত ফলন',
                'sustainability_score': 'স্থায়িত্ব স্কোর',
                'confidence_level': 'আত্মবিশ্বাসের স্তর',
                
                # Actions
                'get_recommendation': 'সুপারিশ পান',
                'clear_inputs': 'ইনপুট পরিষ্কার করুন',
                'voice_input': 'ভয়েস ইনপুট',
                'save_results': 'ফলাফল সংরক্ষণ করুন',
                
                # Messages
                'processing': 'আপনার ডেটা প্রক্রিয়া করা হচ্ছে...',
                'success': 'সুপারিশ সফলভাবে তৈরি হয়েছে!',
                'error': 'ত্রুটি ঘটেছে। আপনার ইনপুট পরীক্ষা করুন।',
                'invalid_input': 'সমস্ত প্যারামিটারের জন্য বৈধ মান প্রবেশ করান।',
                
                # Crop Categories
                'cereals': 'শস্য',
                'pulses': 'ডাল',
                'cash_crops': 'অর্থকরী ফসল',
                'fruits': 'ফল',
                'vegetables': 'সবজি',
                
                # Help Text
                'help_nitrogen': 'মাটিতে নাইট্রোজেনের পরিমাণ (সাধারণ সীমা: 0-200 কেজি/হেক্টর)',
                'help_phosphorus': 'মাটিতে ফসফরাসের পরিমাণ (সাধারণ সীমা: 0-150 কেজি/হেক্টর)',
                'help_potassium': 'মাটিতে পটাসিয়ামের পরিমাণ (সাধারণ সীমা: 0-300 কেজি/হেক্টর)',
                'help_temperature': 'গড় তাপমাত্রা (সাধারণ সীমা: 15-35°সেলসিয়াস)',
                'help_humidity': 'আপেক্ষিক আর্দ্রতার শতাংশ (0-100%)',
                'help_ph': 'মাটির পিএইচ স্তর (সাধারণ সীমা: 4-9)',
                'help_rainfall': 'বার্ষিক বৃষ্টিপাত মিলিমিটারে (সাধারণ সীমা: 200-2000মিমি)'
            }
        }
        
        # Crop names in different languages
        self.crop_names = {
            'english': {
                'rice': 'Rice', 'wheat': 'Wheat', 'maize': 'Maize', 'cotton': 'Cotton',
                'sugarcane': 'Sugarcane', 'jute': 'Jute', 'coffee': 'Coffee', 'coconut': 'Coconut',
                'papaya': 'Papaya', 'orange': 'Orange', 'apple': 'Apple', 'muskmelon': 'Muskmelon',
                'watermelon': 'Watermelon', 'grapes': 'Grapes', 'mango': 'Mango', 'banana': 'Banana',
                'pomegranate': 'Pomegranate', 'lentil': 'Lentil', 'blackgram': 'Black Gram',
                'mungbean': 'Mung Bean', 'mothbeans': 'Moth Beans', 'pigeonpeas': 'Pigeon Peas',
                'kidneybeans': 'Kidney Beans', 'chickpea': 'Chickpea'
            },
            'hindi': {
                'rice': 'चावल', 'wheat': 'गेहूं', 'maize': 'मक्का', 'cotton': 'कपास',
                'sugarcane': 'गन्ना', 'jute': 'जूट', 'coffee': 'कॉफी', 'coconut': 'नारियल',
                'papaya': 'पपीता', 'orange': 'संतरा', 'apple': 'सेब', 'muskmelon': 'खरबूजा',
                'watermelon': 'तरबूज', 'grapes': 'अंगूर', 'mango': 'आम', 'banana': 'केला',
                'pomegranate': 'अनार', 'lentil': 'मसूर', 'blackgram': 'उड़द',
                'mungbean': 'मूंग', 'mothbeans': 'मोठ', 'pigeonpeas': 'अरहर',
                'kidneybeans': 'राजमा', 'chickpea': 'चना'
            },
            'bengali': {
                'rice': 'ধান', 'wheat': 'গম', 'maize': 'ভুট্টা', 'cotton': 'তুলা',
                'sugarcane': 'আখ', 'jute': 'পাট', 'coffee': 'কফি', 'coconut': 'নারকেল',
                'papaya': 'পেঁপে', 'orange': 'কমলা', 'apple': 'আপেল', 'muskmelon': 'খরমুজ',
                'watermelon': 'তরমুজ', 'grapes': 'আঙুর', 'mango': 'আম', 'banana': 'কলা',
                'pomegranate': 'ডালিম', 'lentil': 'মসুর', 'blackgram': 'কালো ছোলা',
                'mungbean': 'মুগ', 'mothbeans': 'মথ', 'pigeonpeas': 'অড়হর',
                'kidneybeans': 'রাজমা', 'chickpea': 'ছোলা'
            }
        }
    
    def set_language(self, language: str) -> bool:
        """Set the current language."""
        if language in self.supported_languages:
            self.current_language = language
            return True
        return False
    
    def get_text(self, key: str) -> str:
        """Get translated text for a key."""
        return self.translations[self.current_language].get(key, key)
    
    def get_crop_name(self, crop: str) -> str:
        """Get crop name in current language."""
        return self.crop_names[self.current_language].get(crop, crop)
    
    def translate_result(self, result: Dict) -> Dict:
        """Translate recommendation result to current language."""
        if 'error' in result:
            return result
        
        translated_result = {
            'status': 'success',
            'language': self.current_language,
            'primary_recommendation': {
                'crop_english': result['crop'],
                'crop_local': self.get_crop_name(result['crop']),
                'predicted_yield_kg_per_ha': result['predicted_yield_kg_per_ha'],
                'sustainability_score': result['sustainability_score'],
                'confidence_score': result.get('confidence_score', 0)
            },
            'ui_text': {
                'recommended_crop': self.get_text('recommended_crop'),
                'predicted_yield': self.get_text('predicted_yield'),
                'sustainability_score': self.get_text('sustainability_score'),
                'kg_per_hectare': self.get_text('kg_per_hectare')
            }
        }
        
        return translated_result
    
    def get_ui_config(self) -> Dict:
        """Get complete UI configuration for current language."""
        return {
            'language': self.current_language,
            'texts': self.translations[self.current_language],
            'crop_names': self.crop_names[self.current_language]
        }
    
    def export_translations(self, filename: str = None) -> str:
        """Export translations to JSON file."""
        if filename is None:
            filename = f"translations_{self.current_language}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.translations, f, ensure_ascii=False, indent=2)
        
        return filename

# Global multilingual instance
ml_support = MultilingualSupport()

def get_localized_interface(language='english'):
    """Get localized interface configuration."""
    ml_support.set_language(language)
    return ml_support.get_ui_config()

def translate_recommendation(result, language='english'):
    """Translate recommendation result."""
    ml_support.set_language(language)
    return ml_support.translate_result(result)

# Demo function
def demo_multilingual():
    """Demo multilingual support."""
    print("🌐 Multilingual Support Demo - SIH 2025")
    print("=" * 50)
    
    # Test all languages
    for lang in ['english', 'hindi', 'bengali']:
        print(f"\n📢 {lang.upper()} Interface:")
        ml_support.set_language(lang)
        
        print(f"   Title: {ml_support.get_text('app_title')}")
        print(f"   Welcome: {ml_support.get_text('welcome_message')}")
        print(f"   Button: {ml_support.get_text('get_recommendation')}")
        
        # Show some crop names
        print(f"   Crops: {ml_support.get_crop_name('rice')}, {ml_support.get_crop_name('wheat')}, {ml_support.get_crop_name('mango')}")
    
    print(f"\n✅ Multilingual support ready!")
    print(f"🌐 Supports: {', '.join(ml_support.supported_languages)}")
    print(f"📱 Perfect for diverse farmer communities in Jharkhand")

if __name__ == "__main__":
    demo_multilingual()
