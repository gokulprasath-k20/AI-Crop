# 📱 React Native Integration Guide - SIH 2025 Crop Recommendation

## 🎯 **WHERE TO USE THE REACT NATIVE CODE**

### **Option 1: New React Native App**

#### **Step 1: Create New App**
```bash
npx react-native init SIH2025CropApp
cd SIH2025CropApp
```

#### **Step 2: Create Screen File**
Create: `src/screens/CropRecommendationScreen.js`
```javascript
// Paste your React Native code here
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert } from 'react-native';

const CropRecommendationScreen = () => {
  // Your existing code...
};

export default CropRecommendationScreen;
```

#### **Step 3: Update App.js**
```javascript
import React from 'react';
import { SafeAreaView } from 'react-native';
import CropRecommendationScreen from './src/screens/CropRecommendationScreen';

const App = () => {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <CropRecommendationScreen />
    </SafeAreaView>
  );
};

export default App;
```

### **Option 2: Existing React Native App**

#### **Add as New Screen**
```javascript
// In your navigation setup (React Navigation)
import CropRecommendationScreen from './screens/CropRecommendationScreen';

const Stack = createStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen 
          name="CropRecommendation" 
          component={CropRecommendationScreen}
          options={{ title: '🌾 Crop Recommendation' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### **Option 3: Expo App**

#### **Step 1: Create Expo App**
```bash
npx create-expo-app SIH2025CropApp
cd SIH2025CropApp
```

#### **Step 2: Replace App.js**
```javascript
import React from 'react';
import CropRecommendationScreen from './CropRecommendationScreen';

export default function App() {
  return <CropRecommendationScreen />;
}
```

## 🔧 **COMPLETE IMPLEMENTATION**

### **Enhanced Version with All Input Fields**
```javascript
import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  Alert,
  ScrollView,
  StyleSheet,
  ActivityIndicator
} from 'react-native';

const CropRecommendationScreen = () => {
  const [soilData, setSoilData] = useState({
    nitrogen: '90',
    phosphorus: '42',
    potassium: '43',
    temperature: '21',
    humidity: '82',
    ph: '6.5',
    rainfall: '203'
  });
  const [recommendation, setRecommendation] = useState(null);
  const [alternatives, setAlternatives] = useState([]);
  const [loading, setLoading] = useState(false);

  const updateSoilData = (field, value) => {
    setSoilData(prev => ({ ...prev, [field]: value }));
  };

  const getCropRecommendation = async () => {
    setLoading(true);
    try {
      // Update with your actual deployed URL
      const response = await fetch('https://your-app-name.onrender.com/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          N: parseFloat(soilData.nitrogen),
          P: parseFloat(soilData.phosphorus),
          K: parseFloat(soilData.potassium),
          temperature: parseFloat(soilData.temperature),
          humidity: parseFloat(soilData.humidity),
          ph: parseFloat(soilData.ph),
          rainfall: parseFloat(soilData.rainfall)
        })
      });

      const result = await response.json();
      
      if (result.status === 'success') {
        setRecommendation(result.recommendation.primary_crop);
        setAlternatives(result.recommendation.alternative_crops || []);
        
        Alert.alert(
          '🎉 Recommendation Ready!',
          `Best crop: ${result.recommendation.primary_crop.name_hindi} (${result.recommendation.primary_crop.name_english})\n\nExpected Yield: ${result.recommendation.primary_crop.predicted_yield_kg_per_ha.toLocaleString()} kg/ha`
        );
      } else {
        Alert.alert('❌ Error', result.message);
      }
    } catch (error) {
      Alert.alert('🌐 Network Error', 'Please check your internet connection and API URL');
    } finally {
      setLoading(false);
    }
  };

  const InputField = ({ label, field, placeholder, unit }) => (
    <View style={styles.inputGroup}>
      <Text style={styles.label}>{label}</Text>
      <View style={styles.inputContainer}>
        <TextInput
          placeholder={placeholder}
          value={soilData[field]}
          onChangeText={(text) => updateSoilData(field, text)}
          style={styles.input}
          keyboardType="numeric"
        />
        <Text style={styles.unit}>{unit}</Text>
      </View>
    </View>
  );

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>🌾 SIH 2025 Crop Recommendation</Text>
        <Text style={styles.subtitle}>AI-Powered Crop Selection for Jharkhand Farmers</Text>
      </View>

      <View style={styles.form}>
        <Text style={styles.sectionTitle}>📊 Soil Test Results</Text>
        <InputField 
          label="🧪 Nitrogen (N)" 
          field="nitrogen" 
          placeholder="Enter nitrogen content"
          unit="kg/ha"
        />
        <InputField 
          label="🧪 Phosphorus (P)" 
          field="phosphorus" 
          placeholder="Enter phosphorus content"
          unit="kg/ha"
        />
        <InputField 
          label="🧪 Potassium (K)" 
          field="potassium" 
          placeholder="Enter potassium content"
          unit="kg/ha"
        />

        <Text style={styles.sectionTitle}>🌤️ Climate Data</Text>
        <InputField 
          label="🌡️ Temperature" 
          field="temperature" 
          placeholder="Average temperature"
          unit="°C"
        />
        <InputField 
          label="💧 Humidity" 
          field="humidity" 
          placeholder="Relative humidity"
          unit="%"
        />
        <InputField 
          label="🌧️ Rainfall" 
          field="rainfall" 
          placeholder="Annual rainfall"
          unit="mm"
        />

        <Text style={styles.sectionTitle}>⚗️ Soil Properties</Text>
        <InputField 
          label="⚗️ pH Level" 
          field="ph" 
          placeholder="Soil pH level"
          unit=""
        />
      </View>

      <TouchableOpacity
        onPress={getCropRecommendation}
        disabled={loading}
        style={[styles.button, loading && styles.buttonDisabled]}
      >
        {loading ? (
          <ActivityIndicator color="white" />
        ) : (
          <Text style={styles.buttonText}>🌾 Get AI Crop Recommendation</Text>
        )}
      </TouchableOpacity>

      {recommendation && (
        <View style={styles.results}>
          <Text style={styles.resultsTitle}>🎯 AI Recommendation</Text>
          
          <View style={styles.cropCard}>
            <Text style={styles.cropName}>
              {recommendation.name_hindi} ({recommendation.name_english})
            </Text>
            <Text style={styles.cropDetail}>
              📈 Expected Yield: {recommendation.predicted_yield_kg_per_ha.toLocaleString()} kg/ha
            </Text>
            <Text style={styles.cropDetail}>
              🌱 Sustainability: {recommendation.sustainability_score}/10
            </Text>
            <Text style={styles.cropDetail}>
              🎯 Confidence: {(recommendation.confidence * 100).toFixed(1)}%
            </Text>
          </View>

          {alternatives.length > 0 && (
            <View style={styles.alternatives}>
              <Text style={styles.alternativesTitle}>🔄 Alternative Options</Text>
              {alternatives.slice(0, 2).map((alt, index) => (
                <View key={index} style={styles.altCard}>
                  <Text style={styles.altName}>
                    {index + 1}. {alt.name_hindi} ({alt.name_english})
                  </Text>
                  <Text style={styles.altDetail}>
                    Yield: {alt.predicted_yield_kg_per_ha.toLocaleString()} kg/ha
                  </Text>
                </View>
              ))}
            </View>
          )}
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f0f8ff',
  },
  header: {
    backgroundColor: '#2e8b57',
    padding: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#e8f5e8',
    textAlign: 'center',
    marginTop: 5,
  },
  form: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2e8b57',
    marginTop: 20,
    marginBottom: 15,
  },
  inputGroup: {
    marginBottom: 15,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 5,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'white',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  input: {
    flex: 1,
    padding: 12,
    fontSize: 16,
  },
  unit: {
    paddingRight: 12,
    color: '#666',
    fontSize: 14,
  },
  button: {
    backgroundColor: '#2e8b57',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    margin: 20,
  },
  buttonDisabled: {
    backgroundColor: '#999',
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  results: {
    margin: 20,
  },
  resultsTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2e8b57',
    marginBottom: 15,
  },
  cropCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 10,
    borderLeftWidth: 5,
    borderLeftColor: '#2e8b57',
    marginBottom: 15,
  },
  cropName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2e8b57',
    marginBottom: 10,
  },
  cropDetail: {
    fontSize: 16,
    color: '#333',
    marginBottom: 5,
  },
  alternatives: {
    marginTop: 10,
  },
  alternativesTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2e8b57',
    marginBottom: 10,
  },
  altCard: {
    backgroundColor: '#f8f8f8',
    padding: 15,
    borderRadius: 8,
    marginBottom: 10,
  },
  altName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  altDetail: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
});

export default CropRecommendationScreen;
```

## 🚀 **DEPLOYMENT STEPS**

### **1. Update API URL**
Replace `'https://your-app-name.onrender.com'` with your actual deployed URL

### **2. Install Dependencies**
```bash
npm install @react-navigation/native @react-navigation/stack
```

### **3. Run the App**
```bash
# For iOS
npx react-native run-ios

# For Android
npx react-native run-android

# For Expo
expo start
```

## 📱 **USAGE SCENARIOS**

### **1. Standalone Farming App**
- Main screen for crop recommendations
- Perfect for farmer-focused mobile apps

### **2. Agricultural Portal**
- Part of larger agricultural management system
- Integration with other farming tools

### **3. Government App**
- Integration with government agricultural schemes
- Part of digital India initiatives

### **4. NGO/Cooperative Apps**
- Farmer support applications
- Rural development programs

## 🎯 **CUSTOMIZATION OPTIONS**

### **Add More Features:**
- GPS location for automatic climate data
- Camera integration for soil image analysis
- Offline mode with local storage
- Multi-language support (Hindi, Bengali)
- Voice input for illiterate farmers

### **Styling:**
- Custom themes for different regions
- Accessibility features
- Dark mode support
- Responsive design for tablets

## 🌾 **PERFECT FOR SIH 2025!**

This React Native component is:
- ✅ **Mobile-First** - Designed for smartphones
- ✅ **Farmer-Friendly** - Simple, clear interface
- ✅ **AI-Powered** - Uses your deployed API
- ✅ **Production-Ready** - Error handling included
- ✅ **Scalable** - Easy to extend and customize

**Your SIH 2025 mobile app is ready to serve farmers across Jharkhand! 🚀**
