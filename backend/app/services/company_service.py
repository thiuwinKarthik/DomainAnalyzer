import os
from app.storage.json_store import JSONStore
from app.config import PROCESSED_DIR

class CompanyService:
    @staticmethod
    def get_company_profile(domain: str):
        return JSONStore.load(domain)

    @staticmethod
    def get_all_companies():
        if not os.path.exists(PROCESSED_DIR): return []
        return sorted([f.replace(".json", "") for f in os.listdir(PROCESSED_DIR) if f.endswith(".json")])