from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "llama-api-tor"})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    api_key = os.getenv('LLAMA_API_KEY')
    if not api_key:
        return jsonify({'error': 'LLAMA_API_KEY not set'}), 500
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'Llama-3.3-70B-Instruct',
        'messages': data['messages']
    }
    proxies = {
        'https': 'socks5h://127.0.0.1:9050'
    }
    response = requests.post('https://api.llama.com/v1/chat/completions', headers=headers, json=payload, proxies=proxies)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)