# Company Intelligence Backend

A complete backend system that processes domain names, extracts company information from offline HTML files, and uses Llama3 (offline) to generate structured JSON responses matching the Topic1_Output_Format.xlsx specification.

## Features

- **Domain Processing**: Accepts domain names and fetches HTML files from offline sites folder
- **LLM Integration**: Uses Llama3 offline via Ollama to extract company information
- **Sub-Industry Classification**: Automatically maps companies to SIC codes using sub_Industry_Classification.csv
- **Structured Output**: Returns JSON matching Topic1_Output_Format.xlsx format
- **Contact Extraction**: Extracts addresses, phone numbers, emails, and business hours
- **Industry Classification**: Maps companies to proper industry, sector, and sub-industry categories

## Setup

### Prerequisites

1. **Python 3.8+**
2. **Ollama** installed and running locally
3. **Llama3 model** downloaded

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install and start Ollama:
```bash
# Install Ollama from https://ollama.ai
# Then pull the Llama3 model:
ollama pull llama3

# Start Ollama server (if not running):
ollama serve
```

3. Ensure your project structure:
```
backend/
├── app/
│   ├── api/routes/
│   ├── core/
│   ├── llm/
│   ├── services/
│   └── storage/
├── data/
│   └── offline_sites/
│       └── [domain.com]/
│           ├── index.html
│           ├── about.html
│           ├── products.html
│           └── contact.html
├── sub_Industry_Classification.csv
└── Topic1_Output_Format.xlsx
```

## Usage

### Start the Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints

#### 1. Lookup Company by Domain
```http
GET /api/lookup?domain=example.com
```

**Response Format** (matching Topic1_Output_Format.xlsx):
```json
{
  "domain": "example.com",
  "text": "Head Office",
  "company_name": "Example Company Ltd",
  "full_address": "123 Main St, City, Postal Code, Country",
  "phone": "+44 20 1234 5678",
  "sales_phone": "+44 20 1234 5679",
  "fax": "",
  "mobile": "",
  "other_numbers": "",
  "email": "info@example.com",
  "hours_of_operation": "Monday-Friday: 9am-5pm",
  "HQ_Indicator": "",
  "sic_code": "62012",
  "sic_text": "Business and domestic software development",
  "sub_industry": "Software Development & Services",
  "industry": "Information Technology",
  "sector": "Information Technology",
  "short_description": "A leading software development company.",
  "long_description": "Example Company Ltd is a key player in the Information Technology sector...",
  "tags": "software, technology, development, services"
}
```

#### 2. Get Company Graph
```http
GET /api/graph/{domain}
```

#### 3. List All Companies
```http
GET /api/companies
```

## How It Works

1. **Domain Input**: User provides a domain name via API
2. **HTML Extraction**: System fetches HTML files from `data/offline_sites/{domain}/`
3. **HTML Parsing**: Extracts clean text, metadata, and structured data from HTML
4. **LLM Processing**: Sends parsed content to Llama3 via Ollama API
5. **Data Extraction**: LLM extracts company information including:
   - Company name, descriptions
   - Contact details (address, phone, email)
   - Business hours
   - Industry classification
6. **Classification**: Maps extracted data to sub-industry classification CSV to get:
   - SIC code
   - SIC description
   - Industry, Sector, Sub-industry
7. **Response**: Returns structured JSON matching the Excel format

## Configuration

Edit `app/config.py` to customize:
- LLM model name (default: "llama3")
- LLM timeout (default: 120 seconds)
- Data directories

## File Structure

- `app/services/classification_service.py`: Maps companies to SIC codes
- `app/services/batch_processor.py`: Main processing logic
- `app/llm/llm_client.py`: Ollama API client
- `app/core/html_parser.py`: HTML parsing and text extraction
- `app/api/routes/api.py`: API endpoints

## Notes

- The system uses **offline** Llama3 model - no API keys or internet required for LLM
- HTML files must be pre-downloaded to `data/offline_sites/{domain}/`
- Classification uses fuzzy matching against sub_Industry_Classification.csv
- Results are cached in `data/processed/{domain}.json`
