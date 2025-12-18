import json
import os
from app.config import PROCESSED_DIR

class JSONStore:
    @staticmethod
    def save(domain: str, data: dict):
        path = os.path.join(PROCESSED_DIR, f"{domain}.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load(domain: str):
        path = os.path.join(PROCESSED_DIR, f"{domain}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None