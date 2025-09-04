import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
PROXY_SHARED_SECRET = os.environ.get('PROXY_SHARED_SECRET')
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

@app.route('/generate', methods=['POST'])
def handle_generation():
    # 1. Check for the secret password from your app
    auth_secret = request.headers.get('X-Proxy-Secret')
    if not auth_secret or auth_secret != PROXY_SHARED_SECRET:
        return jsonify({"error": "Unauthorized"}), 403

    # 2. Get the data your app sent
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    # 3. Call the real Gemini API using the global URL
    try:
        response = requests.post(GEMINI_API_URL, json=data, timeout=30)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        # This will log any errors to your Vercel logs for debugging
        print(f"ERROR calling Google API: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():

    return "Proxy server is running."
