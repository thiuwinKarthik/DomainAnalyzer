# This file is redundant if logic is in client + service, 
# but we keep it for structure adherence.
from app.llm.llm_client import LLMClient

class Extractor(LLMClient):
    pass