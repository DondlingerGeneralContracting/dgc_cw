import os
import requests

def run_llama(prompt):
    """
    Send a prompt to the LLaMA model using the official Meta LLaMA API client.

    Args:
        prompt (str): The user prompt to send to the model

    Returns:
        str: The model's response
    """
    try:
        api_key = os.environ["LLAMA_API_KEY"]

        payload = {
            "model": "Llama-3.3-70B-Instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Provide clear, accurate, and concise responses."},
                {"role": "user", "content": prompt}
            ]
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        api_response = requests.post("https://api.llama.com/v1/chat/completions", json=payload, headers=headers)
        api_response.raise_for_status()
        data = api_response.json()
        return data["completion_message"]["content"]
    except KeyError:
        return "Error: LLAMA_API_KEY environment variable not set"
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    prompt = "Hello, can you tell me about yourself?"
    response = run_llama(prompt)
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")