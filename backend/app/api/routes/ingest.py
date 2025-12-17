# from fastapi import APIRouter, BackgroundTasks
# from app.services.batch_processor import BatchProcessor

# router = APIRouter()
# processor = BatchProcessor()

# @router.post("/ingest/{domain}")
# async def ingest_domain(domain: str, background_tasks: BackgroundTasks):
#     """Starts the extraction process in the background."""
#     background_tasks.add_task(processor.process_domain, domain)
#     return {"status": "accepted", "message": f"Processing {domain} in background"}