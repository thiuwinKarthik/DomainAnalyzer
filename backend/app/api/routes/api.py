from fastapi import APIRouter, HTTPException
from app.services.lookup_service import LookupService
from app.services.company_service import CompanyService

router = APIRouter()
lookup_service = LookupService()

@router.get("/lookup")
async def lookup(domain: str):
    """
    Lookup company information by domain name.
    Returns data in format matching Topic1_Output_Format.xlsx
    """
    if not domain: 
        raise HTTPException(status_code=400, detail="Domain required")
    
    result = lookup_service.fetch_company_data(domain)
    if "error" in result: 
        raise HTTPException(status_code=404, detail=result["error"])
    
    # Transform to match Excel output format
    profile = result.get("profile", {})
    
    # Format response without contact information
    response = {
        "domain": profile.get("domain", domain),
        "company_name": profile.get("company_name", ""),
        "short_description": profile.get("short_description", ""),
        "long_description": profile.get("long_description", ""),
        "sic_code": profile.get("sic_code", ""),
        "sic_text": profile.get("sic_text", ""),
        "sub_industry": profile.get("sub_industry", ""),
        "industry": profile.get("industry", ""),
        "sector": profile.get("sector", ""),
        "tags": profile.get("tags", "")
    }
    
    return response

@router.get("/graph/{domain}")
async def get_graph(domain: str):
    data = CompanyService.get_company_profile(domain)
    if not data or "graph" not in data: raise HTTPException(status_code=404, detail="Graph not found")
    return data["graph"]

@router.get("/companies")
async def list_companies():
    return CompanyService.get_all_companies()