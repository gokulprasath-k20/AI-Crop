# Create Sample Dataset for Testing
# AI-Based Crop Recommendation System for SIH 2025

import pandas as pd
import numpy as np
import random

print("Creating sample Crop Recommendation Dataset...")

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define crop categories and their typical parameter ranges
crops_data = {
    'rice': {
        'N': (80, 120), 'P': (40, 60), 'K': (35, 45),
        'temperature': (20, 27), 'humidity': (80, 90),
        'ph': (5.5, 7.0), 'rainfall': (1500, 2000)
    },
    'wheat': {
        'N': (50, 80), 'P': (30, 50), 'K': (30, 50),
        'temperature': (15, 25), 'humidity': (50, 70),
        'ph': (6.0, 7.5), 'rainfall': (450, 650)
    },
    'maize': {
        'N': (70, 110), 'P': (35, 55), 'K': (20, 40),
        'temperature': (18, 27), 'humidity': (60, 80),
        'ph': (5.8, 7.0), 'rainfall': (600, 1000)
    },
    'cotton': {
        'N': (100, 140), 'P': (40, 70), 'K': (40, 60),
        'temperature': (21, 30), 'humidity': (50, 80),
        'ph': (5.8, 8.0), 'rainfall': (600, 1200)
    },
    'sugarcane': {
        'N': (120, 160), 'P': (50, 80), 'K': (50, 80),
        'temperature': (21, 30), 'humidity': (75, 85),
        'ph': (6.0, 7.5), 'rainfall': (1000, 1500)
    },
    'jute': {
        'N': (40, 80), 'P': (20, 40), 'K': (15, 35),
        'temperature': (24, 35), 'humidity': (70, 90),
        'ph': (6.0, 7.5), 'rainfall': (1000, 2000)
    },
    'coffee': {
        'N': (60, 100), 'P': (30, 50), 'K': (30, 50),
        'temperature': (15, 25), 'humidity': (60, 80),
        'ph': (6.0, 7.0), 'rainfall': (1200, 2000)
    },
    'coconut': {
        'N': (80, 120), 'P': (40, 60), 'K': (60, 100),
        'temperature': (25, 32), 'humidity': (70, 85),
        'ph': (5.5, 7.0), 'rainfall': (1000, 2000)
    },
    'papaya': {
        'N': (100, 140), 'P': (50, 80), 'K': (50, 80),
        'temperature': (22, 32), 'humidity': (60, 85),
        'ph': (6.0, 7.0), 'rainfall': (800, 1200)
    },
    'orange': {
        'N': (80, 120), 'P': (40, 60), 'K': (40, 60),
        'temperature': (15, 30), 'humidity': (50, 80),
        'ph': (6.0, 7.5), 'rainfall': (600, 1200)
    },
    'apple': {
        'N': (60, 100), 'P': (30, 50), 'K': (30, 50),
        'temperature': (15, 25), 'humidity': (60, 80),
        'ph': (6.0, 7.0), 'rainfall': (1000, 1500)
    },
    'muskmelon': {
        'N': (80, 120), 'P': (40, 70), 'K': (50, 80),
        'temperature': (24, 35), 'humidity': (50, 70),
        'ph': (6.0, 7.0), 'rainfall': (400, 600)
    },
    'watermelon': {
        'N': (80, 120), 'P': (40, 70), 'K': (50, 80),
        'temperature': (24, 35), 'humidity': (50, 70),
        'ph': (6.0, 7.0), 'rainfall': (400, 600)
    },
    'grapes': {
        'N': (60, 100), 'P': (35, 55), 'K': (40, 60),
        'temperature': (15, 25), 'humidity': (60, 80),
        'ph': (6.0, 7.0), 'rainfall': (500, 800)
    },
    'mango': {
        'N': (80, 120), 'P': (40, 60), 'K': (40, 60),
        'temperature': (24, 32), 'humidity': (60, 80),
        'ph': (5.5, 7.5), 'rainfall': (800, 1200)
    },
    'banana': {
        'N': (100, 140), 'P': (50, 80), 'K': (60, 100),
        'temperature': (26, 32), 'humidity': (75, 85),
        'ph': (6.0, 7.5), 'rainfall': (1200, 2000)
    },
    'pomegranate': {
        'N': (80, 120), 'P': (40, 60), 'K': (40, 60),
        'temperature': (15, 30), 'humidity': (35, 70),
        'ph': (6.5, 7.5), 'rainfall': (500, 800)
    },
    'lentil': {
        'N': (20, 40), 'P': (20, 40), 'K': (15, 35),
        'temperature': (15, 25), 'humidity': (50, 70),
        'ph': (6.0, 7.5), 'rainfall': (300, 500)
    },
    'blackgram': {
        'N': (20, 40), 'P': (15, 35), 'K': (15, 35),
        'temperature': (25, 35), 'humidity': (60, 80),
        'ph': (6.0, 7.0), 'rainfall': (300, 500)
    },
    'mungbean': {
        'N': (20, 40), 'P': (15, 35), 'K': (15, 35),
        'temperature': (25, 35), 'humidity': (60, 80),
        'ph': (6.2, 7.2), 'rainfall': (250, 400)
    },
    'mothbeans': {
        'N': (15, 35), 'P': (10, 30), 'K': (10, 30),
        'temperature': (27, 35), 'humidity': (50, 70),
        'ph': (6.5, 8.0), 'rainfall': (200, 350)
    },
    'pigeonpeas': {
        'N': (20, 40), 'P': (15, 35), 'K': (15, 35),
        'temperature': (20, 30), 'humidity': (60, 80),
        'ph': (6.0, 7.5), 'rainfall': (350, 500)
    },
    'kidneybeans': {
        'N': (40, 60), 'P': (25, 45), 'K': (20, 40),
        'temperature': (15, 25), 'humidity': (60, 80),
        'ph': (6.0, 7.0), 'rainfall': (400, 600)
    },
    'chickpea': {
        'N': (20, 40), 'P': (20, 40), 'K': (15, 35),
        'temperature': (20, 30), 'humidity': (60, 80),
        'ph': (6.2, 7.8), 'rainfall': (300, 500)
    }
}

# Generate sample data
samples_per_crop = 100
total_samples = len(crops_data) * samples_per_crop

data = []

print(f"Generating {total_samples} samples ({samples_per_crop} per crop)...")

for crop, ranges in crops_data.items():
    for _ in range(samples_per_crop):
        sample = {
            'N': round(np.random.uniform(ranges['N'][0], ranges['N'][1]), 2),
            'P': round(np.random.uniform(ranges['P'][0], ranges['P'][1]), 2),
            'K': round(np.random.uniform(ranges['K'][0], ranges['K'][1]), 2),
            'temperature': round(np.random.uniform(ranges['temperature'][0], ranges['temperature'][1]), 2),
            'humidity': round(np.random.uniform(ranges['humidity'][0], ranges['humidity'][1]), 2),
            'ph': round(np.random.uniform(ranges['ph'][0], ranges['ph'][1]), 2),
            'rainfall': round(np.random.uniform(ranges['rainfall'][0], ranges['rainfall'][1]), 2),
            'label': crop
        }
        data.append(sample)

# Create DataFrame
df = pd.DataFrame(data)

# Shuffle the data
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Add some noise to make it more realistic
noise_factor = 0.05  # 5% noise

for col in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']:
    noise = np.random.normal(0, df[col].std() * noise_factor, len(df))
    df[col] = df[col] + noise
    
    # Ensure values stay within reasonable bounds
    if col in ['humidity']:
        df[col] = np.clip(df[col], 0, 100)
    elif col == 'ph':
        df[col] = np.clip(df[col], 3, 10)
    elif col == 'temperature':
        df[col] = np.clip(df[col], 0, 50)
    else:
        df[col] = np.clip(df[col], 0, None)  # No negative values
    
    # Round to 2 decimal places
    df[col] = df[col].round(2)

# Save the dataset
df.to_csv('Crop_recommendation.csv', index=False)

print(f"✓ Sample dataset created: Crop_recommendation.csv")
print(f"✓ Total samples: {len(df)}")
print(f"✓ Features: {list(df.columns[:-1])}")
print(f"✓ Crops: {len(df['label'].unique())}")

# Display basic statistics
print(f"\nDataset Overview:")
print(f"Shape: {df.shape}")
print(f"\nFirst 5 rows:")
print(df.head())

print(f"\nCrop distribution:")
crop_counts = df['label'].value_counts()
for crop, count in crop_counts.items():
    print(f"  {crop}: {count}")

print(f"\nBasic statistics:")
print(df.describe())

print(f"\n✅ Sample dataset ready for testing!")
print(f"You can now run the main scripts without downloading from Kaggle.")
