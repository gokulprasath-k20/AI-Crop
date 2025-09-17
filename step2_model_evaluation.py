# STEP 2: MODEL BUILDING AND EVALUATION
# AI-Based Crop Recommendation System for SIH 2025

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Try to import XGBoost
try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
    print("✓ XGBoost is available")
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️ XGBoost not found. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "xgboost"])
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
    print("✓ XGBoost installed and imported successfully")

print("=" * 60)
print("AI-BASED CROP RECOMMENDATION SYSTEM - STEP 2")
print("Model Building and Evaluation")
print("=" * 60)

# Load preprocessed data
try:
    X_train = pd.read_csv('X_train.csv')
    X_test = pd.read_csv('X_test.csv')
    y_train = pd.read_csv('y_train.csv').iloc[:, 0]  # Get the series
    y_test = pd.read_csv('y_test.csv').iloc[:, 0]    # Get the series
    
    print("✓ Preprocessed data loaded successfully!")
    print(f"Training set: {X_train.shape}")
    print(f"Testing set: {X_test.shape}")
    print(f"Number of classes: {len(y_train.unique())}")
    
except FileNotFoundError:
    print("❌ Error: Preprocessed data files not found.")
    print("Please run step1_data_preprocessing.py first.")
    exit()

# Encode labels for XGBoost (requires numerical labels)
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

print("\n" + "=" * 60)
print("MODEL TRAINING AND EVALUATION")
print("=" * 60)

# Dictionary to store model results
model_results = {}

# Define models to test
models = {
    'Random Forest': RandomForestClassifier(random_state=42, n_jobs=-1),
    'XGBoost': XGBClassifier(random_state=42, eval_metric='mlogloss', n_jobs=-1),
    'Support Vector Machine': SVC(random_state=42),
    'Gaussian Naive Bayes': GaussianNB()
}

print(f"🚀 Training and evaluating {len(models)} models...\n")

for model_name, model in models.items():
    print(f"{'='*20} {model_name} {'='*20}")
    
    # Train the model
    print("🔄 Training model...")
    if model_name == 'XGBoost':
        # XGBoost requires encoded labels
        model.fit(X_train, y_train_encoded)
        y_pred_encoded = model.predict(X_test)
        # Convert back to original labels
        y_pred = label_encoder.inverse_transform(y_pred_encoded)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"✓ Training completed!")
    print(f"🎯 Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Store results
    model_results[model_name] = {
        'model': model,
        'accuracy': accuracy,
        'predictions': y_pred
    }
    
    # Classification Report
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Confusion Matrix
    print("🔍 Generating confusion matrix...")
    cm = confusion_matrix(y_test, y_pred)
    
    # Plot confusion matrix
    plt.figure(figsize=(12, 10))
    
    # Get unique labels for the matrix
    unique_labels = sorted(y_test.unique())
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=unique_labels, yticklabels=unique_labels,
                cbar_kws={'shrink': 0.8})
    plt.title(f'Confusion Matrix - {model_name}', fontsize=14, fontweight='bold')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    # Save confusion matrix
    filename = f'confusion_matrix_{model_name.lower().replace(" ", "_")}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"✓ Confusion matrix saved as: {filename}")
    print("\n" + "-"*60 + "\n")

print("=" * 60)
print("MODEL COMPARISON AND RESULTS")
print("=" * 60)

# Sort models by accuracy
sorted_results = sorted(model_results.items(), key=lambda x: x[1]['accuracy'], reverse=True)

print("🏆 Model Performance Ranking:")
print("-" * 40)
for i, (model_name, results) in enumerate(sorted_results, 1):
    accuracy = results['accuracy']
    print(f"{i}. {model_name}: {accuracy:.4f} ({accuracy*100:.2f}%)")

# Identify best model
best_model_name = sorted_results[0][0]
best_model_accuracy = sorted_results[0][1]['accuracy']
best_model = sorted_results[0][1]['model']

print(f"\n🥇 BEST PERFORMING MODEL: {best_model_name}")
print(f"   Accuracy: {best_model_accuracy:.4f} ({best_model_accuracy*100:.2f}%)")

# Create comparison visualization
plt.figure(figsize=(12, 8))

# Bar plot of accuracies
model_names = list(model_results.keys())
accuracies = [model_results[name]['accuracy'] for name in model_names]

bars = plt.bar(model_names, accuracies, color=['gold' if name == best_model_name else 'skyblue' for name in model_names],
               edgecolor='black', linewidth=1.2)

# Add accuracy values on top of bars
for bar, acc in zip(bars, accuracies):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
             f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')

plt.title('Model Performance Comparison', fontsize=16, fontweight='bold')
plt.xlabel('Models', fontsize=12)
plt.ylabel('Accuracy', fontsize=12)
plt.ylim(0, 1.1)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)

# Highlight best model
plt.axhline(y=best_model_accuracy, color='red', linestyle='--', alpha=0.7, 
            label=f'Best: {best_model_name} ({best_model_accuracy:.3f})')
plt.legend()

plt.tight_layout()
plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Detailed analysis of best model
print(f"\n" + "=" * 60)
print(f"DETAILED ANALYSIS - {best_model_name}")
print("=" * 60)

best_predictions = model_results[best_model_name]['predictions']

# Per-class accuracy
print("\n📈 Per-class Performance:")
print("-" * 30)
unique_classes = sorted(y_test.unique())
for crop in unique_classes:
    mask = y_test == crop
    if mask.sum() > 0:  # If there are samples for this crop
        crop_accuracy = accuracy_score(y_test[mask], best_predictions[mask])
        print(f"{crop}: {crop_accuracy:.4f} ({crop_accuracy*100:.1f}%)")

# Feature importance (if available)
if hasattr(best_model, 'feature_importances_'):
    print(f"\n🔍 Feature Importance ({best_model_name}):")
    print("-" * 40)
    feature_names = X_train.columns
    importances = best_model.feature_importances_
    
    # Sort features by importance
    feature_importance = list(zip(feature_names, importances))
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    
    for feature, importance in feature_importance:
        print(f"{feature}: {importance:.4f}")
    
    # Plot feature importance
    plt.figure(figsize=(10, 6))
    features, importance_values = zip(*feature_importance)
    plt.barh(features, importance_values, color='lightgreen', edgecolor='black')
    plt.title(f'Feature Importance - {best_model_name}', fontsize=14, fontweight='bold')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.savefig(f'feature_importance_{best_model_name.lower().replace(" ", "_")}.png', 
                dpi=300, bbox_inches='tight')
    plt.show()

# Save model results summary
results_summary = {
    'model_performances': {name: results['accuracy'] for name, results in model_results.items()},
    'best_model': best_model_name,
    'best_accuracy': best_model_accuracy
}

import json
with open('model_results_summary.json', 'w') as f:
    json.dump(results_summary, f, indent=2)

print("\n" + "=" * 60)
print("STEP 2 COMPLETED SUCCESSFULLY! 🎉")
print("=" * 60)
print("Summary:")
print(f"✓ {len(models)} models trained and evaluated")
print(f"✓ Best model: {best_model_name} with {best_model_accuracy*100:.2f}% accuracy")
print("✓ Confusion matrices generated for all models")
print("✓ Model comparison visualization saved")
print("✓ Results summary saved to model_results_summary.json")
print(f"\nReady for Step 3: Hyperparameter tuning of {best_model_name}!")
