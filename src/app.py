from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Llama API per llama-chat-completions.yaml spec
LLAMA_API_URL = os.environ.get("LLAMA_API_URL", "https://api.llama.com/v1/chat/completions")
LLAMA_MODEL = os.environ.get("LLAMA_MODEL", "Llama-3.3-70B-Instruct")

CHERRI_SYSTEM_PROMPT = """You are a Cherri code generator. Cherri is a Siri Shortcuts programming language that compiles to valid runnable Shortcuts.

CHERRI SYNTAX RULES:
- Variables: @varname = "value" or @varname = 123
- Constants: const name = value (for magic variable outputs)
- Type declarations: @varname: text, @varname: number
- String interpolation: "{variable}"
- Functions: function name(type arg) { ... output("result") }
- Includes: #include 'actions/scripting' (for standard actions)
- Defines: #define glyph iconName, #define color colorName
- Actions: show("text"), alert("message", "title"), output("value")
- Conditionals: if condition { } else { }
- Loops: repeat 5 { }, repeatEach item in list { }
- Comments: // single line, /* multi-line */
- Raw actions: rawAction("identifier", { "key": "value" })
- VCards: makeVCard("Title", "Subtitle")

AVAILABLE GLYPHS: smileyFace, heart, star, bell, bookmark, calendar, camera, clock, cloud, gear, house, location, mail, music, phone, search, share, trash, user, etc.

AVAILABLE COLORS: red, orange, yellow, green, blue, purple, pink, gray, teal, navy, etc.

COMMON INCLUDES:
- #include 'actions/scripting' (for scripting actions)
- #include 'actions/network' (for network actions like isOnline())
- #include 'actions/documents' (for file operations)

OUTPUT RULES:
1. Output ONLY valid Cherri code
2. Always start with #define glyph and #define color
3. Include necessary #include statements
4. Use proper variable syntax with @
5. Add helpful comments
6. Make the code functional and complete

Generate clean, working Cherri code based on the user's request."""

def call_llama(messages, temperature=0.6, max_tokens=2048):
    """Call Llama API per llama-chat-completions.yaml spec"""
    payload = {
        'model': LLAMA_MODEL,
        'messages': messages,
        'temperature': temperature,
        'max_completion_tokens': max_tokens,
        'top_p': 0.9
    }
    headers = {
        'Authorization': f'Bearer {os.environ.get("LLAMA_API_KEY", "")}',
        'Content-Type': 'application/json'
    }
    response = requests.post(LLAMA_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        # Per yaml spec: completion_message.content
        return result.get('completion_message', {}).get('content', '')
    else:
        raise Exception(f"Llama API error {response.status_code}: {response.text}")

@app.route('/api/generate', methods=['POST'])
def generate_cherri():
    data = request.json
    user_input = data.get('prompt', '')
    if not user_input:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        messages = [
            {'role': 'system', 'content': CHERRI_SYSTEM_PROMPT},
            {'role': 'user', 'content': f"Generate Cherri code for: {user_input}"}
        ]
        code = call_llama(messages, temperature=0.6)
        # Clean up code blocks if present
        if '```cherri' in code:
            code = code.split('```cherri')[1].split('```')[0].strip()
        elif '```' in code:
            code = code.split('```')[1].split('```')[0].strip()
        return jsonify({'code': code, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/explain', methods=['POST'])
def explain_cherri():
    data = request.json
    code = data.get('code', '')
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    try:
        messages = [
            {'role': 'system', 'content': CHERRI_SYSTEM_PROMPT},
            {'role': 'user', 'content': f"Explain this Cherri code step by step: {code}"}
        ]
        explanation = call_llama(messages, temperature=0.3)
        return jsonify({'explanation': explanation, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

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
    app.run(host='0.0.0.0', port=5002, debug=True)