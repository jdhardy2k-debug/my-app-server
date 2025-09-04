import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
PROXY_SHARED_SECRET = os.environ.get('PROXY_SHARED_SECRET')
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

@app.route('/generate', methods=['POST'])
def handle_generation():
    # --- START OF NEW DIAGNOSTIC CODE ---
    # This block will print what the server sees to the Vercel logs
    print("--- DIAGNOSTIC CHECK INITIATED ---")
    gemini_key_check = os.environ.get('GEMINI_API_KEY')
    proxy_secret_check = os.environ.get('PROXY_SHARED_SECRET')

    print(f"Is GEMINI_API_KEY present? {str(gemini_key_check is not None)}")
    if gemini_key_check:
        # For security, we only log the first 4 characters
        print(f"GEMINI_API_KEY starts with: {gemini_key_check[:4]}...")

    print(f"Is PROXY_SHARED_SECRET present? {str(proxy_secret_check is not None)}")
    if proxy_secret_check:
        print(f"PROXY_SHARED_SECRET starts with: {proxy_secret_check[:4]}...")
    print("--- END OF DIAGNOSTIC CHECK ---")
    # --- END OF NEW DIAGNOSTIC CODE ---

    # The original function logic continues below
    auth_secret = request.headers.get('X-Proxy-Secret')
    if not auth_secret or auth_secret != PROXY_SHARED_SECRET:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    try:
        # We construct the URL here again to ensure it's correct
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key_check}"
        response = requests.post(api_url, json=data)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        # We add more detail to the error logging
        print(f"ERROR calling Google API: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "Proxy server is running."