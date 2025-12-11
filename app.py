from flask import Flask, request, jsonify, send_from_directory
from llamaapi import LlamaAPIClient as LlamaAPI
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

        response = client.run({
            "model": "llama3-70b",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Provide clear, accurate, and concise responses."},
                {"role": "user", "content": message}
            ]
        })
        if isinstance(response, list):
            response = response[0]
        response = response["choices"][0]["message"]["content"]

        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)