from flask import Flask, request, jsonify
from ddgs import DDGS
from flask_cors import CORS
from llama_api_client import LlamaAPI
import os

app = Flask(__name__)
CORS(app)

# Tor proxies
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# LLaMA API client
llama_client = LlamaAPI(os.environ.get('LLAMA_API_KEY'))

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

@app.route('/llama-proxy', methods=['POST'])
def llama_proxy():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Forward to LLaMA API with Tor proxy
        response = llama_client.create_chat_completion(**data, proxies=proxies)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)