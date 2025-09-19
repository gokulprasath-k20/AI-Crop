# Crop Recommendation Frontend

A modern React Native mobile application built with Expo for crop recommendation based on soil and environmental data.

## Features

### 🌾 Crop Recommendation
- **Interactive Form**: Easy-to-use form for entering soil parameters (N, P, K, pH, temperature, humidity, rainfall)
- **Real-time Validation**: Input validation with helpful error messages
- **Beautiful Results**: Displays primary crop recommendation with confidence score, yield prediction, and sustainability rating
- **Alternative Crops**: Shows 3 alternative crop suggestions with their metrics
- **Bilingual Support**: Crop names displayed in both English and Hindi

### ⚙️ Settings & Configuration
- **Backend Configuration**: Easy setup for connecting to different backend URLs
- **Connection Testing**: Test backend connectivity with real-time status updates
- **Preset URLs**: Quick selection for common deployment scenarios (local, network, cloud)
- **System Information**: Displays backend health and system details
- **Crop Information**: Educational content about supported crops

### 🎨 Modern UI/UX
- **Agricultural Theme**: Green gradient design reflecting agricultural focus
- **Responsive Design**: Works on various screen sizes
- **Smooth Animations**: Loading states and transitions
- **Intuitive Navigation**: Tab-based navigation with meaningful icons
- **Accessibility**: Proper contrast ratios and touch targets

## Technical Stack

- **Framework**: React Native with Expo
- **Language**: TypeScript
- **Navigation**: Expo Router with tab navigation
- **Styling**: StyleSheet with LinearGradient
- **Icons**: Expo Vector Icons (Ionicons)
- **HTTP Client**: Fetch API
- **State Management**: React Hooks (useState, useEffect)

## Project Structure

```
Crop/
├── app/
│   ├── (tabs)/
│   │   ├── index.tsx          # Main crop recommendation screen
│   │   ├── explore.tsx        # Settings and information screen
│   │   └── _layout.tsx        # Tab navigation layout
│   ├── _layout.tsx            # Root layout
│   └── modal.tsx              # Modal component
├── services/
│   └── apiService.ts          # Backend API integration
├── components/                # Reusable UI components
├── constants/                 # App constants and themes
├── hooks/                     # Custom React hooks
└── assets/                    # Images and static assets
```

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Expo CLI (`npm install -g @expo/cli`)
- iOS Simulator (Mac) or Android Emulator

### Installation

1. **Navigate to the frontend directory**:
   ```bash
   cd Crop
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Install the missing dependency**:
   ```bash
   npx expo install expo-linear-gradient
   ```

4. **Start the development server**:
   ```bash
   npm start
   ```

5. **Run on device/emulator**:
   - Press `i` for iOS simulator
   - Press `a` for Android emulator
   - Press `w` for web browser
   - Scan QR code with Expo Go app on your phone

### Backend Configuration

1. **Start your Flask backend** (from the main project directory):
   ```bash
   python app.py
   ```

2. **Configure the frontend**:
   - Open the app and go to "Settings & Info" tab
   - Enter your backend URL (default: `http://localhost:5000`)
   - For mobile device testing, use your computer's IP address: `http://192.168.1.XXX:5000`
   - Test the connection to ensure it's working

### Deployment Options

#### For Development
- **Local**: `http://localhost:5000`
- **Network**: `http://[YOUR_IP]:5000`

#### For Production
- **Cloud Deployment**: Update the backend URL in the settings screen
- **Render/Heroku**: `https://your-app-name.onrender.com`

## API Integration

The app integrates with the Flask backend through the `apiService.ts` file:

### Endpoints Used
- `GET /api/health` - Health check and system information
- `POST /api/recommend` - Get crop recommendations
- `GET /api/crops` - Get supported crops list

### Request Format
```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 21,
  "humidity": 82,
  "ph": 6.5,
  "rainfall": 203
}
```

### Response Format
```json
{
  "status": "success",
  "recommendation": {
    "primary_crop": {
      "name_english": "rice",
      "name_hindi": "चावल",
      "confidence": 0.85,
      "predicted_yield_kg_per_ha": 4500,
      "sustainability_score": 8.2
    },
    "alternative_crops": [...]
  },
  "system_info": {
    "model_accuracy": "94%",
    "total_crops_supported": 6,
    "target_region": "Jharkhand, India"
  }
}
```

## Features in Detail

### Crop Recommendation Form
- **Input Fields**: 7 essential parameters for crop prediction
- **Icons**: Each field has a relevant icon for better UX
- **Units**: Clear unit indicators (kg/ha, °C, %, mm)
- **Placeholders**: Example values to guide users
- **Validation**: Real-time validation with error messages

### Results Display
- **Primary Recommendation**: Highlighted best crop with key metrics
- **Confidence Score**: Model confidence as percentage
- **Yield Prediction**: Expected yield in kg/hectare
- **Sustainability Score**: Environmental impact rating (1-10)
- **Alternative Options**: 3 backup crop suggestions
- **Bilingual Names**: English and Hindi names for all crops

### Settings Screen
- **Backend URL Configuration**: Easy backend switching
- **Connection Testing**: Real-time connectivity check
- **System Information**: Backend health and capabilities
- **Crop Database**: Information about all supported crops
- **About Section**: App information and features

## Troubleshooting

### Common Issues

1. **"Cannot find module 'expo-linear-gradient'"**
   ```bash
   npx expo install expo-linear-gradient
   ```

2. **Backend Connection Failed**
   - Ensure Flask backend is running
   - Check the backend URL in settings
   - For mobile testing, use your computer's IP address
   - Verify firewall settings

3. **App Won't Start**
   ```bash
   npm install
   npx expo install --fix
   npm start -- --clear
   ```

4. **TypeScript Errors**
   - Ensure all dependencies are installed
   - Check that the services directory exists
   - Verify import paths are correct

### Development Tips

1. **Hot Reload**: Changes are automatically reflected in the app
2. **Debugging**: Use React Native Debugger or browser dev tools
3. **Logs**: Check terminal output for errors and warnings
4. **Testing**: Test on both iOS and Android for compatibility

## Contributing

1. Follow the existing code structure and naming conventions
2. Use TypeScript for type safety
3. Add proper error handling for API calls
4. Test on multiple devices/screen sizes
5. Update documentation for new features

## License

This project is part of the SIH 2025 submission for crop recommendation system targeting farmers in Jharkhand, India.
