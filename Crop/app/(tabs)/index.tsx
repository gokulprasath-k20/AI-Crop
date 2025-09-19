import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  ScrollView, 
  StyleSheet, 
  Alert,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import apiService, { SoilData, ApiResponse } from '../../services/apiService';

interface FormData {
  N: string;
  P: string;
  K: string;
  temperature: string;
  humidity: string;
  ph: string;
  rainfall: string;
}

export default function HomeScreen() {
  const [formData, setFormData] = useState<FormData>({
    N: '',
    P: '',
    K: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [recommendation, setRecommendation] = useState<ApiResponse | null>(null);
  const [showResults, setShowResults] = useState(false);

  const inputFields = [
    { key: 'N', label: 'Nitrogen (N)', unit: 'kg/ha', icon: 'leaf-outline', placeholder: 'e.g., 90' },
    { key: 'P', label: 'Phosphorus (P)', unit: 'kg/ha', icon: 'flask-outline', placeholder: 'e.g., 42' },
    { key: 'K', label: 'Potassium (K)', unit: 'kg/ha', icon: 'diamond-outline', placeholder: 'e.g., 43' },
    { key: 'temperature', label: 'Temperature', unit: '°C', icon: 'thermometer-outline', placeholder: 'e.g., 21' },
    { key: 'humidity', label: 'Humidity', unit: '%', icon: 'water-outline', placeholder: 'e.g., 82' },
    { key: 'ph', label: 'pH Level', unit: '', icon: 'beaker-outline', placeholder: 'e.g., 6.5' },
    { key: 'rainfall', label: 'Rainfall', unit: 'mm', icon: 'rainy-outline', placeholder: 'e.g., 203' }
  ];

  const handleInputChange = (key: keyof FormData, value: string) => {
    setFormData(prev => ({ ...prev, [key]: value }));
  };

  const validateForm = (): boolean => {
    for (const field of inputFields) {
      if (!formData[field.key as keyof FormData] || formData[field.key as keyof FormData].trim() === '') {
        Alert.alert('Validation Error', `Please enter ${field.label}`);
        return false;
      }
      
      const numValue = parseFloat(formData[field.key as keyof FormData]);
      if (isNaN(numValue) || numValue < 0) {
        Alert.alert('Validation Error', `Please enter a valid positive number for ${field.label}`);
        return false;
      }
    }
    return true;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    setLoading(true);
    try {
      const soilData: SoilData = {
        N: parseFloat(formData.N),
        P: parseFloat(formData.P),
        K: parseFloat(formData.K),
        temperature: parseFloat(formData.temperature),
        humidity: parseFloat(formData.humidity),
        ph: parseFloat(formData.ph),
        rainfall: parseFloat(formData.rainfall)
      };

      const result = await apiService.getCropRecommendation(soilData);
      setRecommendation(result);
      setShowResults(true);
    } catch (error) {
      Alert.alert('Error', 'Failed to get crop recommendation. Please check your internet connection and try again.');
      console.error('API Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      N: '',
      P: '',
      K: '',
      temperature: '',
      humidity: '',
      ph: '',
      rainfall: ''
    });
    setRecommendation(null);
    setShowResults(false);
  };

  if (showResults && recommendation) {
    return (
      <LinearGradient colors={['#4CAF50', '#45a049']} style={styles.container}>
        <ScrollView style={styles.resultsContainer} showsVerticalScrollIndicator={false}>
          <View style={styles.resultsHeader}>
            <TouchableOpacity onPress={() => setShowResults(false)} style={styles.backButton}>
              <Ionicons name="arrow-back" size={24} color="white" />
            </TouchableOpacity>
            <Text style={styles.resultsTitle}>🌾 Crop Recommendation</Text>
          </View>

          {/* Primary Recommendation */}
          <View style={styles.primaryCard}>
            <View style={styles.cardHeader}>
              <Ionicons name="star" size={24} color="#FFD700" />
              <Text style={styles.cardTitle}>Best Recommendation</Text>
            </View>
            
            <View style={styles.cropInfo}>
              <Text style={styles.cropName}>{recommendation.recommendation.primary_crop.name_english}</Text>
              <Text style={styles.cropNameHindi}>{recommendation.recommendation.primary_crop.name_hindi}</Text>
            </View>

            <View style={styles.metricsContainer}>
              <View style={styles.metric}>
                <Ionicons name="trending-up" size={20} color="#4CAF50" />
                <Text style={styles.metricLabel}>Confidence</Text>
                <Text style={styles.metricValue}>
                  {((recommendation.recommendation.primary_crop.confidence || 0) * 100).toFixed(1)}%
                </Text>
              </View>
              
              <View style={styles.metric}>
                <Ionicons name="bar-chart" size={20} color="#2196F3" />
                <Text style={styles.metricLabel}>Yield</Text>
                <Text style={styles.metricValue}>
                  {recommendation.recommendation.primary_crop.predicted_yield_kg_per_ha.toLocaleString()} kg/ha
                </Text>
              </View>
              
              <View style={styles.metric}>
                <Ionicons name="leaf" size={20} color="#8BC34A" />
                <Text style={styles.metricLabel}>Sustainability</Text>
                <Text style={styles.metricValue}>
                  {recommendation.recommendation.primary_crop.sustainability_score.toFixed(1)}/10
                </Text>
              </View>
            </View>
          </View>

          {/* Alternative Crops */}
          <View style={styles.alternativesSection}>
            <Text style={styles.sectionTitle}>Alternative Crops</Text>
            {recommendation.recommendation.alternative_crops.map((crop, index) => (
              <View key={index} style={styles.alternativeCard}>
                <View style={styles.alternativeHeader}>
                  <Text style={styles.alternativeName}>{crop.name_english}</Text>
                  <Text style={styles.alternativeNameHindi}>{crop.name_hindi}</Text>
                </View>
                <View style={styles.alternativeMetrics}>
                  <Text style={styles.alternativeMetric}>
                    🌾 {crop.predicted_yield_kg_per_ha.toLocaleString()} kg/ha
                  </Text>
                  <Text style={styles.alternativeMetric}>
                    🌱 {crop.sustainability_score.toFixed(1)}/10
                  </Text>
                </View>
              </View>
            ))}
          </View>

          {/* System Info */}
          <View style={styles.systemInfo}>
            <Text style={styles.systemInfoTitle}>System Information</Text>
            <Text style={styles.systemInfoText}>
              Model Accuracy: {recommendation.system_info.model_accuracy}
            </Text>
            <Text style={styles.systemInfoText}>
              Supported Crops: {recommendation.system_info.total_crops_supported}
            </Text>
            <Text style={styles.systemInfoText}>
              Target Region: {recommendation.system_info.target_region}
            </Text>
          </View>

          <TouchableOpacity style={styles.newRecommendationButton} onPress={resetForm}>
            <Ionicons name="refresh" size={20} color="white" />
            <Text style={styles.newRecommendationText}>New Recommendation</Text>
          </TouchableOpacity>
        </ScrollView>
      </LinearGradient>
    );
  }

  return (
    <LinearGradient colors={['#4CAF50', '#45a049']} style={styles.container}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
          <View style={styles.header}>
            <Text style={styles.title}>🌾 Crop Recommendation</Text>
            <Text style={styles.subtitle}>Enter your soil and environmental data</Text>
          </View>

          <View style={styles.formContainer}>
            {inputFields.map((field) => (
              <View key={field.key} style={styles.inputGroup}>
                <View style={styles.inputLabelContainer}>
                  <Ionicons name={field.icon as any} size={20} color="#4CAF50" />
                  <Text style={styles.inputLabel}>{field.label}</Text>
                  {field.unit && <Text style={styles.inputUnit}>({field.unit})</Text>}
                </View>
                <TextInput
                  style={styles.input}
                  value={formData[field.key as keyof FormData]}
                  onChangeText={(value) => handleInputChange(field.key as keyof FormData, value)}
                  placeholder={field.placeholder}
                  keyboardType="numeric"
                  placeholderTextColor="#999"
                />
              </View>
            ))}

            <TouchableOpacity 
              style={[styles.submitButton, loading && styles.submitButtonDisabled]} 
              onPress={handleSubmit}
              disabled={loading}
            >
              {loading ? (
                <ActivityIndicator color="white" size="small" />
              ) : (
                <>
                  <Ionicons name="analytics" size={20} color="white" />
                  <Text style={styles.submitButtonText}>Get Recommendation</Text>
                </>
              )}
            </TouchableOpacity>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  keyboardView: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  header: {
    padding: 20,
    paddingTop: 60,
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
    textAlign: 'center',
  },
  formContainer: {
    backgroundColor: 'white',
    margin: 20,
    borderRadius: 20,
    padding: 20,
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  inputGroup: {
    marginBottom: 20,
  },
  inputLabelContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  inputLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginLeft: 8,
  },
  inputUnit: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 10,
    padding: 12,
    fontSize: 16,
    backgroundColor: '#f9f9f9',
  },
  submitButton: {
    backgroundColor: '#4CAF50',
    borderRadius: 10,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 10,
  },
  submitButtonDisabled: {
    backgroundColor: '#ccc',
  },
  submitButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  resultsContainer: {
    flex: 1,
    padding: 20,
    paddingTop: 60,
  },
  resultsHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  backButton: {
    marginRight: 15,
  },
  resultsTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
  primaryCard: {
    backgroundColor: 'white',
    borderRadius: 15,
    padding: 20,
    marginBottom: 20,
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginLeft: 8,
  },
  cropInfo: {
    alignItems: 'center',
    marginBottom: 20,
  },
  cropName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4CAF50',
    textTransform: 'capitalize',
  },
  cropNameHindi: {
    fontSize: 18,
    color: '#666',
    marginTop: 4,
  },
  metricsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  metric: {
    alignItems: 'center',
    flex: 1,
  },
  metricLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  metricValue: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 2,
  },
  alternativesSection: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 15,
  },
  alternativeCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
  },
  alternativeHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  alternativeName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    textTransform: 'capitalize',
  },
  alternativeNameHindi: {
    fontSize: 14,
    color: '#666',
  },
  alternativeMetrics: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  alternativeMetric: {
    fontSize: 14,
    color: '#555',
  },
  systemInfo: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 10,
    padding: 15,
    marginBottom: 20,
  },
  systemInfoTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 8,
  },
  systemInfoText: {
    fontSize: 14,
    color: 'rgba(255, 255, 255, 0.8)',
    marginBottom: 4,
  },
  newRecommendationButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 10,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
  },
  newRecommendationText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
});
