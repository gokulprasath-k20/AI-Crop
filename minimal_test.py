# Minimal Flask Test
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "SIH 2025 API Working!", "status": "success"})

@app.route('/test')
def test():
    return jsonify({"test": "successful", "crops": 24})

if __name__ == '__main__':
    print("🧪 Starting minimal test server...")
    app.run(host='127.0.0.1', port=5001, debug=False)
