# SIH 2025 - Voice Interface for Crop Recommendation
# Speech Recognition and Text-to-Speech Integration

import speech_recognition as sr
import pyttsx3
import json
import threading
from working_crop_system import comprehensive_analysis

class VoiceInterface:
    """Voice interface for crop recommendation system."""
    
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Language support
        self.current_language = 'english'
        self.supported_languages = ['english', 'hindi']
        
        # Voice prompts in multiple languages
        self.prompts = {
            'english': {
                'welcome': "Welcome to the Smart Crop Recommendation System for Jharkhand farmers!",
                'ask_nitrogen': "Please tell me the nitrogen content in your soil in kg per hectare",
                'ask_phosphorus': "Please tell me the phosphorus content in kg per hectare",
                'ask_potassium': "Please tell me the potassium content in kg per hectare",
                'ask_temperature': "What is the average temperature in Celsius?",
                'ask_humidity': "What is the humidity percentage?",
                'ask_ph': "What is the pH level of your soil?",
                'ask_rainfall': "What is the annual rainfall in millimeters?",
                'processing': "Processing your soil and climate data...",
                'recommendation': "Based on your conditions, I recommend growing {crop}",
                'yield_info': "Expected yield is {yield} kilograms per hectare",
                'sustainability': "Sustainability score is {score} out of 10",
                'alternatives': "Alternative crops you can consider are: {crops}",
                'error': "Sorry, I couldn't understand. Please try again.",
                'goodbye': "Thank you for using the Smart Crop Recommendation System!"
            },
            'hindi': {
                'welcome': "झारखंड के किसानों के लिए स्मार्ट फसल सिफारिश प्रणाली में आपका स्वागत है!",
                'ask_nitrogen': "कृपया अपनी मिट्टी में नाइट्रोजन की मात्रा किलोग्राम प्रति हेक्टेयर में बताएं",
                'ask_phosphorus': "कृपया फास्फोरस की मात्रा किलोग्राम प्रति हेक्टेयर में बताएं",
                'ask_potassium': "कृपया पोटेशियम की मात्रा किलोग्राम प्रति हेक्टेयर में बताएं",
                'ask_temperature': "औसत तापमान सेल्सियस में क्या है?",
                'ask_humidity': "आर्द्रता का प्रतिशत क्या है?",
                'ask_ph': "आपकी मिट्टी का पीएच स्तर क्या है?",
                'ask_rainfall': "वार्षिक वर्षा मिलीमीटर में क्या है?",
                'processing': "आपकी मिट्टी और जलवायु डेटा को प्रोसेस कर रहे हैं...",
                'recommendation': "आपकी स्थितियों के आधार पर, मैं {crop} उगाने की सिफारिश करता हूं",
                'yield_info': "अपेक्षित उत्पादन {yield} किलोग्राम प्रति हेक्टेयर है",
                'sustainability': "स्थिरता स्कोर 10 में से {score} है",
                'alternatives': "वैकल्पिक फसलें जिन पर आप विचार कर सकते हैं: {crops}",
                'error': "माफ करें, मैं समझ नहीं सका। कृपया फिर से कोशिश करें।",
                'goodbye': "स्मार्ट फसल सिफारिश प्रणाली का उपयोग करने के लिए धन्यवाद!"
            }
        }
        
    def setup_tts(self):
        """Setup text-to-speech engine."""
        voices = self.tts_engine.getProperty('voices')
        # Set voice properties
        self.tts_engine.setProperty('rate', 150)  # Speed
        self.tts_engine.setProperty('volume', 0.9)  # Volume
        
        # Try to set a female voice if available
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
    
    def speak(self, text):
        """Convert text to speech."""
        print(f"🗣️ Speaking: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self, timeout=5):
        """Listen for voice input."""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout)
            
            print("🔄 Processing speech...")
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            print(f"👂 Heard: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            print("⏰ Listening timeout")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Error with speech recognition service: {e}")
            return None
    
    def extract_number(self, text):
        """Extract number from spoken text."""
        # Convert word numbers to digits
        word_to_num = {
            'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
            'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
            'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70,
            'eighty': 80, 'ninety': 90, 'hundred': 100
        }
        
        # Try to find digits in text
        words = text.split()
        for word in words:
            # Check for direct digits
            try:
                return float(word)
            except ValueError:
                pass
            
            # Check for word numbers
            if word in word_to_num:
                return float(word_to_num[word])
        
        return None
    
    def get_voice_input(self, prompt_key, retries=3):
        """Get voice input for a specific parameter."""
        prompt = self.prompts[self.current_language][prompt_key]
        
        for attempt in range(retries):
            self.speak(prompt)
            response = self.listen()
            
            if response:
                number = self.extract_number(response)
                if number is not None:
                    return number
            
            if attempt < retries - 1:
                error_msg = self.prompts[self.current_language]['error']
                self.speak(error_msg)
        
        return None
    
    def voice_crop_recommendation(self):
        """Complete voice-based crop recommendation flow."""
        try:
            # Welcome message
            welcome_msg = self.prompts[self.current_language]['welcome']
            self.speak(welcome_msg)
            
            # Collect parameters via voice
            parameters = {}
            param_prompts = [
                ('N', 'ask_nitrogen'),
                ('P', 'ask_phosphorus'),
                ('K', 'ask_potassium'),
                ('temperature', 'ask_temperature'),
                ('humidity', 'ask_humidity'),
                ('ph', 'ask_ph'),
                ('rainfall', 'ask_rainfall')
            ]
            
            for param_name, prompt_key in param_prompts:
                value = self.get_voice_input(prompt_key)
                if value is None:
                    self.speak("Sorry, I couldn't get all the required information. Please try again.")
                    return None
                parameters[param_name] = value
                print(f"✅ {param_name}: {value}")
            
            # Processing message
            processing_msg = self.prompts[self.current_language]['processing']
            self.speak(processing_msg)
            
            # Get recommendation
            result = comprehensive_analysis(
                parameters['N'], parameters['P'], parameters['K'],
                parameters['temperature'], parameters['humidity'],
                parameters['ph'], parameters['rainfall']
            )
            
            if 'error' in result['primary_recommendation']:
                self.speak("Sorry, there was an error processing your request.")
                return None
            
            # Announce results
            primary = result['primary_recommendation']
            
            # Main recommendation
            crop_name = primary['crop']
            if self.current_language == 'hindi':
                crop_name = self.get_hindi_crop_name(crop_name)
            
            rec_msg = self.prompts[self.current_language]['recommendation'].format(crop=crop_name)
            self.speak(rec_msg)
            
            # Yield information
            yield_msg = self.prompts[self.current_language]['yield_info'].format(
                yield=int(primary['predicted_yield_kg_per_ha'])
            )
            self.speak(yield_msg)
            
            # Sustainability score
            sust_msg = self.prompts[self.current_language]['sustainability'].format(
                score=round(primary['sustainability_score'], 1)
            )
            self.speak(sust_msg)
            
            # Alternative crops
            alternatives = [alt['crop'] for alt in result['alternative_crops'][:2]]
            if self.current_language == 'hindi':
                alternatives = [self.get_hindi_crop_name(crop) for crop in alternatives]
            
            alt_msg = self.prompts[self.current_language]['alternatives'].format(
                crops=', '.join(alternatives)
            )
            self.speak(alt_msg)
            
            # Goodbye message
            goodbye_msg = self.prompts[self.current_language]['goodbye']
            self.speak(goodbye_msg)
            
            return result
            
        except Exception as e:
            print(f"❌ Error in voice recommendation: {e}")
            self.speak("Sorry, there was a technical error. Please try again.")
            return None
    
    def get_hindi_crop_name(self, crop):
        """Get Hindi name for crop."""
        hindi_names = {
            'rice': 'चावल', 'wheat': 'गेहूं', 'maize': 'मक्का', 'cotton': 'कपास',
            'sugarcane': 'गन्ना', 'jute': 'जूट', 'coffee': 'कॉफी', 'coconut': 'नारियल',
            'papaya': 'पपीता', 'orange': 'संतरा', 'apple': 'सेब', 'muskmelon': 'खरबूजा',
            'watermelon': 'तरबूज', 'grapes': 'अंगूर', 'mango': 'आम', 'banana': 'केला',
            'pomegranate': 'अनार', 'lentil': 'मसूर', 'blackgram': 'उड़द', 'mungbean': 'मूंग',
            'mothbeans': 'मोठ', 'pigeonpeas': 'अरहर', 'kidneybeans': 'राजमा', 'chickpea': 'चना'
        }
        return hindi_names.get(crop, crop)
    
    def set_language(self, language):
        """Set the interface language."""
        if language in self.supported_languages:
            self.current_language = language
            print(f"🌐 Language set to: {language}")
        else:
            print(f"❌ Language {language} not supported")

# Demo function
def demo_voice_interface():
    """Demo the voice interface (without actual speech recognition)."""
    print("🎤 Voice Interface Demo - SIH 2025")
    print("=" * 50)
    
    # Simulate voice interface without actual speech recognition
    voice = VoiceInterface()
    
    print("🗣️ Demo: Voice prompts in English and Hindi")
    print("\n📢 English prompts:")
    for key, prompt in voice.prompts['english'].items():
        if 'ask_' in key:
            print(f"   {prompt}")
    
    print("\n📢 Hindi prompts:")
    for key, prompt in voice.prompts['hindi'].items():
        if 'ask_' in key:
            print(f"   {prompt}")
    
    print("\n✅ Voice interface ready for integration!")
    print("📱 Can be integrated with mobile app for hands-free operation")
    print("🌐 Supports English and Hindi languages")
    print("🎯 Perfect for Jharkhand farmers who prefer voice interaction")

if __name__ == "__main__":
    # Run demo (actual voice features require microphone and internet)
    demo_voice_interface()
    
    # Uncomment below to test actual voice interface (requires microphone)
    # voice_interface = VoiceInterface()
    # result = voice_interface.voice_crop_recommendation()
