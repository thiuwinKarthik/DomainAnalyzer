# API Endpoints for Testing

Base URL: `http://localhost:8000`

## 1. Health Check
**GET** `/`

Check if the backend is running.

**Example:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "status": "System Ready",
  "endpoints": ["/api/lookup", "/api/graph", "/api/companies"]
}
```

---

## 2. Lookup Company by Domain ⭐ MAIN ENDPOINT
**GET** `/api/lookup?domain={domain}`

Extract company information from offline HTML files and return structured JSON matching Topic1_Output_Format.xlsx.

**Parameters:**
- `domain` (required): Domain name (e.g., "airbnb.com", "spotify.com")

**Examples:**

```bash
# Test with airbnb.com
curl "http://localhost:8000/api/lookup?domain=airbnb.com"

# Test with spotify.com
curl "http://localhost:8000/api/lookup?domain=spotify.com"

# Test with zerodha.com
curl "http://localhost:8000/api/lookup?domain=zerodha.com"

# Test with stripe.com
curl "http://localhost:8000/api/lookup?domain=stripe.com"

# Test with netflix.com
curl "http://localhost:8000/api/lookup?domain=netflix.com"
```

**Response Format:**
```json
{
  "domain": "airbnb.com",
  "text": "Head Office",
  "company_name": "Airbnb",
  "full_address": "888 Brannan Street, San Francisco, CA 94103",
  "phone": "+1 415-800-5959",
  "sales_phone": "",
  "fax": "",
  "mobile": "",
  "other_numbers": "",
  "email": "support@airbnb.com",
  "hours_of_operation": "Monday-Friday: 9am-5pm",
  "HQ_Indicator": "",
  "sic_code": "79110",
  "sic_text": "Travel agency activities",
  "sub_industry": "Travel & Leisure",
  "industry": "Travel",
  "sector": "Hospitality",
  "short_description": "A leading travel platform.",
  "long_description": "Airbnb is a key player in the Travel sector...",
  "tags": "travel, hospitality, booking, accommodation"
}
```

**Browser Test:**
```
http://localhost:8000/api/lookup?domain=airbnb.com
```

---

## 3. Get Company Graph
**GET** `/api/graph/{domain}`

Get the knowledge graph for a company (nodes and edges).

**Example:**
```bash
curl http://localhost:8000/api/graph/airbnb.com
```

**Response:**
```json
{
  "nodes": [
    {"id": "airbnb.com", "label": "Airbnb", "group": "Company"},
    {"id": "Travel", "label": "Travel", "group": "Industry"},
    {"id": "travel", "label": "travel", "group": "Tag"}
  ],
  "edges": [
    {"source": "airbnb.com", "target": "Travel", "label": "OPERATES_IN"},
    {"source": "airbnb.com", "target": "travel", "label": "TAGGED_AS"}
  ]
}
```

---

## 4. List All Processed Companies
**GET** `/api/companies`

Get a list of all domains that have been processed.

**Example:**
```bash
curl http://localhost:8000/api/companies
```

**Response:**
```json
[
  "airbnb.com",
  "amazon.com",
  "netflix.com",
  "spotify.com",
  "stripe.com",
  "zerodha.com"
]
```

---

## Testing with PowerShell (Windows)

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/"

# Lookup company
Invoke-RestMethod -Uri "http://localhost:8000/api/lookup?domain=airbnb.com"

# Get graph
Invoke-RestMethod -Uri "http://localhost:8000/api/graph/airbnb.com"

# List companies
Invoke-RestMethod -Uri "http://localhost:8000/api/companies"
```

---

## Testing with Python

```python
import requests

base_url = "http://localhost:8000"

# Health check
response = requests.get(f"{base_url}/")
print(response.json())

# Lookup company
response = requests.get(f"{base_url}/api/lookup", params={"domain": "airbnb.com"})
print(response.json())

# Get graph
response = requests.get(f"{base_url}/api/graph/airbnb.com")
print(response.json())

# List companies
response = requests.get(f"{base_url}/api/companies")
print(response.json())
```

---

## Available Test Domains

Based on your `data/offline_sites/` folder, you can test with:
- `airbnb.com`
- `amazon.com`
- `netflix.com`
- `spotify.com`
- `stripe.com`
- `zerodha.com`
- `zoho.com`
- `tcs.com`
- `wipro.com`
- `infosys.com`

---

## Error Responses

**400 Bad Request:**
```json
{
  "detail": "Domain required"
}
```

**404 Not Found:**
```json
{
  "detail": "Domain not found in offline sites"
}
```

---

## Notes

- Make sure **Ollama is running** (`ollama serve`) before testing
- Make sure **Llama3 model is installed** (`ollama pull llama3`)
- The first request for a domain may take 30-60 seconds (LLM processing)
- Subsequent requests for the same domain are served from cache (instant)


