# SIH 2025 - Main App Entry Point for Deployment
# This file is specifically for Render deployment

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Use the working crop system (full 24 crops support)
from mobile_app_backend import app

# This is what Gunicorn will look for
application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
