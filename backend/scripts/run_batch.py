import sys
import os
import time

# Add backend to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.batch_processor import BatchProcessor
from app.config import DATA_DIR

def run():
    # 1. Setup
    input_file = os.path.join(DATA_DIR, "domains.txt")
    if not os.path.exists(input_file):
        print(f"❌ Error: Create {input_file} first with your list of domains!")
        return

    # 2. Read Domains
    with open(input_file, "r") as f:
        domains = [line.strip() for line in f if line.strip()]

    processor = BatchProcessor()
    total = len(domains)
    print(f"🚀 Starting Autonomous Run for {total} companies...\n")

    # 3. Processing Loop
    success = 0
    for index, domain in enumerate(domains):
        print(f"[{index+1}/{total}] Processing: {domain}")
        
        try:
            # The Magic: Download -> Extract -> Save
            result = processor.process_domain(domain)
            
            if "error" in result:
                print(f"   ⚠️  Issue: {result['error']}")
            else:
                print(f"   ✅ Success! Extracted: {result.get('company_name', 'Unknown')}")
                success += 1
                
        except Exception as e:
            print(f"   ❌ Critical Failure: {e}")
        
        # Tiny pause to be polite to servers (optional)
        time.sleep(1)

    # 4. Final Report
    print(f"\n🏁 JOB COMPLETE")
    print(f"Successful: {success}")
    print(f"Failed:     {total - success}")
    print(f"Data saved to: backend/data/processed/")

if __name__ == "__main__":
    run()