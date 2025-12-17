# from fastapi import APIRouter, HTTPException
# from app.services.lookup_service import LookupService

# router = APIRouter()
# service = LookupService()

# @router.get("/lookup")
# async def lookup(domain: str):
#     """
#     Endpoint: /api/lookup?domain=zoho.com
#     """
#     if not domain:
#         raise HTTPException(status_code=400, detail="Domain required")

#     result = service.fetch_company_data(domain)
    
#     if "error" in result:
#         raise HTTPException(status_code=404, detail=result["error"])
        
#     return result