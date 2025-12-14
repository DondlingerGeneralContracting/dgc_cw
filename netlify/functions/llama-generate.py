import json
import os
import requests

LLAMA_API_URL = os.environ.get("LLAMA_API_URL", "https://api.llama.com/v1/chat/completions")
LLAMA_MODEL = os.environ.get("LLAMA_MODEL", "Llama-3.3-70B-Instruct")
LLAMA_API_KEY = os.environ.get("LLAMA_API_KEY", "")

def handler(event, context):
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': ''
        }

    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }

    try:
        data = json.loads(event['body'])
        user_input = data.get('prompt', '')
        if not user_input:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No prompt provided'})
            }

        headers = {
            'Authorization': f'Bearer {LLAMA_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': LLAMA_MODEL,
            'messages': [
                {'role': 'system', 'content': 'You are a Cherri code generator. Cherri is a Siri Shortcuts programming language that compiles to valid runnable Shortcuts.\n\nCHERRI SYNTAX RULES:\n- Variables: @varname = "value" or @varname = 123\n- Constants: const name = value (for magic variable outputs)\n- Type declarations: @varname: text, @varname: number\n- String interpolation: "{variable}"\n- Functions: function name(type arg) { ... output("result") }\n- Includes: #include \'actions/scripting\' (for standard actions)\n- Defines: #define glyph iconName, #define color colorName\n- Actions: show("text"), alert("message", "title"), output("value")\n- Conditionals: if condition { } else { }\n- Loops: repeat 5 { }, repeatEach item in list { }\n- Comments: // single line, /* multi-line */\n- Raw actions: rawAction("identifier", { "key": "value" })\n- VCards: makeVCard("Title", "Subtitle")\n\nAVAILABLE GLYPHS: smileyFace, heart, star, bell, bookmark, calendar, camera, clock, cloud, gear, house, location, mail, music, phone, search, share, trash, user, etc.\n\nAVAILABLE COLORS: red, orange, yellow, green, blue, purple, pink, gray, teal, navy, etc.\n\nCOMMON INCLUDES:\n- #include \'actions/scripting\' (for scripting actions)\n- #include \'actions/network\' (for network actions like isOnline())\n- #include \'actions/documents\' (for file operations)\n\nGenerate clean, working Cherri code based on the user\'s request.'},
                {'role': 'user', 'content': f"Generate Cherri code for: {user_input}"}
            ],
            'temperature': 0.6,
            'max_completion_tokens': 2048,
            'response_format': {
                "type": "json_schema",
                "json_schema": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"}
                    },
                    "required": ["code"]
                }
            }
        }

        resp = requests.post(LLAMA_API_URL, headers=headers, json=payload)
        if resp.status_code != 200:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f'Llama API error: {resp.text}'})
            }

        result = resp.json()
        content = result['completion_message']['content']
        parsed = json.loads(content)
        code = parsed['code']

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({'code': code, 'success': True})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }