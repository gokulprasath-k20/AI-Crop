# Complete AI-Based Crop Recommendation System
# Smart India Hackathon 2025 - Execute All Steps
# This script runs the entire pipeline from data creation to final testing

import os
import sys
import subprocess
import time

def run_script(script_name, description):
    """Run a Python script and handle errors."""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*60}")
    
    try:
        start_time = time.time()
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        end_time = time.time()
        
        print(f"✅ SUCCESS: {description}")
        print(f"⏱️ Execution time: {end_time - start_time:.2f} seconds")
        
        # Print last few lines of output for confirmation
        output_lines = result.stdout.strip().split('\n')
        if len(output_lines) > 5:
            print("📄 Last few lines of output:")
            for line in output_lines[-5:]:
                print(f"   {line}")
        else:
            print("📄 Output:")
            print(result.stdout)
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {description} failed!")
        print(f"Error code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
        return False

def check_file_exists(filename):
    """Check if a file exists."""
    exists = os.path.exists(filename)
    status = "✅" if exists else "❌"
    print(f"{status} {filename}")
    return exists

def main():
    """Run the complete crop recommendation system pipeline."""
    
    print("🌾" * 30)
    print("AI-BASED CROP RECOMMENDATION SYSTEM")
    print("Smart India Hackathon 2025")
    print("Complete Pipeline Execution")
    print("🌾" * 30)
    
    # Check if we're in the right directory
    expected_files = ['step1_data_preprocessing.py', 'step2_model_evaluation.py']
    if not all(os.path.exists(f) for f in expected_files):
        print("❌ Error: Not in the correct directory or files missing!")
        print("Please ensure you're in the Hackathon directory with all step files.")
        return False
    
    # Step 0: Create sample dataset if Crop_recommendation.csv doesn't exist
    if not os.path.exists('Crop_recommendation.csv'):
        print("\n📊 Crop_recommendation.csv not found. Creating sample dataset...")
        if not run_script('create_sample_dataset.py', 'Creating Sample Dataset'):
            print("❌ Failed to create sample dataset. Exiting.")
            return False
    else:
        print("\n✅ Crop_recommendation.csv found. Using existing dataset.")
    
    # Pipeline steps
    steps = [
        ('step1_data_preprocessing.py', 'Data Understanding and Preprocessing'),
        ('step2_model_evaluation.py', 'Model Building and Evaluation'),
        ('step3_model_optimization.py', 'Model Optimization and Export'),
        ('step4_prediction_function.py', 'Building Prediction Function'),
        ('step5_yield_sustainability.py', 'Yield Prediction and Sustainability')
    ]
    
    successful_steps = 0
    total_start_time = time.time()
    
    for script, description in steps:
        if run_script(script, description):
            successful_steps += 1
        else:
            print(f"\n❌ Pipeline stopped at: {description}")
            print("Please check the error messages above and fix any issues.")
            break
    
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    
    print(f"\n{'='*60}")
    print("PIPELINE EXECUTION SUMMARY")
    print(f"{'='*60}")
    
    print(f"✅ Successful steps: {successful_steps}/{len(steps)}")
    print(f"⏱️ Total execution time: {total_time:.2f} seconds")
    
    if successful_steps == len(steps):
        print("\n🎉 COMPLETE SUCCESS! All steps executed successfully!")
        
        print(f"\n📁 Generated Files Check:")
        important_files = [
            'Crop_recommendation.csv',
            'X_train.csv', 'X_test.csv', 'y_train.csv', 'y_test.csv',
            'model_results_summary.json',
            'model_metadata.json',
            'crop_predictor.py',
            'enhanced_crop_predictor.py'
        ]
        
        all_files_present = True
        for file in important_files:
            if not check_file_exists(file):
                all_files_present = False
        
        # Check for model files (name depends on best model)
        model_files_found = False
        for file in os.listdir('.'):
            if file.startswith('crop_recommendation_model_') and file.endswith('.pkl'):
                print(f"✅ {file}")
                model_files_found = True
                break
        
        if not model_files_found:
            print("❌ No model .pkl files found")
            all_files_present = False
        
        print(f"\n🧪 Testing the Final System:")
        try:
            # Test the enhanced predictor
            import enhanced_crop_predictor
            
            test_result = enhanced_crop_predictor.recommend_crop(
                N=90, P=42, K=43, temperature=21, 
                humidity=82, ph=6.5, rainfall=203
            )
            
            if 'error' not in test_result:
                print("✅ Final system test PASSED!")
                print(f"   Recommended crop: {test_result['crop']}")
                print(f"   Predicted yield: {test_result['predicted_yield_kg_per_ha']:,.0f} kg/ha")
                print(f"   Sustainability score: {test_result['sustainability_score']}/10")
            else:
                print(f"❌ Final system test FAILED: {test_result['error']}")
                all_files_present = False
                
        except Exception as e:
            print(f"❌ Final system test ERROR: {str(e)}")
            all_files_present = False
        
        if all_files_present:
            print(f"\n🚀 SYSTEM READY FOR DEPLOYMENT!")
            print(f"📱 The AI-based crop recommendation system is ready for mobile integration.")
            print(f"📖 Check README.md for detailed usage instructions.")
        else:
            print(f"\n⚠️ Some files are missing. Please check the pipeline execution.")
            
    else:
        print(f"\n❌ Pipeline incomplete. {len(steps) - successful_steps} steps failed.")
        print("Please review the error messages and run individual steps as needed.")
    
    print(f"\n{'='*60}")
    print("NEXT STEPS FOR SIH 2025:")
    print(f"{'='*60}")
    print("1. 📱 Integrate with mobile app framework (React Native/Flutter)")
    print("2. 🗣️ Add voice input/output capabilities")
    print("3. 🌐 Implement multilingual support (Hindi, Bengali, etc.)")
    print("4. 📡 Add offline data synchronization")
    print("5. 🎨 Design farmer-friendly UI/UX")
    print("6. 🧪 Test with real farmers in Jharkhand")
    print("7. 📊 Integrate real yield and market data")
    print("8. 🔒 Implement data privacy and security measures")
    
    return successful_steps == len(steps)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
