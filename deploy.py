#!/usr/bin/env python3
"""
SIH 2025 - One-Click Deployment Script
This script helps you deploy your Crop Recommendation API to various platforms
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class CropAPIDeployer:
    def __init__(self):
        self.project_path = Path(__file__).parent
        self.app_name = "sih2025-crop-api"
        
    def check_requirements(self):
        """Check if all required files exist."""
        required_files = [
            'simple_deployment_app.py',
            'usage_tracker.py',
            'requirements.txt',
            'Procfile',
            'render.yaml',
            'app.py'
        ]
        
        missing_files = []
        for file in required_files:
            if not (self.project_path / file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Missing required files: {', '.join(missing_files)}")
            return False
        
        print("✅ All required files present")
        return True
    
    def test_local_deployment(self):
        """Test the API locally before deployment."""
        print("🧪 Testing local deployment...")
        
        try:
            # Import and test the app
            sys.path.append(str(self.project_path))
            from simple_deployment_app import app
            
            print("✅ App imports successfully")
            
            # Test basic functionality
            with app.test_client() as client:
                # Test home endpoint
                response = client.get('/')
                if response.status_code == 200:
                    print("✅ Home endpoint working")
                else:
                    print(f"❌ Home endpoint failed: {response.status_code}")
                    return False
                
                # Test health endpoint
                response = client.get('/api/health')
                if response.status_code == 200:
                    print("✅ Health endpoint working")
                else:
                    print(f"❌ Health endpoint failed: {response.status_code}")
                    return False
                
                # Test recommendation endpoint
                test_data = {
                    "N": 90, "P": 42, "K": 43,
                    "temperature": 21, "humidity": 82,
                    "ph": 6.5, "rainfall": 203
                }
                
                response = client.post('/api/recommend', 
                                     json=test_data,
                                     content_type='application/json')
                
                if response.status_code == 200:
                    result = response.get_json()
                    crop = result.get('recommendation', {}).get('primary_crop', {}).get('name_english', 'Unknown')
                    print(f"✅ Recommendation endpoint working - Suggested: {crop}")
                else:
                    print(f"❌ Recommendation endpoint failed: {response.status_code}")
                    return False
                
                # Test usage endpoint
                response = client.get('/api/usage')
                if response.status_code == 200:
                    print("✅ Usage tracking working")
                else:
                    print(f"❌ Usage tracking failed: {response.status_code}")
                    return False
            
            print("🎉 Local testing completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Local testing failed: {str(e)}")
            return False
    
    def generate_deployment_info(self):
        """Generate deployment information and URLs."""
        
        deployment_info = {
            "app_name": self.app_name,
            "platforms": {
                "render": {
                    "url": f"https://{self.app_name}.onrender.com",
                    "dashboard": f"https://{self.app_name}.onrender.com/dashboard",
                    "api_docs": f"https://{self.app_name}.onrender.com/",
                    "usage_stats": f"https://{self.app_name}.onrender.com/api/usage"
                },
                "heroku": {
                    "url": f"https://{self.app_name}.herokuapp.com",
                    "dashboard": f"https://{self.app_name}.herokuapp.com/dashboard",
                    "api_docs": f"https://{self.app_name}.herokuapp.com/",
                    "usage_stats": f"https://{self.app_name}.herokuapp.com/api/usage"
                },
                "railway": {
                    "url": f"https://{self.app_name}.railway.app",
                    "dashboard": f"https://{self.app_name}.railway.app/dashboard",
                    "api_docs": f"https://{self.app_name}.railway.app/",
                    "usage_stats": f"https://{self.app_name}.railway.app/api/usage"
                }
            },
            "endpoints": {
                "POST /api/recommend": "Get crop recommendations",
                "GET /api/health": "Check API health",
                "GET /api/crops": "List supported crops",
                "GET /api/usage": "Get usage statistics",
                "GET /dashboard": "View usage dashboard",
                "GET /": "API documentation"
            }
        }
        
        # Save deployment info
        with open(self.project_path / 'deployment_info.json', 'w') as f:
            json.dump(deployment_info, f, indent=2)
        
        return deployment_info
    
    def print_deployment_guide(self, deployment_info):
        """Print comprehensive deployment guide."""
        
        print("\n" + "="*60)
        print("🚀 SIH 2025 CROP API - DEPLOYMENT READY!")
        print("="*60)
        
        print("\n📋 DEPLOYMENT OPTIONS:")
        print("-" * 30)
        
        print("\n1️⃣ RENDER (Recommended - Free)")
        print("   • Connect your GitHub repo to Render")
        print("   • Auto-deploy from render.yaml")
        print(f"   • Your URL: {deployment_info['platforms']['render']['url']}")
        print(f"   • Dashboard: {deployment_info['platforms']['render']['dashboard']}")
        
        print("\n2️⃣ HEROKU (Popular)")
        print("   • heroku create sih2025-crop-api")
        print("   • git push heroku main")
        print(f"   • Your URL: {deployment_info['platforms']['heroku']['url']}")
        
        print("\n3️⃣ RAILWAY (Modern)")
        print("   • Connect GitHub repo to Railway")
        print("   • Automatic deployment")
        print(f"   • Your URL: {deployment_info['platforms']['railway']['url']}")
        
        print("\n📊 USAGE TRACKING FEATURES:")
        print("-" * 30)
        print("✅ Real-time usage statistics")
        print("✅ Daily request tracking")
        print("✅ Crop recommendation analytics")
        print("✅ Interactive web dashboard")
        print("✅ Public API endpoints")
        print("✅ Mobile app ready")
        
        print("\n🔗 API ENDPOINTS:")
        print("-" * 30)
        for endpoint, description in deployment_info['endpoints'].items():
            print(f"   {endpoint:<25} - {description}")
        
        print("\n🧪 TESTING YOUR DEPLOYED API:")
        print("-" * 30)
        print("# Test crop recommendation")
        print("curl -X POST https://your-url/api/recommend \\")
        print("  -H 'Content-Type: application/json' \\")
        print("  -d '{\"N\":90,\"P\":42,\"K\":43,\"temperature\":21,\"humidity\":82,\"ph\":6.5,\"rainfall\":203}'")
        print("\n# Get usage statistics")
        print("curl https://your-url/api/usage")
        
        print("\n📱 MOBILE APP INTEGRATION:")
        print("-" * 30)
        print("const response = await fetch('https://your-url/api/recommend', {")
        print("  method: 'POST',")
        print("  headers: {'Content-Type': 'application/json'},")
        print("  body: JSON.stringify(farmData)")
        print("});")
        
        print("\n🎯 NEXT STEPS:")
        print("-" * 30)
        print("1. Push your code to GitHub")
        print("2. Deploy to your chosen platform")
        print("3. Test your public API")
        print("4. Share your dashboard URL")
        print("5. Monitor usage statistics")
        print("6. Scale based on demand")
        
        print("\n🏆 READY FOR SIH 2025 SUBMISSION!")
        print("="*60)
    
    def run_deployment_check(self):
        """Run complete deployment readiness check."""
        
        print("🌾 SIH 2025 Crop API - Deployment Checker")
        print("="*50)
        
        # Check requirements
        if not self.check_requirements():
            return False
        
        # Test local deployment
        if not self.test_local_deployment():
            return False
        
        # Generate deployment info
        deployment_info = self.generate_deployment_info()
        
        # Print deployment guide
        self.print_deployment_guide(deployment_info)
        
        return True

def main():
    """Main deployment script."""
    
    deployer = CropAPIDeployer()
    
    if deployer.run_deployment_check():
        print("\n✅ Your API is ready for public deployment!")
        print("📊 Start local server: python simple_deployment_app.py")
        print("🌐 View dashboard: http://localhost:5000/dashboard")
    else:
        print("\n❌ Deployment check failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
