from flask import Flask, request, jsonify, send_from_directory
from llama_api_client import LlamaAPI
import os

app = Flask(__name__, static_folder='.')

# Initialize LLAMA API client
client = LlamaAPI(os.environ.get('LLAMA_API_KEY', 'your-api-key-here'))

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Call LLAMA API
        response = client.generate(message)
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)