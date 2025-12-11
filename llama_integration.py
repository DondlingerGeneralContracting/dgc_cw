import os
from llama_api_client import LlamaAPIClient as LlamaAPI

def run_llama(prompt):
    """
    Send a prompt to the LLaMA model using the official Meta LLaMA API client.

    Args:
        prompt (str): The user prompt to send to the model

    Returns:
        str: The model's response
    """
    try:
        # Initialize the LLaMA API client (reads API key from LLAMA_API_KEY env var)
        llama = LlamaAPI()

        # Make the API call using OpenAI-compatible interface with best practices
        response = llama.chat.completions.create(
            model="meta-llama/Llama-3.3-8B-Instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Provide clear, accurate, and concise responses."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=512,
            temperature=0.7
        )

        # Extract and return the response content
        return response.choices[0].message.content
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