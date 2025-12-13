import json
from ddgs import DDGS

def handler(event, context):
    query = event.get('queryStringParameters', {}).get('q', '')
    if not query:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Query parameter q is required'})
        }

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=10))

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps(results)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Simulate Netlify event
event = {
    'queryStringParameters': {
        'q': 'python programming'
    }
}

context = {}

# Call the handler
response = handler(event, context)

print("Status Code:", response['statusCode'])
print("Response Body:")
print(json.dumps(json.loads(response['body']), indent=2))