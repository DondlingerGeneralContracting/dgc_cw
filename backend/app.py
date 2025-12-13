from flask import Flask, request, jsonify
from ddgs import DDGS
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Tor proxies
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)