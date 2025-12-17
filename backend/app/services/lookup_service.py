import os
import json
from app.config import PROCESSED_DIR
from app.services.batch_processor import BatchProcessor

class LookupService:
    def __init__(self):
        self.processor = BatchProcessor()

    def fetch_company_data(self, domain: str):
        # 1. Clean domain input
        domain = domain.lower().replace("https://", "").replace("www.", "").strip("/")
        
        # 2. Check if domain folder exists in offline_sites
        from app.config import OFFLINE_SITES_DIR
        domain_dir = os.path.join(OFFLINE_SITES_DIR, domain)
        if not os.path.exists(domain_dir):
            return {"error": f"Domain '{domain}' not found in offline sites folder. Please ensure HTML files exist for this domain."}
        
        # 3. Check Local Cache (Processed JSON)
        json_path = os.path.join(PROCESSED_DIR, f"{domain}.json")
        if os.path.exists(json_path):
            print(f"⚡ Serving {domain} from Cache")
            with open(json_path, "r") as f:
                return json.load(f)

        # 4. If not in Cache, Process the Downloaded HTML
        print(f"🔨 Parsing offline data for {domain}...")
        return self.processor.process_domain(domain)