import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Alert,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { apiService, CropRecommendationRequest, CropRecommendationResponse } from '@/services/api';

const { width } = Dimensions.get('window');

interface Props {
  onRecommendationReceived: (recommendation: CropRecommendationResponse) => void;
}

export default function CropRecommendationForm({ onRecommendationReceived }: Props) {
  const [formData, setFormData] = useState<CropRecommendationRequest>({
    N: 90,
    P: 42,
    K: 43,
    temperature: 21,
    humidity: 82,
    ph: 6.5,
    rainfall: 203,
  });
  
  const [loading, setLoading] = useState(false);
  const [focusedField, setFocusedField] = useState<string | null>(null);
  const [errors, setErrors] = useState<{[key: string]: string}>({});

  const handleInputChange = (field: keyof CropRecommendationRequest, value: string) => {
    // Handle empty string or invalid input
    if (value === '' || value === '.') {
      setFormData(prev => ({
        ...prev,
        [field]: 0,
      }));
      return;
    }
    
    // Parse decimal numbers properly
    const numericValue = parseFloat(value);
    if (!isNaN(numericValue)) {
      setFormData(prev => ({
        ...prev,
        [field]: numericValue,
      }));
    }
    
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const validateField = (field: keyof CropRecommendationRequest, value: number) => {
    const validationRules = {
      N: { min: 0, max: 200, name: 'Nitrogen' },
      P: { min: 0, max: 100, name: 'Phosphorus' },
      K: { min: 0, max: 100, name: 'Potassium' },
      temperature: { min: -10, max: 50, name: 'Temperature' },
      humidity: { min: 0, max: 100, name: 'Humidity' },
      ph: { min: 0, max: 14, name: 'pH Level' },
      rainfall: { min: 0, max: 3000, name: 'Rainfall' },
    };
    
    const rule = validationRules[field];
    if (value < rule.min || value > rule.max) {
      return `${rule.name} should be between ${rule.min} and ${rule.max}`;
    }
    return null;
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      
      // Validate all inputs
      const newErrors: {[key: string]: string} = {};
      const requiredFields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'] as const;
      
      for (const field of requiredFields) {
        const value = formData[field];
        if (!value && value !== 0) {
          newErrors[field] = `${field} is required`;
        } else {
          const error = validateField(field, value);
          if (error) {
            newErrors[field] = error;
          }
        }
      }
      
      if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
        Alert.alert('Validation Error', 'Please fix the highlighted errors before submitting.');
        return;
      }

      const recommendation = await apiService.getCropRecommendation(formData);
      onRecommendationReceived(recommendation);
    } catch (error) {
      console.error('Error getting recommendation:', error);
      Alert.alert(
        'Error',
        'Failed to get crop recommendation. Please check your internet connection and try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const inputFields = [
    { key: 'N', label: 'Nitrogen (N)', unit: 'kg/ha', placeholder: '90', icon: '🌱', description: 'Nitrogen content in soil', hindi: 'मिट्टी में नाइट्रोजन' },
    { key: 'P', label: 'Phosphorus (P)', unit: 'kg/ha', placeholder: '42', icon: '🌿', description: 'Phosphorus content in soil', hindi: 'मिट्टी में फास्फोरस' },
    { key: 'K', label: 'Potassium (K)', unit: 'kg/ha', placeholder: '43', icon: '🍃', description: 'Potassium content in soil', hindi: 'मिट्टी में पोटाश' },
    { key: 'temperature', label: 'Temperature', unit: '°C', placeholder: '21', icon: '🌞', description: 'Average temperature in your area', hindi: 'तापमान' },
    { key: 'humidity', label: 'Humidity', unit: '%', placeholder: '82', icon: '💧', description: 'Relative humidity percentage', hindi: 'नमी' },
    { key: 'ph', label: 'pH Level', unit: '', placeholder: '6.5', icon: '🧪', description: 'Soil acidity level (0-14)', hindi: 'मिट्टी का pH' },
    { key: 'rainfall', label: 'Rainfall', unit: 'mm', placeholder: '203', icon: '🌧️', description: 'Annual rainfall amount', hindi: 'बारिश' },
  ];

  return (
    <ThemedView style={styles.container}>
      <View style={styles.header}>
        <ThemedText type="title" style={styles.title}>
          🚜 Smart Crop Advisor
        </ThemedText>
        <ThemedText style={styles.subtitle}>
          Get AI-powered crop recommendations based on your soil and weather conditions
        </ThemedText>
        <ThemedText style={styles.subtitleEnglish}>
          अपनी मिट्टी और मौसम के आधार पर सबसे अच्छी फसल की सलाह पाएं
        </ThemedText>
        <View style={styles.badge}>
          <Text style={styles.badgeText}>🏆 SIH 2025 • For Jharkhand Farmers</Text>
        </View>
      </View>

      <ScrollView style={styles.formContainer} showsVerticalScrollIndicator={false}>
        {inputFields.map((field) => (
          <View key={field.key} style={styles.inputGroup}>
            <View style={styles.labelContainer}>
              <Text style={styles.icon}>{field.icon}</Text>
              <View style={styles.labelTextContainer}>
                <ThemedText style={styles.label}>
                  {field.label} {field.unit && `(${field.unit})`}
                </ThemedText>
                <ThemedText style={styles.description}>
                  {field.description}
                </ThemedText>
                <ThemedText style={styles.englishLabel}>
                  {field.hindi}
                </ThemedText>
              </View>
            </View>
            <TextInput
              style={[
                styles.input,
                focusedField === field.key && styles.inputFocused,
                errors[field.key] && styles.inputError
              ]}
              value={formData[field.key as keyof CropRecommendationRequest].toString()}
              onChangeText={(value) => handleInputChange(field.key as keyof CropRecommendationRequest, value)}
              onFocus={() => setFocusedField(field.key)}
              onBlur={() => setFocusedField(null)}
              placeholder={field.placeholder}
              keyboardType="decimal-pad"
              placeholderTextColor="#999"
              returnKeyType="next"
            />
            {errors[field.key] && (
              <Text style={styles.errorText}>{errors[field.key]}</Text>
            )}
          </View>
        ))}

        <TouchableOpacity
          style={[styles.submitButton, loading && styles.submitButtonDisabled]}
          onPress={handleSubmit}
          disabled={loading}
        >
          {loading ? (
            <View style={styles.loadingContainer}>
              <ActivityIndicator color="#fff" size="small" />
              <Text style={styles.loadingButtonText}>Preparing recommendation...</Text>
            </View>
          ) : (
            <View style={styles.buttonContent}>
              <Text style={styles.submitButtonText}>🌾 Get Crop Recommendation</Text>
              <Text style={styles.submitButtonSubtext}>फसल की सलाह पाएं</Text>
            </View>
          )}
        </TouchableOpacity>
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F4F1E8', // Warm earth tone
  },
  header: {
    backgroundColor: 'linear-gradient(135deg, #8BC34A 0%, #4CAF50 100%)', // Green gradient
    paddingHorizontal: 20,
    paddingTop: 30,
    paddingBottom: 25,
    borderBottomLeftRadius: 25,
    borderBottomRightRadius: 25,
    shadowColor: '#2E7D32',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 8,
  },
  title: {
    textAlign: 'center',
    marginBottom: 8,
    fontSize: 26,
    fontWeight: 'bold',
    color: '#1B5E20', // Dark green
  },
  subtitle: {
    textAlign: 'center',
    marginBottom: 8,
    fontSize: 16,
    lineHeight: 22,
    paddingHorizontal: 10,
    color: '#2E7D32',
    fontWeight: '600',
  },
  subtitleEnglish: {
    textAlign: 'center',
    marginBottom: 15,
    fontSize: 14,
    opacity: 0.8,
    color: '#388E3C',
    fontStyle: 'italic',
  },
  badge: {
    backgroundColor: '#FFF8E1', // Light yellow
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
    alignSelf: 'center',
    borderWidth: 1,
    borderColor: '#F57F17',
  },
  badgeText: {
    color: '#E65100', // Orange
    fontSize: 13,
    fontWeight: '700',
  },
  formContainer: {
    flex: 1,
    padding: 20,
  },
  inputGroup: {
    marginBottom: 18,
    backgroundColor: '#FFFFFF',
    borderRadius: 15,
    padding: 18,
    shadowColor: '#8BC34A',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    borderLeftWidth: 4,
    borderLeftColor: '#8BC34A',
  },
  labelContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  icon: {
    fontSize: 24,
    marginRight: 15,
    marginTop: 2,
  },
  labelTextContainer: {
    flex: 1,
  },
  label: {
    fontSize: 17,
    fontWeight: '700',
    marginBottom: 4,
    color: '#1B5E20',
  },
  description: {
    fontSize: 13,
    opacity: 0.8,
    lineHeight: 18,
    color: '#2E7D32',
    marginBottom: 2,
  },
  englishLabel: {
    fontSize: 11,
    opacity: 0.6,
    color: '#666',
    fontStyle: 'italic',
  },
  input: {
    borderWidth: 2,
    borderColor: '#C8E6C9',
    borderRadius: 12,
    padding: 16,
    fontSize: 18,
    backgroundColor: '#F1F8E9',
    color: '#1B5E20',
    fontWeight: '600',
    textAlign: 'center',
  },
  inputFocused: {
    borderColor: '#4CAF50',
    backgroundColor: '#E8F5E8',
    shadowColor: '#4CAF50',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 4,
  },
  inputError: {
    borderColor: '#F44336',
    backgroundColor: '#FFEBEE',
  },
  errorText: {
    color: '#D32F2F',
    fontSize: 12,
    marginTop: 8,
    marginLeft: 4,
    fontWeight: '600',
    backgroundColor: '#FFEBEE',
    padding: 4,
    borderRadius: 4,
  },
  submitButton: {
    backgroundColor: '#388E3C',
    padding: 20,
    borderRadius: 15,
    alignItems: 'center',
    marginTop: 25,
    marginBottom: 40,
    shadowColor: '#2E7D32',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 8,
    borderWidth: 2,
    borderColor: '#4CAF50',
  },
  submitButtonDisabled: {
    backgroundColor: '#BDBDBD',
    shadowOpacity: 0,
    elevation: 0,
    borderColor: '#E0E0E0',
  },
  buttonContent: {
    alignItems: 'center',
  },
  submitButtonText: {
    color: '#FFFFFF',
    fontSize: 20,
    fontWeight: '800',
    letterSpacing: 0.5,
    marginBottom: 2,
  },
  submitButtonSubtext: {
    color: '#E8F5E8',
    fontSize: 12,
    fontWeight: '500',
    opacity: 0.9,
  },
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  loadingButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 10,
  },
});
