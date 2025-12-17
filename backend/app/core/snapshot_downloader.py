import os
import requests
from app.config import OFFLINE_SITES_DIR

class SnapshotDownloader:
    def download_site(self, domain: str):
        """Downloads the homepage of the domain for offline processing."""
        save_dir = os.path.join(OFFLINE_SITES_DIR, domain)
        os.makedirs(save_dir, exist_ok=True)
        
        url = f"https://{domain}" if not domain.startswith("http") else domain
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            with open(os.path.join(save_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(response.text)
            return True
        except Exception as e:
            print(f"Failed to download {domain}: {e}")
            return False