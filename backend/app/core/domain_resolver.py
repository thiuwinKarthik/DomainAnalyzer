import os
from app.config import OFFLINE_SITES_DIR

class DomainResolver:
    @staticmethod
    def get_snapshot_path(domain: str) -> str:
        """Returns the path to index.html for a domain"""
        return os.path.join(OFFLINE_SITES_DIR, domain, "index.html")