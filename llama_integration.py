import os
from llama_api_client import LlamaAPI

def run_llama(prompt):
    """
    Send a prompt to the LLaMA model using the official Meta LLaMA API client.

    Args:
        prompt (str): The user prompt to send to the model

    Returns:
        str: The model's response
    """
    try:
        # Initialize the LLaMA API client with the API key from environment
        api_key = os.environ["LLAMA_API_KEY"]
        llama = LlamaAPI(api_key)

        # Prepare the request payload following Meta's best practices
        payload = {
            "model": "meta-llama/Llama-3.3-8B-Instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 512,
            "temperature": 0.7
        }

        # Make the API call
        response = llama.run(payload)

        # Extract and return the response content
        if response and "choices" in response:
            return response["choices"][0]["message"]["content"]
        else:
            return "Error: Unexpected response format"

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