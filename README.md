# AI-Based Crop Recommendation System for SIH 2025

## 🌾 Project Overview

This is a comprehensive AI-based crop recommendation system developed for the Smart India Hackathon 2025, specifically designed for farmers in Jharkhand, India. The system provides intelligent crop recommendations based on soil conditions and climate data, along with yield predictions and sustainability scoring.

## 🎯 Key Features

- **Accurate Crop Recommendations**: ML-powered recommendations based on soil NPK, climate conditions
- **Yield Prediction**: Estimates expected crop yield in kg/hectare
- **Sustainability Scoring**: Environmental impact assessment (1-10 scale)
- **Multiple Model Support**: Random Forest, XGBoost, SVM, Naive Bayes
- **Offline Capability**: All models can run locally without internet
- **Multilingual Ready**: Designed for easy integration with regional languages

## 📁 Project Structure

```
Hackathon/
├── step1_data_preprocessing.py      # Data analysis and preprocessing
├── step2_model_evaluation.py        # Model training and comparison
├── step3_model_optimization.py      # Hyperparameter tuning and export
├── step4_prediction_function.py     # Basic prediction functions
├── step5_yield_sustainability.py    # Enhanced features
├── crop_predictor.py               # Basic predictor module
├── enhanced_crop_predictor.py      # Full-featured predictor
├── model files (.pkl)              # Trained ML models
├── data files (.csv)               # Preprocessed datasets
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites

```bash
pip install pandas numpy scikit-learn matplotlib seaborn xgboost joblib
```

### Step 1: Data Preprocessing
```bash
python step1_data_preprocessing.py
```
**Requirements**: Place `Crop_recommendation.csv` in the project directory

### Step 2: Model Training
```bash
python step2_model_evaluation.py
```

### Step 3: Model Optimization
```bash
python step3_model_optimization.py
```

### Step 4: Create Prediction Functions
```bash
python step4_prediction_function.py
```

### Step 5: Add Yield & Sustainability
```bash
python step5_yield_sustainability.py
```

## 🔧 Usage Examples

### Basic Crop Recommendation

```python
from enhanced_crop_predictor import recommend_crop

# Input parameters
result = recommend_crop(
    N=90,           # Nitrogen (kg/ha)
    P=42,           # Phosphorus (kg/ha)  
    K=43,           # Potassium (kg/ha)
    temperature=21, # Temperature (°C)
    humidity=82,    # Humidity (%)
    ph=6.5,         # Soil pH
    rainfall=203    # Rainfall (mm)
)

print(f"Recommended crop: {result['crop']}")
print(f"Expected yield: {result['predicted_yield_kg_per_ha']:,.0f} kg/ha")
print(f"Sustainability score: {result['sustainability_score']}/10")
```

### Comprehensive Analysis

```python
from step5_yield_sustainability import comprehensive_crop_analysis

analysis = comprehensive_crop_analysis(90, 42, 43, 21, 82, 6.5, 203)

print("Primary recommendation:", analysis['primary_recommendation'])
print("Alternative crops:", analysis['alternative_crops'])
```

## 📊 Model Performance

The system evaluates multiple ML algorithms and automatically selects the best performer:

- **Random Forest**: Excellent for feature importance analysis
- **XGBoost**: High accuracy with gradient boosting
- **SVM**: Good for complex decision boundaries  
- **Naive Bayes**: Fast and efficient baseline

Typical accuracy: **95%+** on the crop recommendation dataset.

## 🌱 Supported Crops (23+ varieties)

- **Cereals**: Rice, Wheat, Maize
- **Cash Crops**: Cotton, Sugarcane, Jute, Coffee
- **Fruits**: Mango, Banana, Apple, Orange, Grapes, Papaya, Coconut
- **Vegetables**: Watermelon, Muskmelon, Pomegranate
- **Pulses**: Lentil, Chickpea, Kidney beans, Black gram, Mung bean, Pigeon peas, Moth beans

## 🔬 Technical Details

### Input Parameters
- **N, P, K**: Soil nutrient levels (kg/ha)
- **Temperature**: Average temperature (°C)
- **Humidity**: Relative humidity (%)
- **pH**: Soil pH level (0-14)
- **Rainfall**: Annual rainfall (mm)

### Output Features
- **Crop Recommendation**: Best suited crop
- **Yield Prediction**: Expected yield (kg/ha)
- **Sustainability Score**: Environmental impact (1-10)
- **Confidence Level**: Prediction confidence (if available)

### Yield Calculation Formula
```
Yield = Base_Yield × (
    Nutrient_Factor × 0.4 +
    Temperature_Factor × 0.25 +
    Humidity_Factor × 0.15 +
    pH_Factor × 0.1 +
    Rainfall_Factor × 0.1
) × Random_Factor
```

### Sustainability Scoring
```
Sustainability = (
    Water_Efficiency × 0.3 +
    Fertilizer_Efficiency × 0.25 +
    pH_Adaptability × 0.2 +
    Climate_Adaptability × 0.15 +
    Rainfall_Efficiency × 0.1
)
```

## 📱 Mobile Integration Ready

The system is designed for easy integration into mobile applications:

1. **Lightweight Models**: Optimized .pkl files for mobile deployment
2. **Offline Capability**: No internet required for predictions
3. **Fast Inference**: Sub-second prediction times
4. **JSON Output**: Mobile-friendly data format
5. **Error Handling**: Robust error management

## 🌍 Jharkhand-Specific Features

- **Regional Crop Database**: Includes crops commonly grown in Jharkhand
- **Climate Adaptation**: Optimized for local weather patterns
- **Soil Compatibility**: Considers regional soil characteristics
- **Sustainability Focus**: Emphasizes water conservation and soil health

## 📈 Future Enhancements

1. **Real Yield Data Integration**: Replace simulated yields with actual data
2. **Weather API Integration**: Real-time weather data
3. **Market Price Prediction**: Economic viability analysis
4. **Disease Prediction**: Crop disease risk assessment
5. **Multilingual Interface**: Hindi, Bengali, and local languages
6. **Voice Input/Output**: Speech recognition and synthesis

## 🔧 Customization

### Adding New Crops
```python
# In enhanced_crop_predictor.py, update CROP_DATA
CROP_DATA['new_crop'] = {
    'base_yield': 3000,
    'water_need': 800,
    'fertilizer_efficiency': 0.75
}
```

### Adjusting Sustainability Weights
```python
# Modify weights in calculate_sustainability_score()
sustainability_score = (
    water_score * 0.3 +      # Water efficiency weight
    fertilizer_score * 0.25 + # Fertilizer efficiency weight
    ph_score * 0.2 +         # pH adaptability weight
    climate_score * 0.15 +   # Climate adaptability weight
    rainfall_efficiency * 0.1 # Rainfall efficiency weight
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is developed for Smart India Hackathon 2025. Please refer to the competition guidelines for usage terms.

## 👥 Team

Developed for SIH 2025 - AI-Based Crop Recommendation System for Jharkhand farmers.

## 📞 Support

For technical support or questions:
- Check the troubleshooting section below
- Review the code comments for detailed explanations
- Test with provided sample data

## 🔧 Troubleshooting

### Common Issues

1. **"Dataset not found" error**
   - Download Crop_recommendation.csv from Kaggle
   - Place it in the project root directory

2. **"XGBoost not found" error**
   - Run: `pip install xgboost`
   - The code will auto-install if missing

3. **"Model file not found" error**
   - Run steps 1-3 in sequence to generate model files
   - Check that .pkl files are in the directory

4. **Low prediction accuracy**
   - Verify input parameter ranges
   - Check for data quality issues
   - Consider retraining with more data

### Performance Tips

1. **For faster training**: Use RandomizedSearchCV instead of GridSearchCV
2. **For mobile deployment**: Use joblib for model serialization
3. **For large datasets**: Consider feature selection and dimensionality reduction

---

**Ready to revolutionize agriculture in Jharkhand! 🚀🌾**
