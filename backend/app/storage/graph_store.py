import json
import os
from app.config import PROCESSED_DIR

class GraphStore:
    # Graphs are stored inside the main JSON for simplicity in this architecture
    # But this class provides a specific accessor
    @staticmethod
    def get_graph(domain: str):
        path = os.path.join(PROCESSED_DIR, f"{domain}.json")
        if os.path.exists(path):
            data = json.load(open(path))
            return data.get("graph", {})
        return {}