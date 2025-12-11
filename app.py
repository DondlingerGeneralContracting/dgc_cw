from flask import Flask, request, jsonify, send_from_directory, send_file
import requests
import io
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
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY',  # Replace with your actual API key
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

@app.route('/api/tts', methods=['POST'])
def generate_tts():
    data = request.get_json()
    text = data.get('text', '')
    voice = data.get('voice', 'expr-voice-2-f')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Generate audio bytes
    audio_data = tts.generate(text, voice=voice)
    
    # Return as WAV
    return send_file(io.BytesIO(audio_data), mimetype='audio/wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)