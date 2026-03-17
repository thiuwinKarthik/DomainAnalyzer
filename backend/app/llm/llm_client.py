import requests
import json
from app.config import LLM_MODEL, LLM_TIMEOUT

class LLMClient:
    def __init__(self):
        self.model = LLM_MODEL
        self.api_url = "http://127.0.0.1:11434/api/generate"
        self.timeout = LLM_TIMEOUT

        print("Sending request to:", self.api_url)

    def query_json(self, prompt: str):
        try:
            print(f"🧠 Asking Phi-3 ({self.model})...")

            payload = {
                "model": self.model,
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_ctx": 4096
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
                print(f"❌ Ollama API Error: {response.status_code} - {response.text}")
                return "{}"

        except requests.exceptions.ConnectionError as e:
            print("❌ Connection Error:", e)
            return "{}"

        except requests.exceptions.Timeout:
            print("❌ Ollama Timeout: Model took too long to respond.")
            return "{}"

        except Exception as e:
            print(f"❌ Ollama Error: {e}")
            return "{}"