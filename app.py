from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='.')

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

        api_key = os.environ.get('LLAMA_API_KEY')
        if not api_key:
            return jsonify({'error': 'LLAMA_API_KEY not set'}), 500

        payload = {
            "model": "Llama-3.3-70B-Instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Provide clear, accurate, and concise responses."},
                {"role": "user", "content": message}
            ]
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        api_response = requests.post("https://api.llama.com/v1/chat/completions", json=payload, headers=headers)
        api_response.raise_for_status()
        data = api_response.json()
        response = data["completion_message"]["content"]

        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)