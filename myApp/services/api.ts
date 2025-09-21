// API Service for Crop Recommendation with Auto-Fallback
const API_ENDPOINTS = [
  'http://localhost:5000', // Local development server
  'https://crop-advisor-4lmd.onrender.com', // Deployed API URL
  'http://127.0.0.1:5000', // Alternative local address
];

let WORKING_API_URL: string | null = null;

export interface CropRecommendationRequest {
  N: number;
  P: number;
  K: number;
  temperature: number;
  humidity: number;
  ph: number;
  rainfall: number;
}

export interface CropInfo {
  name_english: string;
  name_hindi: string;
  predicted_yield_kg_per_ha: number;
  sustainability_score: number;
  confidence?: number;
}

export interface CropRecommendationResponse {
  status: string;
  timestamp: string;
  recommendation: {
    primary_crop: CropInfo;
    alternative_crops: CropInfo[];
  };
  system_info: {
    model_accuracy: string;
    total_crops_supported: number;
    target_region: string;
  };
}

export interface ApiError {
  status: string;
  message: string;
}

class ApiService {
  private async findWorkingEndpoint(): Promise<string> {
    if (WORKING_API_URL) {
      return WORKING_API_URL;
    }

    for (const baseUrl of API_ENDPOINTS) {
      try {
        console.log(`Testing API endpoint: ${baseUrl}`);
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 second timeout for Render cold start
        
        const response = await fetch(`${baseUrl}/api/health`, {
          method: 'GET',
          headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          signal: controller.signal,
        });
        
        clearTimeout(timeoutId);
        
        if (response.ok) {
          const data = await response.json();
          console.log(`✅ Working API found: ${baseUrl}`, data);
          WORKING_API_URL = baseUrl;
          return baseUrl;
        } else {
          console.log(`❌ API responded with status: ${response.status} for ${baseUrl}`);
        }
      } catch (error) {
        console.log(`❌ Failed to connect to: ${baseUrl}`, error);
      }
    }
    
    throw new Error('No working API endpoints found. Please ensure the server is running.');
  }

  private async makeRequest<T>(endpoint: string, options?: RequestInit): Promise<T> {
    try {
      const baseUrl = await this.findWorkingEndpoint();
      const url = `${baseUrl}${endpoint}`;
      console.log('Making API request to:', url);
      
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      console.log('Response status:', response.status);

      if (!response.ok) {
        // If request fails, reset working URL to retry endpoint discovery
        if (response.status >= 500) {
          WORKING_API_URL = null;
        }
        const errorText = await response.text();
        console.error('Error response:', errorText);
        throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log('Response data:', data);
      
      if (data.status === 'error') {
        throw new Error(data.message || 'API request failed');
      }

      return data;
    } catch (error) {
      console.error('API request failed:', error);
      // Reset working URL on error to retry endpoint discovery
      WORKING_API_URL = null;
      throw error;
    }
  }

  async getCropRecommendation(params: CropRecommendationRequest): Promise<CropRecommendationResponse> {
    return this.makeRequest<CropRecommendationResponse>('/api/recommend', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  async getHealthCheck(): Promise<any> {
    return this.makeRequest('/api/health');
  }

  async getSupportedCrops(): Promise<any> {
    return this.makeRequest('/api/crops');
  }

  async getUsageStats(): Promise<any> {
    return this.makeRequest('/api/usage');
  }

  async testConnection(): Promise<any> {
    // Test the root endpoint first
    return this.makeRequest('/');
  }

  async wakeUpRenderService(): Promise<void> {
    // Try to wake up the Render service by hitting the health endpoint
    try {
      console.log('Attempting to wake up Render service...');
      const response = await fetch('https://crop-advisor-4lmd.onrender.com/api/health', {
        method: 'GET',
        signal: AbortSignal.timeout(30000), // 30 second timeout for cold start
      });
      if (response.ok) {
        console.log('✅ Render service is awake!');
        WORKING_API_URL = 'https://crop-advisor-4lmd.onrender.com';
      }
    } catch (error) {
      console.log('❌ Could not wake up Render service');
    }
  }

  async getWorkingEndpoint(): Promise<string | null> {
    return WORKING_API_URL;
  }

  setCustomEndpoint(url: string): void {
    WORKING_API_URL = url;
    console.log(`🔧 Manual API endpoint set to: ${url}`);
  }

  async updateDataset(datasetUrl: string): Promise<any> {
    return this.makeRequest('/api/update-dataset', {
      method: 'POST',
      body: JSON.stringify({ dataset_url: datasetUrl }),
    });
  }

  async getDatasetInfo(): Promise<any> {
    return this.makeRequest('/api/dataset-info');
  }

  async testCustomEndpoint(url: string): Promise<boolean> {
    try {
      console.log(`Testing custom endpoint: ${url}`);
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 20000); // 20 second timeout for cold start
      
      const response = await fetch(`${url}/api/health`, {
        method: 'GET',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        const data = await response.json();
        console.log(`✅ Custom endpoint working: ${url}`, data);
        return true;
      } else {
        console.log(`❌ Custom endpoint responded with status: ${response.status}`);
        return false;
      }
    } catch (error) {
      console.log(`❌ Custom endpoint failed: ${url}`, error);
      return false;
    }
  }
}

export const apiService = new ApiService();
