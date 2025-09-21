import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { CropRecommendationResponse } from '@/services/api';

interface Props {
  recommendation: CropRecommendationResponse;
  onBackToForm: () => void;
}

export default function RecommendationResults({ recommendation, onBackToForm }: Props) {
  const { primary_crop, alternative_crops } = recommendation.recommendation;

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-IN').format(Math.round(num));
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return '#4CAF50';
    if (confidence >= 0.6) return '#FF9800';
    return '#F44336';
  };

  const getSustainabilityColor = (score: number) => {
    if (score >= 8) return '#4CAF50';
    if (score >= 6) return '#FF9800';
    return '#F44336';
  };

  return (
    <ThemedView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false} style={styles.scrollView}>
        <View style={styles.header}>
          <ThemedText type="title" style={styles.title}>
            🎯 Your Crop Recommendations
          </ThemedText>
          <ThemedText style={styles.subtitle}>
            AI-powered analysis based on your soil and weather data
          </ThemedText>
          <ThemedText style={styles.subtitleEnglish}>
            आपकी मिट्टी और मौसम के आधार पर सबसे अच्छी फसल
          </ThemedText>
        </View>

        {/* Primary Recommendation */}
        <View style={styles.primaryCard}>
          <ThemedText type="subtitle" style={styles.cardTitle}>
            🏆 Recommended Crop
          </ThemedText>
          
          <View style={styles.cropHeader}>
            <ThemedText style={styles.cropName}>
              {primary_crop.name_english.charAt(0).toUpperCase() + primary_crop.name_english.slice(1)}
            </ThemedText>
            <ThemedText style={styles.cropNameHindi}>
              {primary_crop.name_hindi}
            </ThemedText>
          </View>

          <View style={styles.metricsContainer}>
            <View style={styles.metric}>
              <ThemedText style={styles.metricLabel}>Confidence</ThemedText>
              <View style={styles.metricValueContainer}>
                <ThemedText 
                  style={[
                    styles.metricValue, 
                    { color: getConfidenceColor(primary_crop.confidence || 0) }
                  ]}
                >
                  {((primary_crop.confidence || 0) * 100).toFixed(1)}%
                </ThemedText>
              </View>
            </View>

            <View style={styles.metric}>
              <ThemedText style={styles.metricLabel}>Predicted Yield</ThemedText>
              <ThemedText style={styles.metricValue}>
                {formatNumber(primary_crop.predicted_yield_kg_per_ha)} kg/ha
              </ThemedText>
            </View>

            <View style={styles.metric}>
              <ThemedText style={styles.metricLabel}>Sustainability</ThemedText>
              <ThemedText 
                style={[
                  styles.metricValue, 
                  { color: getSustainabilityColor(primary_crop.sustainability_score) }
                ]}
              >
                {primary_crop.sustainability_score.toFixed(1)}/10
              </ThemedText>
            </View>
          </View>
        </View>

        {/* Alternative Crops */}
        {alternative_crops.length > 0 && (
          <View style={styles.alternativesSection}>
            <ThemedText type="subtitle" style={styles.sectionTitle}>
              🌱 Alternative Crops
            </ThemedText>
            
            {alternative_crops.map((crop, index) => (
              <View key={index} style={styles.alternativeCard}>
                <View style={styles.alternativeHeader}>
                  <ThemedText style={styles.alternativeName}>
                    {crop.name_english.charAt(0).toUpperCase() + crop.name_english.slice(1)}
                  </ThemedText>
                  <ThemedText style={styles.alternativeNameHindi}>
                    {crop.name_hindi}
                  </ThemedText>
                </View>
                
                <View style={styles.alternativeMetrics}>
                  <View style={styles.alternativeMetric}>
                    <ThemedText style={styles.alternativeMetricLabel}>Yield</ThemedText>
                    <ThemedText style={styles.alternativeMetricValue}>
                      {formatNumber(crop.predicted_yield_kg_per_ha)} kg/ha
                    </ThemedText>
                  </View>
                  
                  <View style={styles.alternativeMetric}>
                    <ThemedText style={styles.alternativeMetricLabel}>Sustainability</ThemedText>
                    <ThemedText 
                      style={[
                        styles.alternativeMetricValue,
                        { color: getSustainabilityColor(crop.sustainability_score) }
                      ]}
                    >
                      {crop.sustainability_score.toFixed(1)}/10
                    </ThemedText>
                  </View>
                </View>
              </View>
            ))}
          </View>
        )}

        {/* System Info */}
        <View style={styles.systemInfo}>
          <ThemedText style={styles.systemInfoTitle}>📊 System Information</ThemedText>
          <ThemedText style={styles.systemInfoText}>
            Model Accuracy: {recommendation.system_info.model_accuracy}
          </ThemedText>
          <ThemedText style={styles.systemInfoText}>
            Supported Crops: {recommendation.system_info.total_crops_supported}
          </ThemedText>
          <ThemedText style={styles.systemInfoText}>
            Target Region: {recommendation.system_info.target_region}
          </ThemedText>
        </View>

        <TouchableOpacity style={styles.backButton} onPress={onBackToForm}>
          <Text style={styles.backButtonText}>🔄 Get New Recommendation</Text>
          <Text style={styles.backButtonSubtext}>नई सलाह लें</Text>
        </TouchableOpacity>
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F4F1E8',
  },
  scrollView: {
    flex: 1,
  },
  header: {
    backgroundColor: '#388E3C',
    paddingHorizontal: 20,
    paddingTop: 30,
    paddingBottom: 25,
    borderBottomLeftRadius: 25,
    borderBottomRightRadius: 25,
    marginBottom: 20,
  },
  title: {
    textAlign: 'center',
    marginBottom: 8,
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  subtitle: {
    textAlign: 'center',
    marginBottom: 5,
    fontSize: 16,
    color: '#E8F5E8',
    fontWeight: '600',
  },
  subtitleEnglish: {
    textAlign: 'center',
    fontSize: 13,
    color: '#C8E6C9',
    fontStyle: 'italic',
  },
  primaryCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    padding: 25,
    marginHorizontal: 20,
    marginBottom: 20,
    borderWidth: 3,
    borderColor: '#4CAF50',
    shadowColor: '#2E7D32',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 8,
  },
  cardTitle: {
    textAlign: 'center',
    marginBottom: 20,
    color: '#1B5E20',
    fontSize: 18,
    fontWeight: '700',
  },
  cropHeader: {
    alignItems: 'center',
    marginBottom: 25,
    backgroundColor: '#E8F5E8',
    padding: 15,
    borderRadius: 15,
  },
  cropName: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1B5E20',
    marginBottom: 5,
  },
  cropNameHindi: {
    fontSize: 20,
    color: '#388E3C',
    fontWeight: '600',
  },
  metricsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: '#F1F8E9',
    padding: 15,
    borderRadius: 12,
  },
  metric: {
    alignItems: 'center',
  },
  metricLabel: {
    fontSize: 12,
    opacity: 0.8,
    marginBottom: 6,
    color: '#2E7D32',
    fontWeight: '600',
  },
  metricValueContainer: {
    alignItems: 'center',
  },
  metricValue: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  alternativesSection: {
    marginHorizontal: 20,
    marginBottom: 20,
  },
  sectionTitle: {
    marginBottom: 15,
    fontSize: 18,
    fontWeight: '700',
    color: '#1B5E20',
  },
  alternativeCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 18,
    marginBottom: 12,
    borderLeftWidth: 5,
    borderLeftColor: '#FF9800',
    shadowColor: '#FF9800',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  alternativeHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  alternativeName: {
    fontSize: 18,
    fontWeight: '700',
    color: '#E65100',
  },
  alternativeNameHindi: {
    fontSize: 14,
    color: '#FF9800',
    fontWeight: '600',
  },
  alternativeMetrics: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: '#FFF8E1',
    padding: 10,
    borderRadius: 8,
  },
  alternativeMetric: {
    alignItems: 'center',
  },
  alternativeMetricLabel: {
    fontSize: 11,
    opacity: 0.8,
    color: '#E65100',
    fontWeight: '600',
  },
  alternativeMetricValue: {
    fontSize: 14,
    fontWeight: '700',
    color: '#E65100',
  },
  systemInfo: {
    backgroundColor: '#FFFFFF',
    borderRadius: 15,
    padding: 20,
    marginHorizontal: 20,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#C8E6C9',
  },
  systemInfoTitle: {
    fontSize: 16,
    fontWeight: '700',
    marginBottom: 12,
    color: '#1B5E20',
  },
  systemInfoText: {
    fontSize: 14,
    marginBottom: 6,
    color: '#2E7D32',
    fontWeight: '500',
  },
  backButton: {
    backgroundColor: '#FF9800',
    padding: 18,
    borderRadius: 15,
    alignItems: 'center',
    marginHorizontal: 20,
    marginBottom: 30,
    shadowColor: '#E65100',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
    borderWidth: 2,
    borderColor: '#FFB74D',
  },
  backButtonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 2,
  },
  backButtonSubtext: {
    color: '#FFF3E0',
    fontSize: 12,
    fontWeight: '500',
  },
});
