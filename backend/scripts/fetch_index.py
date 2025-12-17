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
from curl_cffi import requests as stealth_requests # Primary library

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()],
)

# Map filename -> List of possible URL paths to check
TARGET_PAGES = {
    "index.html": [""],
    "about.html": ["about", "about-us", "company", "our-story", "corporate"],
    "contact.html": ["contact", "contact-us", "support"],
    "careers.html": ["careers", "jobs", "join-us"],
    "products.html": ["products", "services", "solutions", "features"]
}

def read_domains(path: Path) -> List[str]:
    if not path.exists():
        logging.error(f"❌ Domain file not found: {path}")
        return []
    with path.open("r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def fetch_with_stealth(url: str, timeout: int) -> Optional[str]:
    """Engine 1: Chrome Impersonation (Best for Cloudflare/Security)"""
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
    except Exception as e:
        # logging.warning(f"   [Stealth] {url} failed: {e}")
        pass
    return None

def fetch_with_standard(url: str, timeout: int) -> Optional[str]:
    """Engine 2: Standard Python Requests (Best for DNS stability)"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
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
    except Exception as e:
        # logging.warning(f"   [Standard] {url} failed: {e}")
        pass
    return None

def find_active_base_url(domain: str, timeout: int) -> Optional[str]:
    """
    Determines the working base URL (root vs www, https vs http).
    Returns the successful base URL string.
    """
    # Sanitize input
    clean = domain.replace("https://", "").replace("http://", "").replace("www.", "").strip("/")
    
    # Priority list
    candidates = [
        f"https://{clean}",
        f"https://www.{clean}",
        f"http://{clean}"
    ]
    
    for url in candidates:
        logging.info(f"   Testing connection: {url} ...")
        # Try both engines to establish connection
        if fetch_with_stealth(url, timeout) or fetch_with_standard(url, timeout):
            return url.rstrip("/")
            
    return None

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--domains", type=Path, default=Path("data/domains.txt"))
    parser.add_argument("--delay", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=15)
    args = parser.parse_args()

    domains = read_domains(args.domains)
    if not domains: return

    base_dir = Path("data/offline_sites")
    logging.info(f"🚀 Scanning {len(domains)} domains for multi-page content...")

    for i, domain in enumerate(domains, start=1):
        logging.info(f"[{i}/{len(domains)}] Target: {domain}")
        
        domain_dir = base_dir / domain
        domain_dir.mkdir(parents=True, exist_ok=True)

        # 1. Find the working Base URL
        base_url = find_active_base_url(domain, args.timeout)
        
        if not base_url:
            logging.error(f"   ❌ Could not connect to {domain}. Skipping.")
            continue
            
        logging.info(f"   🔗 Connected to: {base_url}")

        # 2. Iterate through Target Pages
        for filename, paths in TARGET_PAGES.items():
            file_path = domain_dir / filename
            
            # Smart Skip: Don't redownload if we already have it
            if file_path.exists() and file_path.stat().st_size > 500:
                continue

            success = False
            # Try paths in order (e.g. try /about, then /about-us)
            for path_suffix in paths:
                target_url = f"{base_url}/{path_suffix}" if path_suffix else base_url
                
                # Attempt Download (Dual Engine)
                html = fetch_with_stealth(target_url, args.timeout)
                if not html:
                    html = fetch_with_standard(target_url, args.timeout)
                
                if html:
                    file_path.write_text(html, encoding="utf-8")
                    logging.info(f"      ✓ Saved: {filename} (found at /{path_suffix})")
                    success = True
                    break # Stop looking for this file type once found
            
            if not success and filename == "index.html":
                logging.warning(f"      ⚠️ Failed to download Homepage for {domain}")

        time.sleep(args.delay)

    logging.info("🏁 Snapshot Complete.")

if __name__ == "__main__":
    main()