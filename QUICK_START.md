# 🚀 Quick Start - SIH 2025 Crop API with Public Usage Tracking

## ⚡ Get Started in 3 Steps

### 1. **Start the API Server**
```bash
python simple_deployment_app.py
```

### 2. **View Usage Dashboard**
Open in browser: http://localhost:5000/dashboard

### 3. **Test the API**
```bash
python test_usage_tracking.py
```

## 🌐 Public Deployment

### **Deploy to Render (Free)**
1. Push code to GitHub
2. Connect repo to Render
3. Auto-deploy with `render.yaml`
4. Get public URL: `https://your-app.onrender.com`

### **Deploy to Heroku**
```bash
heroku create sih2025-crop-api
git push heroku main
```

## 📊 Usage Tracking Features

✅ **Real-time Analytics Dashboard**  
✅ **Daily Usage Statistics**  
✅ **Crop Recommendation Tracking**  
✅ **API Endpoint Monitoring**  
✅ **Public Usage API**  
✅ **Mobile App Ready**  

## 🔗 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API documentation |
| `/api/recommend` | POST | Get crop recommendations |
| `/api/health` | GET | Check API health |
| `/api/crops` | GET | List supported crops |
| `/api/usage` | GET | Get usage statistics |
| `/dashboard` | GET | View usage dashboard |

## 📱 Mobile Integration Example

```javascript
// React Native / JavaScript
const getCropRecommendation = async (farmData) => {
  const response = await fetch('https://your-url/api/recommend', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      N: 90, P: 42, K: 43,
      temperature: 21, humidity: 82,
      ph: 6.5, rainfall: 203
    })
  });
  return await response.json();
};
```

## 🧪 Test Your Deployed API

```bash
# Test crop recommendation
curl -X POST https://your-url/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"N":90,"P":42,"K":43,"temperature":21,"humidity":82,"ph":6.5,"rainfall":203}'

# Get usage statistics  
curl https://your-url/api/usage

# Check API health
curl https://your-url/api/health
```

## 📈 Monitor Usage

- **Dashboard**: `https://your-url/dashboard`
- **Statistics API**: `https://your-url/api/usage`
- **Log File**: `usage_logs.json` (auto-generated)

## 🎯 Key Features

🌾 **24 Crop Varieties** - Rice, Wheat, Maize, Cotton, etc.  
🎯 **94% Accuracy** - Reliable crop recommendations  
🌐 **Multilingual** - English, Hindi support  
📱 **Mobile Ready** - JSON API responses  
📊 **Usage Analytics** - Comprehensive tracking  
🚀 **Deploy Ready** - Render, Heroku, Railway  

## 🏆 Perfect for SIH 2025!

Your API is now ready for:
- ✅ Public deployment
- ✅ Mobile app integration  
- ✅ Usage monitoring
- ✅ Real-world farming applications
- ✅ SIH 2025 submission

**🎉 Start building the future of agriculture! 🌾**
