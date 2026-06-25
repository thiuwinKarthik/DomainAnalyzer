import requests
import json
from app.config import LLM_BASE_URL, LLM_MODEL, LLM_TIMEOUT, LLM_NUM_CTX

class LLMClient:
    def __init__(self):
        self.model = LLM_MODEL
        self.api_url = f"{LLM_BASE_URL}/api/generate"
        self.timeout = LLM_TIMEOUT

        print(f"LLM endpoint: {self.api_url}")
        print(f"LLM model: {self.model}")

    def query_json(self, prompt: str):
        try:
            print(f"Asking local Ollama model: {self.model}")

            payload = {
                "model": self.model,
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_ctx": LLM_NUM_CTX
                }
            }

            response = requests.post(
                self.api_url,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "{}")
            else:
                print(f"Ollama API error: {response.status_code} - {response.text}")
                return "{}"

        except requests.exceptions.ConnectionError as e:
            print("Ollama connection error:", e)
            return "{}"

        except requests.exceptions.Timeout:
            print("Ollama timeout: model took too long to respond.")
            return "{}"

        except Exception as e:
            print(f"Ollama error: {e}")
            return "{}"