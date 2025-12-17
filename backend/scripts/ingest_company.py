import sys
import os

# Add backend to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.batch_processor import BatchProcessor

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest_company.py <domain>")
        sys.exit(1)
    
    domain = sys.argv[1]
    print(f"Starting ingestion for {domain}...")
    processor = BatchProcessor()
    result = processor.process_domain(domain)
    print("Done!")
    print(result)