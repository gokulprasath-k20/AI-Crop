import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  ScrollView, 
  StyleSheet, 
  Alert,
  ActivityIndicator
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import apiService from '../../services/apiService';

export default function SettingsScreen() {
  const [backendUrl, setBackendUrl] = useState('http://localhost:5000');
  const [isConnecting, setIsConnecting] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'unknown' | 'connected' | 'failed'>('unknown');
  const [systemInfo, setSystemInfo] = useState<any>(null);

  const testConnection = async () => {
    setIsConnecting(true);
    try {
      apiService.setBaseUrl(backendUrl);
      const health = await apiService.checkHealth();
      setConnectionStatus('connected');
      setSystemInfo(health);
      Alert.alert('Success', 'Successfully connected to backend!');
    } catch (error) {
      setConnectionStatus('failed');
      setSystemInfo(null);
      Alert.alert('Connection Failed', 'Could not connect to the backend. Please check the URL and ensure the server is running.');
    } finally {
      setIsConnecting(false);
    }
  };

  const presetUrls = [
    { label: 'Local Development', url: 'http://localhost:5000' },
    { label: 'Local Network (192.168.1.x)', url: 'http://192.168.1.100:5000' },
    { label: 'Render Deployment', url: 'https://your-app-name.onrender.com' },
    { label: 'Custom', url: '' }
  ];

  const cropInfo = [
    { name: 'Rice (चावल)', icon: '🌾', description: 'High water requirement, monsoon crop' },
    { name: 'Wheat (गेहूं)', icon: '🌾', description: 'Winter crop, moderate water needs' },
    { name: 'Maize (मक्का)', icon: '🌽', description: 'Kharif crop, good for varied soil types' },
    { name: 'Cotton (कपास)', icon: '🌿', description: 'Cash crop, requires warm climate' },
    { name: 'Banana (केला)', icon: '🍌', description: 'Perennial crop, high yield potential' },
    { name: 'Mango (आम)', icon: '🥭', description: 'Fruit tree, long-term investment' }
  ];

  return (
    <LinearGradient colors={['#4CAF50', '#45a049']} style={styles.container}>
      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        <View style={styles.header}>
          <Text style={styles.title}>⚙️ Settings & Info</Text>
          <Text style={styles.subtitle}>Configure backend connection and learn about crops</Text>
        </View>

        {/* Backend Configuration */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="server-outline" size={24} color="white" />
            <Text style={styles.sectionTitle}>Backend Configuration</Text>
          </View>
          
          <View style={styles.card}>
            <Text style={styles.cardTitle}>Backend URL</Text>
            <TextInput
              style={styles.urlInput}
              value={backendUrl}
              onChangeText={setBackendUrl}
              placeholder="Enter backend URL"
              placeholderTextColor="#999"
            />
            
            <View style={styles.presetContainer}>
              <Text style={styles.presetTitle}>Quick Presets:</Text>
              {presetUrls.map((preset, index) => (
                <TouchableOpacity
                  key={index}
                  style={styles.presetButton}
                  onPress={() => preset.url && setBackendUrl(preset.url)}
                >
                  <Text style={styles.presetText}>{preset.label}</Text>
                </TouchableOpacity>
              ))}
            </View>

            <TouchableOpacity
              style={[styles.testButton, isConnecting && styles.testButtonDisabled]}
              onPress={testConnection}
              disabled={isConnecting}
            >
              {isConnecting ? (
                <ActivityIndicator color="white" size="small" />
              ) : (
                <>
                  <Ionicons name="wifi-outline" size={20} color="white" />
                  <Text style={styles.testButtonText}>Test Connection</Text>
                </>
              )}
            </TouchableOpacity>

            {/* Connection Status */}
            <View style={styles.statusContainer}>
              <View style={styles.statusRow}>
                <Ionicons 
                  name={connectionStatus === 'connected' ? 'checkmark-circle' : connectionStatus === 'failed' ? 'close-circle' : 'help-circle'} 
                  size={20} 
                  color={connectionStatus === 'connected' ? '#4CAF50' : connectionStatus === 'failed' ? '#f44336' : '#999'} 
                />
                <Text style={[styles.statusText, { 
                  color: connectionStatus === 'connected' ? '#4CAF50' : connectionStatus === 'failed' ? '#f44336' : '#999' 
                }]}>
                  {connectionStatus === 'connected' ? 'Connected' : connectionStatus === 'failed' ? 'Connection Failed' : 'Not Tested'}
                </Text>
              </View>
            </View>

            {/* System Info */}
            {systemInfo && (
              <View style={styles.systemInfoContainer}>
                <Text style={styles.systemInfoTitle}>System Information</Text>
                <Text style={styles.systemInfoText}>Service: {systemInfo.service}</Text>
                <Text style={styles.systemInfoText}>Version: {systemInfo.version}</Text>
                <Text style={styles.systemInfoText}>Accuracy: {systemInfo.accuracy}</Text>
                <Text style={styles.systemInfoText}>Supported Crops: {systemInfo.supported_crops}</Text>
                <Text style={styles.systemInfoText}>Target: {systemInfo.target}</Text>
              </View>
            )}
          </View>
        </View>

        {/* Supported Crops */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="leaf-outline" size={24} color="white" />
            <Text style={styles.sectionTitle}>Supported Crops</Text>
          </View>
          
          <View style={styles.cropsContainer}>
            {cropInfo.map((crop, index) => (
              <View key={index} style={styles.cropCard}>
                <Text style={styles.cropIcon}>{crop.icon}</Text>
                <View style={styles.cropInfo}>
                  <Text style={styles.cropName}>{crop.name}</Text>
                  <Text style={styles.cropDescription}>{crop.description}</Text>
                </View>
              </View>
            ))}
          </View>
        </View>

        {/* App Information */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="information-circle-outline" size={24} color="white" />
            <Text style={styles.sectionTitle}>About This App</Text>
          </View>
          
          <View style={styles.card}>
            <Text style={styles.aboutText}>
              This crop recommendation app uses machine learning to suggest the best crops for your soil and environmental conditions.
            </Text>
            <Text style={styles.aboutText}>
              • Built for farmers in Jharkhand, India
            </Text>
            <Text style={styles.aboutText}>
              • Supports 6 major crops with bilingual names
            </Text>
            <Text style={styles.aboutText}>
              • Provides yield predictions and sustainability scores
            </Text>
            <Text style={styles.aboutText}>
              • Developed for SIH 2025
            </Text>
          </View>
        </View>
      </ScrollView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
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
  section: {
    marginHorizontal: 20,
    marginBottom: 20,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
    marginLeft: 10,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 15,
    padding: 20,
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  urlInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 10,
    padding: 12,
    fontSize: 16,
    backgroundColor: '#f9f9f9',
    marginBottom: 15,
  },
  presetContainer: {
    marginBottom: 15,
  },
  presetTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    marginBottom: 8,
  },
  presetButton: {
    backgroundColor: '#f0f0f0',
    borderRadius: 8,
    padding: 10,
    marginBottom: 5,
  },
  presetText: {
    fontSize: 14,
    color: '#333',
  },
  testButton: {
    backgroundColor: '#4CAF50',
    borderRadius: 10,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 15,
  },
  testButtonDisabled: {
    backgroundColor: '#ccc',
  },
  testButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  statusContainer: {
    marginBottom: 15,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusText: {
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  systemInfoContainer: {
    backgroundColor: '#f9f9f9',
    borderRadius: 10,
    padding: 15,
  },
  systemInfoTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  systemInfoText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
  cropsContainer: {
    backgroundColor: 'white',
    borderRadius: 15,
    padding: 15,
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  cropCard: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  cropIcon: {
    fontSize: 32,
    marginRight: 15,
  },
  cropInfo: {
    flex: 1,
  },
  cropName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  cropDescription: {
    fontSize: 14,
    color: '#666',
  },
  aboutText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    lineHeight: 20,
  },
});
