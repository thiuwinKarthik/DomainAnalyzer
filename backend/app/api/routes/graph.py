# from fastapi import APIRouter, HTTPException
# from app.services.company_service import CompanyService

# router = APIRouter()

# @router.get("/graph/{domain}")
# def get_company_graph(domain: str):
#     data = CompanyService.get_company_profile(domain)
#     if not data or "graph" not in data:
#         raise HTTPException(status_code=404, detail="Graph not found")
#     return data["graph"]