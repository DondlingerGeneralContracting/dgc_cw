from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/brainstorm', methods=['POST'])
def brainstorm():
    data = request.json
    user_input = data.get('input', '')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    system_prompt = """You are a deterministic problem-collapsing engine.

Rules:
- Do not ask questions.
- If information is missing, assume and lock it.
- Produce ONE usable artifact.
- Output must follow this exact structure:

1. Problem Restated
2. Assumptions Locked
3. Constraints
4. Decomposition
5. First Usable Artifact

If you violate this, you failed."""

    payload = {
        'model': 'Llama-3.3-70B-Instruct',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input}
        ]
    }
    headers = {
        'Authorization': f'Bearer {os.environ.get("LLAMA_API_KEY", "")}',
        'Content-Type': 'application/json'
    }
    response = requests.post('https://api.together.ai/v1/chat/completions', headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        output = result['choices'][0]['message']['content']
        return jsonify({'output': output})
    else:
        return jsonify({'error': 'API request failed', 'status_code': response.status_code}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)