# 🌐 PUBLIC DEPLOYMENT GUIDE - SIH 2025 Crop Recommendation System

## 🎯 **DEPLOYMENT OPTIONS FOR PUBLIC ACCESS**

### **Option 1: Cloud Deployment (RECOMMENDED)**

#### 🔥 **A. Heroku Deployment (Free/Easy)**

1. **Prepare for Heroku:**
```bash
# Install Heroku CLI
# Create these files:
```

**requirements.txt:**
```
Flask==2.3.3
gunicorn==21.2.0
requests==2.31.0
```

**Procfile:**
```
web: gunicorn final_working_api:app
```

**runtime.txt:**
```
python-3.11.5
```

2. **Deploy to Heroku:**
```bash
# Login to Heroku
heroku login

# Create app
heroku create sih2025-crop-recommendation

# Deploy
git init
git add .
git commit -m "SIH 2025 Crop Recommendation System"
git push heroku main

# Your app will be live at:
# https://sih2025-crop-recommendation.herokuapp.com
```

#### ☁️ **B. Railway Deployment (Modern & Fast)**

1. **Connect GitHub repository**
2. **Deploy with one click**
3. **Automatic HTTPS and custom domain**

**railway.json:**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn final_working_api:app",
    "healthcheckPath": "/api/health"
  }
}
```

#### 🌊 **C. Render Deployment (Free Tier)**

1. **Connect your GitHub repo**
2. **Auto-deploy on push**
3. **Free SSL certificates**

**render.yaml:**
```yaml
services:
  - type: web
    name: sih2025-crop-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn final_working_api:app
    healthCheckPath: /api/health
```

### **Option 2: VPS/Server Deployment**

#### 🖥️ **A. DigitalOcean Droplet**

```bash
# Create Ubuntu droplet
# SSH into server
ssh root@your-server-ip

# Install dependencies
apt update
apt install python3 python3-pip nginx

# Upload your code
scp -r /path/to/your/project root@your-server-ip:/var/www/

# Install requirements
cd /var/www/Hackathon
pip3 install -r requirements.txt

# Setup systemd service
sudo nano /etc/systemd/system/crop-api.service
```

**crop-api.service:**
```ini
[Unit]
Description=SIH 2025 Crop Recommendation API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/Hackathon
ExecStart=/usr/bin/python3 final_working_api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl enable crop-api
sudo systemctl start crop-api

# Configure Nginx
sudo nano /etc/nginx/sites-available/crop-api
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **Option 3: Serverless Deployment**

#### ⚡ **A. Vercel (Frontend + API)**

**vercel.json:**
```json
{
  "functions": {
    "api/recommend.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/$1" }
  ]
}
```

#### 🔥 **B. Netlify Functions**

**netlify.toml:**
```toml
[build]
  functions = "functions"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
```

### **Option 4: Container Deployment**

#### 🐳 **Docker Deployment**

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["python", "final_working_api.py"]
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  crop-api:
    build: .
    ports:
      - "5002:5002"
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

```bash
# Build and run
docker-compose up -d

# Deploy to cloud
docker tag your-app your-registry/crop-api
docker push your-registry/crop-api
```

## 📱 **MOBILE APP DEPLOYMENT**

### **React Native App**

**config.js:**
```javascript
const API_CONFIG = {
  development: 'http://localhost:5002',
  production: 'https://your-deployed-api.com'
};

export const API_BASE_URL = __DEV__ 
  ? API_CONFIG.development 
  : API_CONFIG.production;
```

### **Flutter App**

**lib/config/api_config.dart:**
```dart
class ApiConfig {
  static const String baseUrl = kDebugMode 
    ? 'http://localhost:5002'
    : 'https://your-deployed-api.com';
}
```

## 🌐 **DOMAIN & SSL SETUP**

### **Custom Domain:**
1. **Buy domain** (GoDaddy, Namecheap)
2. **Point DNS** to your server/service
3. **Setup SSL** (Let's Encrypt, Cloudflare)

### **Cloudflare Setup:**
```bash
# Add your domain to Cloudflare
# Enable SSL/TLS encryption
# Setup caching rules for better performance
```

## 📊 **MONITORING & ANALYTICS**

### **Health Monitoring:**
```python
# Add to your API
@app.route('/api/status')
def system_status():
    return jsonify({
        "status": "healthy",
        "uptime": get_uptime(),
        "requests_served": get_request_count(),
        "memory_usage": get_memory_usage()
    })
```

### **Analytics Integration:**
```javascript
// Google Analytics for mobile app
import analytics from '@react-native-firebase/analytics';

const trackCropRecommendation = async (cropData) => {
  await analytics().logEvent('crop_recommendation', {
    crop_recommended: cropData.crop,
    yield_predicted: cropData.yield,
    state: 'jharkhand'
  });
};
```

## 🔒 **SECURITY & PERFORMANCE**

### **API Security:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/recommend', methods=['POST'])
@limiter.limit("10 per minute")
def recommend_crop():
    # Your existing code
```

### **CORS Configuration:**
```python
from flask_cors import CORS

CORS(app, origins=[
    "https://your-mobile-app.com",
    "https://your-website.com"
])
```

## 🚀 **QUICK DEPLOYMENT STEPS**

### **Fastest Option - Railway:**

1. **Push code to GitHub**
2. **Connect Railway to GitHub**
3. **Deploy with one click**
4. **Get public URL instantly**

### **Most Reliable - Heroku:**

```bash
# 1. Install Heroku CLI
# 2. Create requirements.txt and Procfile
# 3. Deploy
heroku create your-app-name
git push heroku main
# 4. Your API is live!
```

### **Most Scalable - AWS/Google Cloud:**

1. **Use AWS Elastic Beanstalk**
2. **Or Google Cloud Run**
3. **Auto-scaling enabled**
4. **Global CDN distribution**

## 📱 **MOBILE APP STORES**

### **Google Play Store:**
1. **Build APK/AAB**
2. **Create developer account**
3. **Upload and publish**

### **Apple App Store:**
1. **Build IPA file**
2. **Apple Developer account**
3. **App Store Connect upload**

## 🎯 **RECOMMENDED DEPLOYMENT STRATEGY**

### **For SIH 2025 Demo:**
1. **Railway/Heroku** - Quick public API
2. **GitHub Pages** - Host documentation
3. **Mobile app** - TestFlight/Play Console

### **For Production:**
1. **AWS/Google Cloud** - Scalable backend
2. **Cloudflare** - CDN and security
3. **App Stores** - Mobile distribution
4. **Custom domain** - Professional presence

## 💡 **DEPLOYMENT CHECKLIST**

- ✅ **Environment variables** for sensitive data
- ✅ **Error logging** and monitoring
- ✅ **Rate limiting** for API protection
- ✅ **HTTPS/SSL** certificates
- ✅ **Database backup** (if using)
- ✅ **Load testing** before launch
- ✅ **Documentation** for users
- ✅ **Support contact** information

## 🎉 **YOUR SYSTEM IS READY FOR PUBLIC DEPLOYMENT!**

Choose the deployment option that best fits your needs:
- **Quick Demo**: Railway/Heroku
- **Professional**: AWS/Google Cloud
- **Mobile Focus**: App Store deployment

**Your SIH 2025 Crop Recommendation System is ready to serve farmers across Jharkhand and beyond! 🌾🚀**
