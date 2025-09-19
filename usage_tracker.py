# Usage Analytics for SIH 2025 Crop Recommendation API
import json
import os
from datetime import datetime
from collections import defaultdict

class UsageTracker:
    def __init__(self, log_file='usage_logs.json'):
        self.log_file = log_file
        self.usage_data = self.load_usage_data()
    
    def load_usage_data(self):
        """Load existing usage data from file."""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'total_requests': 0,
            'daily_stats': {},
            'endpoint_stats': defaultdict(int),
            'crop_recommendations': defaultdict(int),
            'user_locations': defaultdict(int)
        }
    
    def save_usage_data(self):
        """Save usage data to file."""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.usage_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving usage data: {e}")
    
    def log_request(self, endpoint, user_ip=None, crop_recommended=None, location=None):
        """Log a new API request."""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Update total requests
        self.usage_data['total_requests'] += 1
        
        # Update daily stats
        if today not in self.usage_data['daily_stats']:
            self.usage_data['daily_stats'][today] = 0
        self.usage_data['daily_stats'][today] += 1
        
        # Update endpoint stats
        self.usage_data['endpoint_stats'][endpoint] += 1
        
        # Update crop recommendations
        if crop_recommended:
            self.usage_data['crop_recommendations'][crop_recommended] += 1
        
        # Update user locations (if provided)
        if location:
            self.usage_data['user_locations'][location] += 1
        
        # Save data
        self.save_usage_data()
    
    def get_usage_stats(self):
        """Get comprehensive usage statistics."""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Get recent daily stats (last 7 days)
        recent_days = sorted(self.usage_data['daily_stats'].keys())[-7:]
        recent_stats = {day: self.usage_data['daily_stats'][day] for day in recent_days}
        
        # Get top crops
        top_crops = dict(sorted(self.usage_data['crop_recommendations'].items(), 
                               key=lambda x: x[1], reverse=True)[:5])
        
        # Get top locations
        top_locations = dict(sorted(self.usage_data['user_locations'].items(), 
                                   key=lambda x: x[1], reverse=True)[:5])
        
        return {
            'total_requests': self.usage_data['total_requests'],
            'today_requests': self.usage_data['daily_stats'].get(today, 0),
            'recent_daily_stats': recent_stats,
            'endpoint_usage': dict(self.usage_data['endpoint_stats']),
            'top_recommended_crops': top_crops,
            'top_user_locations': top_locations,
            'last_updated': datetime.now().isoformat()
        }

# Global usage tracker instance
usage_tracker = UsageTracker()
