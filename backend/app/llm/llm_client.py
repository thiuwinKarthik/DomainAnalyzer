import requests
import json
from app.config import LLM_MODEL, LLM_TIMEOUT

class LLMClient:
    def __init__(self):
        self.model = LLM_MODEL
        self.api_url = "http://localhost:11434/api/generate"
        self.timeout = LLM_TIMEOUT

    def query_json(self, prompt: str):
        try:
            print(f"🧠 Asking LLaMA-3 ({self.model}) with extended context...")
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Keep it factual
                    "num_ctx": 8192      # Extended context window
                }
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '{}')
            else:
                print(f"❌ Ollama API Error: {response.status_code} - {response.text}")
                return "{}"

        except requests.exceptions.ConnectionError:
            print(f"❌ Ollama Connection Error: Make sure Ollama is running (ollama serve)")
            return "{}"
        except Exception as e:
            print(f"❌ Ollama Error: {e}")
            return "{}"