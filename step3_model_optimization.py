# STEP 3: MODEL OPTIMIZATION AND EXPORT
# AI-Based Crop Recommendation System for SIH 2025

import pandas as pd
import numpy as np
import json
import joblib
import pickle
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Try to import XGBoost
try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️ XGBoost not available")

print("=" * 60)
print("AI-BASED CROP RECOMMENDATION SYSTEM - STEP 3")
print("Model Optimization and Export")
print("=" * 60)

# Load preprocessed data
try:
    X_train = pd.read_csv('X_train.csv')
    X_test = pd.read_csv('X_test.csv')
    y_train = pd.read_csv('y_train.csv').iloc[:, 0]
    y_test = pd.read_csv('y_test.csv').iloc[:, 0]
    
    print("✓ Preprocessed data loaded successfully!")
    
except FileNotFoundError:
    print("❌ Error: Preprocessed data files not found.")
    print("Please run step1_data_preprocessing.py first.")
    exit()

# Load model results to identify best model
try:
    with open('model_results_summary.json', 'r') as f:
        results_summary = json.load(f)
    
    best_model_name = results_summary['best_model']
    best_baseline_accuracy = results_summary['best_accuracy']
    
    print(f"✓ Best model from Step 2: {best_model_name}")
    print(f"✓ Baseline accuracy: {best_baseline_accuracy:.4f} ({best_baseline_accuracy*100:.2f}%)")
    
except FileNotFoundError:
    print("❌ Error: model_results_summary.json not found.")
    print("Please run step2_model_evaluation.py first.")
    exit()

print("\n" + "=" * 60)
print("HYPERPARAMETER TUNING")
print("=" * 60)

# Prepare label encoder for XGBoost if needed
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Define hyperparameter grids for each model
hyperparameter_grids = {
    'Random Forest': {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30, None],
        'max_features': ['sqrt', 'log2', None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    },
    'XGBoost': {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 6, 10],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.8, 0.9, 1.0],
        'colsample_bytree': [0.8, 0.9, 1.0]
    },
    'Support Vector Machine': {
        'C': [0.1, 1, 10, 100],
        'kernel': ['rbf', 'poly', 'sigmoid'],
        'gamma': ['scale', 'auto', 0.001, 0.01, 0.1]
    },
    'Gaussian Naive Bayes': {
        'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]
    }
}

# Initialize the best model
if best_model_name == 'Random Forest':
    base_model = RandomForestClassifier(random_state=42, n_jobs=-1)
    param_grid = hyperparameter_grids['Random Forest']
    use_encoded_labels = False
elif best_model_name == 'XGBoost':
    base_model = XGBClassifier(random_state=42, eval_metric='mlogloss', n_jobs=-1)
    param_grid = hyperparameter_grids['XGBoost']
    use_encoded_labels = True
elif best_model_name == 'Support Vector Machine':
    base_model = SVC(random_state=42)
    param_grid = hyperparameter_grids['Support Vector Machine']
    use_encoded_labels = False
elif best_model_name == 'Gaussian Naive Bayes':
    base_model = GaussianNB()
    param_grid = hyperparameter_grids['Gaussian Naive Bayes']
    use_encoded_labels = False

print(f"🔧 Tuning hyperparameters for {best_model_name}...")
print(f"Parameter grid: {param_grid}")

# Use RandomizedSearchCV for faster tuning (especially for large grids)
if len(param_grid) > 3 or any(len(v) > 5 for v in param_grid.values()):
    print("🎲 Using RandomizedSearchCV for faster tuning...")
    search_cv = RandomizedSearchCV(
        base_model, 
        param_grid, 
        n_iter=50,  # Number of parameter settings sampled
        cv=5, 
        scoring='accuracy',
        n_jobs=-1, 
        random_state=42,
        verbose=1
    )
else:
    print("🔍 Using GridSearchCV for exhaustive search...")
    search_cv = GridSearchCV(
        base_model, 
        param_grid, 
        cv=5, 
        scoring='accuracy',
        n_jobs=-1,
        verbose=1
    )

# Fit the search
print("⏳ Starting hyperparameter search... This may take a few minutes.")

if use_encoded_labels:
    search_cv.fit(X_train, y_train_encoded)
else:
    search_cv.fit(X_train, y_train)

print("✓ Hyperparameter tuning completed!")

# Get best parameters and score
best_params = search_cv.best_params_
best_cv_score = search_cv.best_score_

print(f"\n🏆 Best parameters found:")
for param, value in best_params.items():
    print(f"  {param}: {value}")

print(f"\n📊 Best cross-validation score: {best_cv_score:.4f} ({best_cv_score*100:.2f}%)")
print(f"📈 Improvement over baseline: {(best_cv_score - best_baseline_accuracy)*100:.2f} percentage points")

print("\n" + "=" * 60)
print("FINAL MODEL TRAINING AND EVALUATION")
print("=" * 60)

# Train final model with best parameters
print("🚀 Training final optimized model...")
final_model = search_cv.best_estimator_

# Make predictions
if use_encoded_labels:
    y_pred_encoded = final_model.predict(X_test)
    y_pred = label_encoder.inverse_transform(y_pred_encoded)
else:
    y_pred = final_model.predict(X_test)

# Calculate final accuracy
final_accuracy = accuracy_score(y_test, y_pred)

print(f"✓ Final model training completed!")
print(f"🎯 Final test accuracy: {final_accuracy:.4f} ({final_accuracy*100:.2f}%)")
print(f"📈 Improvement over baseline: {(final_accuracy - best_baseline_accuracy)*100:.2f} percentage points")

# Detailed evaluation
print(f"\n📊 Detailed Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion matrix for final model
print("🔍 Generating final confusion matrix...")
cm = confusion_matrix(y_test, y_pred)
unique_labels = sorted(y_test.unique())

plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', 
            xticklabels=unique_labels, yticklabels=unique_labels,
            cbar_kws={'shrink': 0.8})
plt.title(f'Final Optimized Model Confusion Matrix - {best_model_name}', 
          fontsize=14, fontweight='bold')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('final_model_confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

# Feature importance for final model (if available)
if hasattr(final_model, 'feature_importances_'):
    print(f"\n🔍 Final Model Feature Importance:")
    print("-" * 40)
    feature_names = X_train.columns
    importances = final_model.feature_importances_
    
    feature_importance = list(zip(feature_names, importances))
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    
    for feature, importance in feature_importance:
        print(f"{feature}: {importance:.4f}")
    
    # Plot final feature importance
    plt.figure(figsize=(10, 6))
    features, importance_values = zip(*feature_importance)
    plt.barh(features, importance_values, color='lightcoral', edgecolor='black')
    plt.title(f'Final Model Feature Importance - {best_model_name}', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.savefig('final_model_feature_importance.png', dpi=300, bbox_inches='tight')
    plt.show()

print("\n" + "=" * 60)
print("MODEL EXPORT")
print("=" * 60)

# Save the final model
model_filename = f'crop_recommendation_model_{best_model_name.lower().replace(" ", "_")}.pkl'

print(f"💾 Saving final model as {model_filename}...")

# Save using joblib (recommended for scikit-learn models)
joblib.dump(final_model, model_filename)
print(f"✓ Model saved using joblib")

# Also save using pickle as backup
pickle_filename = f'crop_recommendation_model_{best_model_name.lower().replace(" ", "_")}_pickle.pkl'
with open(pickle_filename, 'wb') as f:
    pickle.dump(final_model, f)
print(f"✓ Model also saved using pickle as {pickle_filename}")

# Save label encoder if used
if use_encoded_labels:
    joblib.dump(label_encoder, 'label_encoder.pkl')
    print("✓ Label encoder saved as label_encoder.pkl")

# Save model metadata
model_metadata = {
    'model_name': best_model_name,
    'model_type': type(final_model).__name__,
    'best_parameters': best_params,
    'final_accuracy': final_accuracy,
    'baseline_accuracy': best_baseline_accuracy,
    'improvement': final_accuracy - best_baseline_accuracy,
    'cv_score': best_cv_score,
    'feature_names': list(X_train.columns),
    'target_classes': sorted(y_train.unique()),
    'uses_encoded_labels': use_encoded_labels,
    'training_samples': len(X_train),
    'test_samples': len(X_test)
}

with open('model_metadata.json', 'w') as f:
    json.dump(model_metadata, f, indent=2)

print("✓ Model metadata saved as model_metadata.json")

# Test model loading
print(f"\n🧪 Testing model loading...")
try:
    loaded_model = joblib.load(model_filename)
    
    # Test prediction
    if use_encoded_labels:
        loaded_label_encoder = joblib.load('label_encoder.pkl')
        test_pred_encoded = loaded_model.predict(X_test[:5])
        test_pred = loaded_label_encoder.inverse_transform(test_pred_encoded)
    else:
        test_pred = loaded_model.predict(X_test[:5])
    
    print("✓ Model loaded and tested successfully!")
    print(f"Sample predictions: {test_pred}")
    
except Exception as e:
    print(f"❌ Error loading model: {e}")

print("\n" + "=" * 60)
print("STEP 3 COMPLETED SUCCESSFULLY! 🎉")
print("=" * 60)
print("Summary:")
print(f"✓ Hyperparameter tuning completed for {best_model_name}")
print(f"✓ Final model accuracy: {final_accuracy*100:.2f}%")
print(f"✓ Improvement: {(final_accuracy - best_baseline_accuracy)*100:.2f} percentage points")
print(f"✓ Model saved as: {model_filename}")
print(f"✓ Backup saved as: {pickle_filename}")
print("✓ Model metadata saved")
print("✓ Model loading tested successfully")
print("\nReady for Step 4: Building the prediction function!")
