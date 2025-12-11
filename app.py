from flask import Flask, request, jsonify, send_from_directory, send_file
import requests
import io
import subprocess
from kittentts import TTS

app = Flask(__name__)
tts = TTS()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    payload = {
        'model': data.get('model', 'Llama-3.3-70B-Instruct'),
        'messages': data['messages']
    }
    headers = {
        'Authorization': 'Bearer YOUR_LLAMA_API_KEY',  # Replace with your actual key or use env var
        'Content-Type': 'application/json'
    }
    response = requests.post('https://api.together.ai/v1/chat/completions', headers=headers, json=payload)

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Generate audio bytes
    audio_data = tts.generate(text, voice=voice)

    # Return as WAV
    return send_file(io.BytesIO(audio_data), mimetype='audio/wav')

@app.route('/api/command', methods=['POST'])
def run_command():
    data = request.get_json()
    cmd = data.get('command', '')

    if not cmd:
        return jsonify({'error': 'No command provided'}), 400

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return jsonify({
            'output': result.stdout,
            'error': result.stderr,
            'returncode': result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timed out'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)