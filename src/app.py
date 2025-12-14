from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('/app', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('/app', path)

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

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])
    if not messages:
        return jsonify({'error': 'No messages provided'}), 400

    try:
        # Add system prompt for chat refinement
        system_message = {
            'role': 'system',
            'content': 'You are a helpful assistant for creating Siri Shortcuts using Cherri language. Help the user refine their shortcut idea through conversation. When they are ready, suggest they say "generate" to create the code.'
        }
        full_messages = [system_message] + messages
        response = call_llama(full_messages, temperature=0.7, max_tokens=1024)
        return jsonify({'response': response, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)