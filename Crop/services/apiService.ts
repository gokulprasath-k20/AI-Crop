// API Service for Crop Recommendation Backend
// Handles communication with Flask backend

export interface SoilData {
  N: number;
  P: number;
  K: number;
  temperature: number;
  humidity: number;
  ph: number;
  rainfall: number;
}

export interface CropRecommendation {
  name_english: string;
  name_hindi: string;
  confidence?: number;
  predicted_yield_kg_per_ha: number;
  sustainability_score: number;
}

export interface ApiResponse {
  status: string;
  timestamp: string;
  recommendation: {
    primary_crop: CropRecommendation;
    alternative_crops: CropRecommendation[];
  };
  system_info: {
    model_accuracy: string;
    total_crops_supported: number;
    target_region: string;
  };
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  supported_crops: number;
  accuracy: string;
  target: string;
}

class ApiService {
  private baseUrl: string;

  constructor() {
    // You can change this to your deployed backend URL
    this.baseUrl = 'http://localhost:5000'; // Change to your backend URL
  }

  setBaseUrl(url: string) {
    this.baseUrl = url;
  }

  async checkHealth(): Promise<HealthResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/health`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }

  async getCropRecommendation(soilData: SoilData): Promise<ApiResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(soilData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Crop recommendation failed:', error);
      throw error;
    }
  }

  async getSupportedCrops() {
    try {
      const response = await fetch(`${this.baseUrl}/api/crops`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to get supported crops:', error);
      throw error;
    }
  }
}

export default new ApiService();
