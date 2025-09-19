# 🌐 Public Usage Guide - SIH 2025 Crop Recommendation API

## 🎯 How to Get Public Usage for Your Crop API

Your SIH 2025 Crop Recommendation API is now equipped with **comprehensive usage tracking** and ready for public deployment. Here's how to make it publicly accessible and track usage.

## 🚀 Deployment Options for Public Access

### 1. **Render (Recommended - Free)**

Your project is already configured for Render deployment:

```bash
# Your files are ready:
✅ render.yaml - Render configuration
✅ Procfile - Process configuration  
✅ requirements.txt - Dependencies
✅ app.py - Entry point
✅ simple_deployment_app.py - Main application
```

**Steps to deploy on Render:**
1. Push your code to GitHub
2. Connect your GitHub repo to Render
3. Deploy automatically
4. Get public URL: `https://your-app-name.onrender.com`

### 2. **Heroku (Popular Choice)**

```bash
# Install Heroku CLI and deploy
heroku create your-crop-api
git push heroku main
# Get URL: https://your-crop-api.herokuapp.com
```

### 3. **Railway (Modern Platform)**

```bash
# Connect GitHub repo to Railway
# Automatic deployment
# Get URL: https://your-app.railway.app
```

### 4. **Vercel (Serverless)**

```bash
# Install Vercel CLI
npm i -g vercel
vercel --prod
# Get URL: https://your-app.vercel.app
```

## 📊 Usage Tracking Features

Your API now includes comprehensive analytics:

### **Real-time Statistics**
- Total API requests
- Daily usage patterns
- Most recommended crops
- Endpoint usage breakdown
- User location tracking (if provided)

### **Public Endpoints**
```
GET /api/usage - JSON usage statistics
GET /dashboard - Interactive web dashboard
GET /api/health - API health status
GET /api/crops - Supported crops list
POST /api/recommend - Crop recommendations
```

### **Usage Dashboard Features**
- 📈 Daily usage charts
- 🌾 Top recommended crops
- 🔗 Endpoint usage statistics
- 📊 Real-time metrics
- 🔄 Auto-refresh every 30 seconds

## 🧪 Testing Your Public API

### **1. Local Testing**

```bash
# Start your API server
python simple_deployment_app.py

# Test with sample data
python test_usage_tracking.py

# View dashboard
http://localhost:5000/dashboard
```

### **2. API Testing with curl**

```bash
# Test crop recommendation
curl -X POST http://your-public-url/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "N": 90,
    "P": 42, 
    "K": 43,
    "temperature": 21,
    "humidity": 82,
    "ph": 6.5,
    "rainfall": 203
  }'

# Get usage statistics
curl http://your-public-url/api/usage
```

### **3. Mobile App Integration**

```javascript
// React Native example
const getCropRecommendation = async (farmData) => {
  try {
    const response = await fetch('https://your-public-url/api/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(farmData)
    });
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('API Error:', error);
  }
};
```

## 📈 Monitoring Public Usage

### **1. Built-in Analytics Dashboard**

Visit: `https://your-public-url/dashboard`

**Features:**
- Real-time usage metrics
- Daily request charts
- Top recommended crops
- Endpoint usage breakdown
- Auto-refreshing data

### **2. Usage API Endpoint**

```bash
# Get comprehensive usage statistics
GET https://your-public-url/api/usage

# Response format:
{
  "status": "success",
  "usage_statistics": {
    "total_requests": 1250,
    "today_requests": 45,
    "recent_daily_stats": {
      "2025-01-15": 32,
      "2025-01-16": 28,
      "2025-01-17": 45
    },
    "top_recommended_crops": {
      "rice": 156,
      "wheat": 98,
      "maize": 87
    },
    "endpoint_usage": {
      "/api/recommend": 341,
      "/api/health": 89,
      "/api/crops": 67
    }
  }
}
```

### **3. Log File Tracking**

Usage data is automatically saved to `usage_logs.json`:

```json
{
  "total_requests": 1250,
  "daily_stats": {
    "2025-01-17": 45
  },
  "endpoint_stats": {
    "/api/recommend": 341
  },
  "crop_recommendations": {
    "rice": 156,
    "wheat": 98
  }
}
```

## 🌍 Making Your API Public

### **1. Share Your Public URL**

Once deployed, share your API with:
- **Farmers**: Direct access to recommendations
- **Developers**: API integration for mobile apps
- **Researchers**: Agricultural data analysis
- **Government**: Policy making support

### **2. API Documentation**

Your API automatically provides documentation at the root endpoint:

```bash
GET https://your-public-url/
```

**Response includes:**
- Available endpoints
- Supported crops (24 varieties)
- Language support (English, Hindi)
- API version and status

### **3. Public Usage Examples**

**For Farmers:**
```
🌾 Get crop recommendations: https://your-url/dashboard
📊 View usage statistics: https://your-url/api/usage
```

**For Developers:**
```
📱 Mobile integration: POST https://your-url/api/recommend
🔍 API health check: GET https://your-url/api/health
📋 Supported crops: GET https://your-url/api/crops
```

## 🔧 Advanced Usage Tracking

### **1. Custom Analytics**

Add location tracking to your requests:

```python
# In your mobile app, include location
data = {
    "N": 90, "P": 42, "K": 43,
    "temperature": 21, "humidity": 82,
    "ph": 6.5, "rainfall": 203,
    "location": "Ranchi, Jharkhand"  # Optional
}
```

### **2. Usage Alerts**

Set up monitoring for high usage:

```python
# Add to your deployment
if daily_requests > 1000:
    send_alert("High API usage detected!")
```

### **3. Rate Limiting**

Protect your API from abuse:

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)
```

## 🎯 Success Metrics

Track these key metrics for public usage:

### **Engagement Metrics**
- Daily active users
- API requests per day
- Most popular endpoints
- Peak usage hours

### **Agricultural Impact**
- Most recommended crops
- Regional usage patterns
- Seasonal trends
- Farmer adoption rates

### **Technical Performance**
- API response times
- Error rates
- Uptime percentage
- Mobile app integrations

## 🚀 Next Steps for Public Launch

### **1. Pre-Launch Checklist**
- ✅ API deployed and accessible
- ✅ Usage tracking working
- ✅ Dashboard functional
- ✅ Documentation complete
- ✅ Error handling robust

### **2. Launch Strategy**
1. **Soft Launch**: Share with local farmers in Jharkhand
2. **Developer Outreach**: Provide API to mobile app developers
3. **Government Partnership**: Connect with agricultural departments
4. **Scale Up**: Monitor usage and scale infrastructure

### **3. Promotion Ideas**
- Create API documentation website
- Share usage dashboard publicly
- Provide mobile app templates
- Offer developer support
- Showcase success stories

## 🎉 Your API is Ready for Public Use!

**Public URLs after deployment:**
- **Main API**: `https://your-app.onrender.com/`
- **Crop Recommendations**: `https://your-app.onrender.com/api/recommend`
- **Usage Dashboard**: `https://your-app.onrender.com/dashboard`
- **Usage Statistics**: `https://your-app.onrender.com/api/usage`

**Key Features:**
- 🌾 24 crop varieties supported
- 📱 Mobile-ready JSON API
- 📊 Real-time usage analytics
- 🌐 Public dashboard
- 🔍 Comprehensive monitoring
- 🚀 Ready for scale

**Perfect for SIH 2025 submission and real-world deployment! 🏆**
