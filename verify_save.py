
import sys
import os
import shutil

# Add the backend directory to the path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.storage.json_store import JSONStore
from app.config import PROCESSED_DIR

def test_save_creates_dir():
    # 1. Clean up: Delete the processed directory if it exists
    if os.path.exists(PROCESSED_DIR):
        try:
            shutil.rmtree(PROCESSED_DIR)
            print("[INFO] Deleted existing processed directory.")
        except Exception as e:
            print(f"[WARN] Could not delete processed dir: {e}")

    # 2. Attempt to save
    domain = "test_netflix"
    data = {"foo": "bar"}
    
    print(f"[INFO] Attempting to save to: {os.path.join(PROCESSED_DIR, domain + '.json')}")
    try:
        JSONStore.save(domain, data)
        print("[SUCCESS] File saved successfully.")
    except Exception as e:
        print(f"[FAIL] Save failed: {e}")

    # 3. Verify file exists
    expected_path = os.path.join(PROCESSED_DIR, f"{domain}.json")
    if os.path.exists(expected_path):
        print("[CHECK] File actually exists on disk.")
    else:
        print("[CHECK] File NOT found on disk.")

if __name__ == "__main__":
    test_save_creates_dir()
