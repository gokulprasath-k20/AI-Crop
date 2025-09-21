import React, { useState, useEffect } from 'react';
import { StyleSheet, TouchableOpacity, Text, ActivityIndicator, ScrollView, TextInput, View, Alert } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { apiService } from '@/services/api';

export default function TabTwoScreen() {
  const [apiStatus, setApiStatus] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [customApiUrl, setCustomApiUrl] = useState('https://crop-advisor-4lmd.onrender.com');
  const [isEditingUrl, setIsEditingUrl] = useState(false);
  const [wakingUp, setWakingUp] = useState(false);
  const [datasetInfo, setDatasetInfo] = useState<any>(null);
  const [datasetUrl, setDatasetUrl] = useState('');
  const [isEditingDataset, setIsEditingDataset] = useState(false);
  const [updatingDataset, setUpdatingDataset] = useState(false);

  const checkApiHealth = async (customUrl?: string) => {
    try {
      setLoading(true);
      setError(null);
      
      if (customUrl) {
        apiService.setCustomEndpoint(customUrl);
      }
      
      const health = await apiService.getHealthCheck();
      setApiStatus(health);
      
      // Also get dataset info
      try {
        const dataset = await apiService.getDatasetInfo();
        setDatasetInfo(dataset);
      } catch (datasetErr) {
        console.log('Could not fetch dataset info:', datasetErr);
      }
    } catch (err) {
      console.error('API health check failed:', err);
      setError(err instanceof Error ? err.message : 'Failed to connect to API');
      setApiStatus(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSetCustomApi = async () => {
    if (!customApiUrl.trim()) {
      Alert.alert('Error', 'Please enter a valid API URL');
      return;
    }

    try {
      setLoading(true);
      const isWorking = await apiService.testCustomEndpoint(customApiUrl);
      
      if (isWorking) {
        apiService.setCustomEndpoint(customApiUrl);
        await checkApiHealth();
        setIsEditingUrl(false);
        Alert.alert('Success', `API endpoint set to: ${customApiUrl}`);
      } else {
        Alert.alert('Error', 'Could not connect to the specified API endpoint');
      }
    } catch (err) {
      Alert.alert('Error', 'Failed to test API endpoint');
    } finally {
      setLoading(false);
    }
  };

  const wakeUpRender = async () => {
    try {
      setWakingUp(true);
      setError(null);
      Alert.alert('Waking up Render...', 'This may take up to 30 seconds for a cold start.');
      
      await apiService.wakeUpRenderService();
      await checkApiHealth();
      
      Alert.alert('Success', 'Render service is now active!');
    } catch (err) {
      Alert.alert('Error', 'Failed to wake up Render service. Please try again.');
    } finally {
      setWakingUp(false);
    }
  };

  const updateDataset = async () => {
    if (!datasetUrl.trim()) {
      Alert.alert('Error', 'Please enter a valid dataset URL');
      return;
    }

    try {
      setUpdatingDataset(true);
      const result = await apiService.updateDataset(datasetUrl);
      
      if (result.status === 'success') {
        Alert.alert('Success', `Dataset updated! Loaded ${result.crops_loaded.length} crops: ${result.crops_loaded.join(', ')}`);
        setDatasetInfo(result);
        setIsEditingDataset(false);
        await checkApiHealth(); // Refresh status
      } else {
        Alert.alert('Error', result.message || 'Failed to update dataset');
      }
    } catch (err) {
      Alert.alert('Error', 'Failed to update dataset. Please check the URL.');
    } finally {
      setUpdatingDataset(false);
    }
  };

  const getPresetUrls = () => [
    { label: 'Local Server', url: 'http://localhost:5000' },
    { label: 'Render Deployment', url: 'https://crop-advisor-4lmd.onrender.com' },
    { label: 'Alternative Local', url: 'http://127.0.0.1:5000' },
  ];

  const getPresetDatasets = () => [
    { label: 'Kaggle Crop Dataset', url: 'https://raw.githubusercontent.com/atharvajakkanwar/crop-prediction/main/Crop_recommendation.csv' },
    { label: 'Agriculture Dataset', url: 'https://raw.githubusercontent.com/your-username/datasets/main/agriculture.csv' },
    { label: 'Custom Dataset', url: 'https://your-domain.com/your-dataset.csv' },
  ];

  useEffect(() => {
    checkApiHealth();
  }, []);

  return (
    <ThemedView style={styles.container}>
      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        <ThemedView style={styles.titleContainer}>
          <ThemedText type="title">🌾 System Status</ThemedText>
          <ThemedText style={styles.titleEnglish}>सिस्टम की स्थिति</ThemedText>
        </ThemedView>

        {/* API Endpoint Configuration */}
        <ThemedView style={styles.configCard}>
          <ThemedText type="subtitle" style={styles.cardTitle}>
            🔧 API Configuration
          </ThemedText>
          
          {!isEditingUrl ? (
            <View style={styles.currentEndpoint}>
              <ThemedText style={styles.endpointLabel}>Current Endpoint:</ThemedText>
              <ThemedText style={styles.endpointUrl}>{customApiUrl}</ThemedText>
              <TouchableOpacity 
                style={styles.editButton} 
                onPress={() => setIsEditingUrl(true)}
              >
                <Text style={styles.editButtonText}>✏️ Change</Text>
              </TouchableOpacity>
            </View>
          ) : (
            <View style={styles.editEndpoint}>
              <ThemedText style={styles.inputLabel}>Enter API URL:</ThemedText>
              <TextInput
                style={styles.urlInput}
                value={customApiUrl}
                onChangeText={setCustomApiUrl}
                placeholder="http://localhost:5000"
                placeholderTextColor="#999"
              />
              
              <View style={styles.presetButtons}>
                {getPresetUrls().map((preset, index) => (
                  <TouchableOpacity
                    key={index}
                    style={styles.presetButton}
                    onPress={() => setCustomApiUrl(preset.url)}
                  >
                    <Text style={styles.presetButtonText}>{preset.label}</Text>
                  </TouchableOpacity>
                ))}
              </View>
              
              <View style={styles.actionButtons}>
                <TouchableOpacity 
                  style={styles.cancelButton} 
                  onPress={() => setIsEditingUrl(false)}
                >
                  <Text style={styles.cancelButtonText}>Cancel</Text>
                </TouchableOpacity>
                <TouchableOpacity 
                  style={styles.setButton} 
                  onPress={handleSetCustomApi}
                  disabled={loading}
                >
                  <Text style={styles.setButtonText}>
                    {loading ? 'Testing...' : 'Set & Test'}
                  </Text>
                </TouchableOpacity>
              </View>
            </View>
          )}
        </ThemedView>

        {/* Dataset Management */}
        <ThemedView style={styles.datasetCard}>
          <ThemedText type="subtitle" style={styles.cardTitle}>
            📊 Dataset Management
          </ThemedText>
          <ThemedText style={styles.cardSubtitle}>
            डेटासेट प्रबंधन
          </ThemedText>
          
          {datasetInfo && (
            <View style={styles.datasetInfo}>
              <ThemedText style={styles.datasetLabel}>Current Dataset:</ThemedText>
              <ThemedText style={styles.datasetValue}>{datasetInfo.dataset_url}</ThemedText>
              <ThemedText style={styles.datasetLabel}>Crops Available:</ThemedText>
              <ThemedText style={styles.datasetValue}>
                {datasetInfo.crops ? datasetInfo.crops.join(', ') : 'Loading...'}
              </ThemedText>
              <ThemedText style={styles.datasetLabel}>Total Records:</ThemedText>
              <ThemedText style={styles.datasetValue}>{datasetInfo.total_records}</ThemedText>
            </View>
          )}
          
          {!isEditingDataset ? (
            <TouchableOpacity 
              style={styles.editDatasetButton} 
              onPress={() => setIsEditingDataset(true)}
            >
              <Text style={styles.editDatasetButtonText}>🔄 Change Dataset</Text>
            </TouchableOpacity>
          ) : (
            <View style={styles.editDatasetSection}>
              <ThemedText style={styles.inputLabel}>Enter Dataset URL:</ThemedText>
              <TextInput
                style={styles.datasetInput}
                value={datasetUrl}
                onChangeText={setDatasetUrl}
                placeholder="https://raw.githubusercontent.com/user/repo/main/dataset.csv"
                placeholderTextColor="#999"
                multiline
              />
              
              <View style={styles.presetButtons}>
                {getPresetDatasets().map((preset, index) => (
                  <TouchableOpacity
                    key={index}
                    style={styles.presetButton}
                    onPress={() => setDatasetUrl(preset.url)}
                  >
                    <Text style={styles.presetButtonText}>{preset.label}</Text>
                  </TouchableOpacity>
                ))}
              </View>
              
              <View style={styles.actionButtons}>
                <TouchableOpacity 
                  style={styles.cancelButton} 
                  onPress={() => setIsEditingDataset(false)}
                >
                  <Text style={styles.cancelButtonText}>Cancel</Text>
                </TouchableOpacity>
                <TouchableOpacity 
                  style={styles.updateDatasetButton} 
                  onPress={updateDataset}
                  disabled={updatingDataset}
                >
                  <Text style={styles.updateDatasetButtonText}>
                    {updatingDataset ? '⏳ Updating...' : '✅ Update Dataset'}
                  </Text>
                </TouchableOpacity>
              </View>
            </View>
          )}
        </ThemedView>

        <ThemedView style={styles.statusCard}>
          <ThemedText type="subtitle" style={styles.cardTitle}>
            Crop Recommendation Service
          </ThemedText>
          <ThemedText style={styles.cardSubtitle}>
            फसल सलाह सेवा
          </ThemedText>
          
          {loading ? (
            <ThemedView style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="#4CAF50" />
              <ThemedText style={styles.loadingText}>Checking API status...</ThemedText>
            </ThemedView>
          ) : error ? (
            <ThemedView style={styles.errorContainer}>
              <ThemedText style={styles.errorText}>❌ {error}</ThemedText>
            </ThemedView>
          ) : apiStatus ? (
            <ThemedView style={styles.successContainer}>
              <ThemedText style={styles.successText}>✅ API is healthy</ThemedText>
              <ThemedText style={styles.statusDetail}>Service: {apiStatus.service}</ThemedText>
              <ThemedText style={styles.statusDetail}>Version: {apiStatus.version}</ThemedText>
              <ThemedText style={styles.statusDetail}>Accuracy: {apiStatus.accuracy}</ThemedText>
              <ThemedText style={styles.statusDetail}>Supported Crops: {apiStatus.supported_crops}</ThemedText>
              <ThemedText style={styles.statusDetail}>Target: {apiStatus.target}</ThemedText>
            </ThemedView>
          ) : null}

          <View style={styles.buttonRow}>
            <TouchableOpacity 
              style={[styles.refreshButton, { flex: 0.48 }]} 
              onPress={() => checkApiHealth()}
              disabled={loading || wakingUp}
            >
              <Text style={styles.refreshButtonText}>
                {loading ? '🔄 Checking...' : '🔄 Refresh'}
              </Text>
            </TouchableOpacity>
            
            <TouchableOpacity 
              style={[styles.wakeUpButton, { flex: 0.48 }]} 
              onPress={wakeUpRender}
              disabled={loading || wakingUp}
            >
              <Text style={styles.wakeUpButtonText}>
                {wakingUp ? '⏳ Waking...' : '🚀 Wake Render'}
              </Text>
            </TouchableOpacity>
          </View>
        </ThemedView>

        <ThemedView style={styles.infoCard}>
          <ThemedText type="subtitle" style={styles.cardTitle}>
            📱 App Information
          </ThemedText>
          <ThemedText style={styles.cardSubtitle}>
            ऐप की जानकारी
          </ThemedText>
          <ThemedText style={styles.infoText}>
            This is the SIH 2025 Crop Recommendation mobile app for Jharkhand farmers.
          </ThemedText>
          <ThemedText style={styles.infoText}>
            • Get personalized crop recommendations
          </ThemedText>
          <ThemedText style={styles.infoText}>
            • Based on soil and weather parameters
          </ThemedText>
          <ThemedText style={styles.infoText}>
            • Supports multiple crops and languages
          </ThemedText>
          <ThemedText style={styles.infoText}>
            • Real-time yield and sustainability predictions
          </ThemedText>
        </ThemedView>
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
    padding: 20,
  },
  titleContainer: {
    alignItems: 'center',
    marginBottom: 25,
    marginTop: 20,
    backgroundColor: '#388E3C',
    padding: 20,
    borderRadius: 20,
    shadowColor: '#2E7D32',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 6,
  },
  titleEnglish: {
    textAlign: 'center',
    fontSize: 14,
    color: '#C8E6C9',
    fontStyle: 'italic',
    marginTop: 5,
  },
  statusCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 15,
    padding: 25,
    marginBottom: 20,
    borderWidth: 2,
    borderColor: '#4CAF50',
    shadowColor: '#2E7D32',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.15,
    shadowRadius: 6,
    elevation: 5,
  },
  cardTitle: {
    textAlign: 'center',
    marginBottom: 8,
    fontSize: 18,
    fontWeight: '700',
    color: '#1B5E20',
  },
  cardSubtitle: {
    textAlign: 'center',
    marginBottom: 20,
    fontSize: 13,
    color: '#666',
    fontStyle: 'italic',
  },
  loadingContainer: {
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#F1F8E9',
    borderRadius: 12,
  },
  loadingText: {
    marginTop: 12,
    textAlign: 'center',
    color: '#2E7D32',
    fontWeight: '600',
  },
  errorContainer: {
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#FFEBEE',
    borderRadius: 12,
  },
  errorText: {
    color: '#D32F2F',
    textAlign: 'center',
    fontWeight: '600',
  },
  successContainer: {
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#E8F5E8',
    borderRadius: 12,
  },
  successText: {
    color: '#1B5E20',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 12,
  },
  statusDetail: {
    fontSize: 14,
    marginBottom: 6,
    textAlign: 'center',
    color: '#2E7D32',
    fontWeight: '500',
  },
  refreshButton: {
    backgroundColor: '#FF9800',
    padding: 15,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 20,
    shadowColor: '#E65100',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.2,
    shadowRadius: 6,
    elevation: 4,
  },
  refreshButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '700',
  },
  infoCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 15,
    padding: 25,
    marginBottom: 30,
    borderLeftWidth: 5,
    borderLeftColor: '#8BC34A',
    shadowColor: '#8BC34A',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  infoText: {
    fontSize: 15,
    marginBottom: 10,
    lineHeight: 22,
    color: '#1B5E20',
    fontWeight: '500',
  },
  // API Configuration Styles
  configCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 15,
    padding: 20,
    marginBottom: 20,
    borderWidth: 2,
    borderColor: '#2196F3',
    shadowColor: '#2196F3',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.15,
    shadowRadius: 6,
    elevation: 5,
  },
  currentEndpoint: {
    alignItems: 'center',
  },
  endpointLabel: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  endpointUrl: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2196F3',
    marginBottom: 15,
    textAlign: 'center',
  },
  editButton: {
    backgroundColor: '#2196F3',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  editButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
  },
  editEndpoint: {
    width: '100%',
  },
  inputLabel: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 10,
    color: '#1B5E20',
  },
  urlInput: {
    borderWidth: 2,
    borderColor: '#2196F3',
    borderRadius: 10,
    padding: 12,
    fontSize: 16,
    backgroundColor: '#F8FBFF',
    marginBottom: 15,
    color: '#333',
  },
  presetButtons: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  presetButton: {
    backgroundColor: '#E3F2FD',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 6,
    marginBottom: 8,
    minWidth: '30%',
    alignItems: 'center',
  },
  presetButtonText: {
    color: '#1976D2',
    fontSize: 12,
    fontWeight: '600',
  },
  actionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  cancelButton: {
    backgroundColor: '#F5F5F5',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    flex: 0.45,
  },
  cancelButtonText: {
    color: '#666',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
  setButton: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    flex: 0.45,
  },
  setButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 15,
  },
  wakeUpButton: {
    backgroundColor: '#9C27B0',
    padding: 15,
    borderRadius: 12,
    alignItems: 'center',
    shadowColor: '#7B1FA2',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.2,
    shadowRadius: 6,
    elevation: 4,
  },
  wakeUpButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '700',
  },
  // Dataset Management Styles
  datasetCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 15,
    padding: 20,
    marginBottom: 20,
    borderWidth: 2,
    borderColor: '#FF9800',
    shadowColor: '#FF9800',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.15,
    shadowRadius: 6,
    elevation: 5,
  },
  datasetInfo: {
    marginBottom: 15,
  },
  datasetLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#E65100',
    marginTop: 10,
    marginBottom: 5,
  },
  datasetValue: {
    fontSize: 13,
    color: '#333',
    marginBottom: 5,
    paddingLeft: 10,
  },
  editDatasetButton: {
    backgroundColor: '#FF9800',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  editDatasetButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
  },
  editDatasetSection: {
    width: '100%',
  },
  datasetInput: {
    borderWidth: 2,
    borderColor: '#FF9800',
    borderRadius: 10,
    padding: 12,
    fontSize: 14,
    backgroundColor: '#FFF3E0',
    marginBottom: 15,
    color: '#333',
    minHeight: 60,
    textAlignVertical: 'top',
  },
  updateDatasetButton: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    flex: 0.45,
  },
  updateDatasetButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
    textAlign: 'center',
  },
});
