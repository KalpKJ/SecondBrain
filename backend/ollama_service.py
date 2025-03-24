import requests
import json

class OllamaService:
    def __init__(self, base_url="http://localhost:11434") :
        self.base_url = base_url
        self.generate_endpoint = f"{base_url}/api/generate"
        self.embeddings_endpoint = f"{base_url}/api/embeddings"
        
    def generate_response(self, prompt, model="llama3", system_prompt=None, max_tokens=2000):
        """Generate a response from the LLM"""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "max_tokens": max_tokens
        }
        
        if system_prompt:
            payload["system"] = system_prompt
            
        response = requests.post(self.generate_endpoint, json=payload)
        
        if response.status_code == 200:
            return response.json()["response"]
        else:
            raise Exception(f"Error generating response: {response.text}")
    
    def create_embeddings(self, text, model="nomic-embed-text"):
        """Create embeddings for the given text"""
        payload = {
            "model": model,
            "prompt": text
        }
        
        response = requests.post(self.embeddings_endpoint, json=payload)
        
        if response.status_code == 200:
            return response.json()["embedding"]
        else:
            raise Exception(f"Error creating embeddings: {response.text}")

# Test the service
if __name__ == "__main__":
    ollama = OllamaService()
    
    # Test generation
    response = ollama.generate_response("Explain what a Second Brain is in one paragraph.")
    print("LLM Response:", response)
    
    # Test embeddings
    embedding = ollama.create_embeddings("This is a test sentence for embeddings.")
    print(f"Embedding created with {len(embedding)} dimensions")
