from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from flask_cors import CORS
from ddgs import DDGS

app = Flask(__name__)
CORS(app, origins=["*"])  # Allow all origins for now

# Tor proxies
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "llama-api-tor"})

@app.route('/ddgs-search', methods=['POST'])
def ddgs_search():
    data = request.get_json()
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    try:
        # Use DDGS with Tor proxy
        with DDGS(proxies=proxies) as ddgs:
            results = list(ddgs.text(query, max_results=10))
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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