from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api

app = FastAPI(title="Company Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api", tags=["Core"])

@app.get("/")
def health_check():
    return {"status": "System Ready", "endpoints": ["/api/lookup", "/api/graph", "/api/companies"]}