# from fastapi import APIRouter, HTTPException
# from app.services.company_service import CompanyService

# router = APIRouter()

# @router.get("/company/{domain}")
# def get_profile(domain: str):
#     data = CompanyService.get_company_profile(domain)
#     if not data:
#         raise HTTPException(status_code=404, detail="Company not found")
#     return data