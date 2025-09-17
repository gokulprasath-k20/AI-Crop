# STEP 1: DATA UNDERSTANDING AND PREPROCESSING
# AI-Based Crop Recommendation System for SIH 2025

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("AI-BASED CROP RECOMMENDATION SYSTEM - STEP 1")
print("Data Understanding and Preprocessing")
print("=" * 60)

# Load the dataset
try:
    df = pd.read_csv('Crop_recommendation.csv')
    print("✓ Dataset loaded successfully!")
    print(f"Dataset shape: {df.shape}")
except FileNotFoundError:
    print("❌ Error: Crop_recommendation.csv not found in the current directory.")
    print("Please download the dataset from Kaggle and place it in the same directory.")
    print("Dataset URL: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset")
    exit()

print("\n" + "=" * 60)
print("1. DATASET OVERVIEW")
print("=" * 60)

# Display first 5 rows
print("\n📊 First 5 rows of the dataset:")
print(df.head())

# Column information
print("\n📋 Dataset Information:")
print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")
print("\nColumn names and data types:")
print(df.dtypes)

# Check for missing values
print("\n🔍 Missing values check:")
missing_values = df.isnull().sum()
print(missing_values)
if missing_values.sum() == 0:
    print("✓ No missing values found!")
else:
    print("⚠️ Missing values detected!")

print("\n" + "=" * 60)
print("2. TARGET VARIABLE ANALYSIS")
print("=" * 60)

# Unique crops and their counts
print("\n🌾 Unique crops in the dataset:")
crop_counts = df['label'].value_counts()
print(f"Total number of unique crops: {len(crop_counts)}")
print("\nCrop distribution:")
for crop, count in crop_counts.items():
    print(f"  {crop}: {count} samples")

# Visualize crop distribution
plt.figure(figsize=(15, 8))
plt.subplot(2, 1, 1)
crop_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Distribution of Crops in Dataset', fontsize=14, fontweight='bold')
plt.xlabel('Crops')
plt.ylabel('Number of Samples')
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)

plt.subplot(2, 1, 2)
plt.pie(crop_counts.values, labels=crop_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Crop Distribution (Percentage)', fontsize=14, fontweight='bold')
plt.axis('equal')

plt.tight_layout()
plt.savefig('crop_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "=" * 60)
print("3. NUMERICAL FEATURES ANALYSIS")
print("=" * 60)

# Summary statistics for numerical features
numerical_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
print("\n📈 Summary statistics for numerical features:")
print(df[numerical_features].describe())

# Correlation analysis
print("\n🔗 Correlation matrix:")
correlation_matrix = df[numerical_features].corr()
print(correlation_matrix)

# Visualize correlations
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
plt.title('Feature Correlation Matrix', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

# Distribution plots for each feature
fig, axes = plt.subplots(3, 3, figsize=(15, 12))
axes = axes.ravel()

for i, feature in enumerate(numerical_features):
    axes[i].hist(df[feature], bins=30, color='lightblue', edgecolor='black', alpha=0.7)
    axes[i].set_title(f'Distribution of {feature}', fontweight='bold')
    axes[i].set_xlabel(feature)
    axes[i].set_ylabel('Frequency')
    axes[i].grid(alpha=0.3)

# Remove empty subplot
axes[7].remove()
axes[8].remove()

plt.tight_layout()
plt.savefig('feature_distributions.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "=" * 60)
print("4. DATA PREPROCESSING")
print("=" * 60)

# Separate features and target
X = df[numerical_features]
y = df['label']

print(f"✓ Features (X) shape: {X.shape}")
print(f"✓ Target (y) shape: {y.shape}")

print("\nFeature columns:")
for i, col in enumerate(X.columns):
    print(f"  {i+1}. {col}")

print(f"\nTarget variable: {y.name}")
print(f"Number of unique classes: {y.nunique()}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n✓ Data split completed:")
print(f"  Training set: {X_train.shape[0]} samples ({X_train.shape[0]/len(df)*100:.1f}%)")
print(f"  Testing set: {X_test.shape[0]} samples ({X_test.shape[0]/len(df)*100:.1f}%)")

# Check class distribution in splits
print("\n📊 Class distribution in training set:")
train_dist = y_train.value_counts().sort_index()
for crop, count in train_dist.items():
    print(f"  {crop}: {count} samples")

print("\n📊 Class distribution in testing set:")
test_dist = y_test.value_counts().sort_index()
for crop, count in test_dist.items():
    print(f"  {crop}: {count} samples")

# Save preprocessed data
print("\n💾 Saving preprocessed data...")
X_train.to_csv('X_train.csv', index=False)
X_test.to_csv('X_test.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
y_test.to_csv('y_test.csv', index=False)

print("✓ Preprocessed data saved:")
print("  - X_train.csv")
print("  - X_test.csv") 
print("  - y_train.csv")
print("  - y_test.csv")

print("\n" + "=" * 60)
print("STEP 1 COMPLETED SUCCESSFULLY! 🎉")
print("=" * 60)
print("Summary:")
print(f"✓ Dataset loaded with {df.shape[0]} samples and {df.shape[1]} features")
print(f"✓ {len(crop_counts)} unique crops identified")
print(f"✓ No missing values detected")
print(f"✓ Data split into {X_train.shape[0]} training and {X_test.shape[0]} testing samples")
print("✓ Visualizations saved: crop_distribution.png, correlation_matrix.png, feature_distributions.png")
print("✓ Preprocessed data files saved")
print("\nReady for Step 2: Model Building and Evaluation!")
