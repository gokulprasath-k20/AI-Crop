import React, { useState } from 'react';
import { StyleSheet } from 'react-native';
import { ThemedView } from '@/components/themed-view';
import CropRecommendationForm from '@/components/CropRecommendationForm';
import RecommendationResults from '@/components/RecommendationResults';
import { CropRecommendationResponse } from '@/services/api';

export default function HomeScreen() {
  const [recommendation, setRecommendation] = useState<CropRecommendationResponse | null>(null);

  const handleRecommendationReceived = (rec: CropRecommendationResponse) => {
    setRecommendation(rec);
  };

  const handleBackToForm = () => {
    setRecommendation(null);
  };

  return (
    <ThemedView style={styles.container}>
      {recommendation ? (
        <RecommendationResults 
          recommendation={recommendation} 
          onBackToForm={handleBackToForm}
        />
      ) : (
        <CropRecommendationForm 
          onRecommendationReceived={handleRecommendationReceived}
        />
      )}
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
