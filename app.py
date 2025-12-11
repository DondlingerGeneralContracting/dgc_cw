from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

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

if __name__ == '__main__':
    app.run(debug=True)