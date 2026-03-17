#!/usr/bin/env python3
"""
fetch_snapshot.py - ROBUST MULTI-PAGE VERSION
Downloads Homepage + About + Contact + Careers pages.
Uses Dual-Engine (Stealth + Standard) to bypass blocks and handle network errors.
"""

import argparse
import logging
import time
import requests as std_requests  # Fallback library
from pathlib import Path
from typing import List, Optional
from curl_cffi import requests as stealth_requests  # Primary library

# ----------------------------------------------------------------------
# Path Configuration (FIXED ✅)
# ----------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent      # backend/scripts
PROJECT_ROOT = BASE_DIR.parent                  # backend
DATA_DIR = PROJECT_ROOT / "data"                # backend/data

# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()],
)

# ----------------------------------------------------------------------
# Target Pages
# ----------------------------------------------------------------------
TARGET_PAGES = {
    "index.html": [""],
    "about.html": ["about", "about-us", "company", "our-story", "corporate"],
    "contact.html": ["contact", "contact-us", "support"],
    "careers.html": ["careers", "jobs", "join-us"],
    "products.html": ["products", "services", "solutions", "features"]
}

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def read_domains(path: Path) -> List[str]:
    if not path.exists():
        logging.error(f"❌ Domain file not found: {path}")
        return []
    with path.open("r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def fetch_with_stealth(url: str, timeout: int) -> Optional[str]:
    """Engine 1: Chrome Impersonation"""
    try:
        resp = stealth_requests.get(
            url,
            impersonate="chrome110",
            timeout=timeout,
            allow_redirects=True,
            verify=False
        )
        if resp.status_code == 200 and len(resp.text) > 500:
            return resp.text
    except Exception:
        pass
    return None

def fetch_with_standard(url: str, timeout: int) -> Optional[str]:
    """Engine 2: Standard Requests"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        resp = std_requests.get(
            url,
            headers=headers,
            timeout=timeout,
            verify=False,
            allow_redirects=True
        )
        if resp.status_code == 200 and len(resp.text) > 500:
            return resp.text
    except Exception:
        pass
    return None

def find_active_base_url(domain: str, timeout: int) -> Optional[str]:
    clean = domain.replace("https://", "").replace("http://", "").replace("www.", "").strip("/")

    candidates = [
        f"https://{clean}",
        f"https://www.{clean}",
        f"http://{clean}"
    ]

    for url in candidates:
        logging.info(f"   Testing: {url}")
        if fetch_with_stealth(url, timeout) or fetch_with_standard(url, timeout):
            return url.rstrip("/")

    return None

# ----------------------------------------------------------------------
# Main Logic
# ----------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domains", type=Path, default=DATA_DIR / "domains.txt")
    parser.add_argument("--delay", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=15)
    args = parser.parse_args()

    domains = read_domains(args.domains)
    if not domains:
        return

    base_dir = DATA_DIR / "offline_sites"
    base_dir.mkdir(parents=True, exist_ok=True)

    logging.info(f"🚀 Scanning {len(domains)} domains...")

    for i, domain in enumerate(domains, start=1):
        logging.info(f"[{i}/{len(domains)}] {domain}")

        domain_dir = base_dir / domain
        domain_dir.mkdir(parents=True, exist_ok=True)

        base_url = find_active_base_url(domain, args.timeout)

        if not base_url:
            logging.error(f"   ❌ Could not connect to {domain}")
            continue

        logging.info(f"   🔗 Connected: {base_url}")

        for filename, paths in TARGET_PAGES.items():
            file_path = domain_dir / filename

            if file_path.exists() and file_path.stat().st_size > 500:
                continue

            success = False

            for path_suffix in paths:
                target_url = f"{base_url}/{path_suffix}" if path_suffix else base_url

                html = fetch_with_stealth(target_url, args.timeout)
                if not html:
                    html = fetch_with_standard(target_url, args.timeout)

                if html:
                    file_path.write_text(html, encoding="utf-8")
                    logging.info(f"      ✓ {filename} (/{path_suffix})")
                    success = True
                    break

            if not success and filename == "index.html":
                logging.warning(f"      ⚠️ Homepage failed")

        time.sleep(args.delay)

    logging.info("🏁 Done.")

# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()