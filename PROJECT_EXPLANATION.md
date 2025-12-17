# Company Intelligence System - Hackathon Presentation

## 🎯 Project Overview

**Company Intelligence System** is an AI-powered platform that extracts and visualizes comprehensive company information from domain names using offline HTML files and local LLM processing.

### Key Features
- 🔍 **Domain Analysis**: Extract company data from offline HTML files
- 🤖 **AI-Powered Extraction**: Uses Llama3 (offline) for intelligent data extraction
- 📊 **Industry Classification**: Automatic SIC code mapping using sub-industry classification
- 🕸️ **Knowledge Graph**: Interactive visualization of company relationships
- 💾 **Data Export**: Download company details as JSON or CSV
- 🎨 **Modern UI**: Beautiful, responsive dashboard with custom CSS

---

## 🏗️ System Architecture

```
┌─────────────────┐
│   Frontend      │  React.js Application
│   (React)       │  - Domain Input
│                 │  - Company Details Display
│                 │  - Graph Visualization
└────────┬────────┘
         │ HTTP REST API
         ▼
┌─────────────────┐
│   Backend       │  FastAPI Server
│   (Python)      │  - API Endpoints
│                 │  - Business Logic
└────────┬────────┘
         │
         ├─────────────────┬─────────────────┐
         ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ HTML Parser  │  │ LLM Client   │  │ Classification│
│              │  │ (Ollama)     │  │ Service      │
│ Extracts     │  │ Llama3       │  │ SIC Mapping  │
│ clean text   │  │ Processing   │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
         │                 │                 │
         └─────────────────┴─────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Data Storage   │
                  │  - JSON Cache   │
                  │  - CSV Export   │
                  └─────────────────┘
```

---

## 🔄 Complete Workflow

### Step 1: User Input
**Frontend (`DomainInput.js`)**
- User enters a domain name (e.g., `airbnb.com`)
- Input is validated and sent to backend via API

```javascript
// User types: "airbnb.com"
// Frontend sends: GET /api/lookup?domain=airbnb.com
```

---

### Step 2: Domain Validation
**Backend (`lookup_service.py`)**
- Cleans domain input (removes `www.`, `https://`, etc.)
- Checks if domain folder exists in `data/offline_sites/`
- Returns error if domain not found

```python
# Clean domain: "airbnb.com" → "airbnb.com"
# Check: data/offline_sites/airbnb.com/ exists?
# If not → Return 404 error
```

---

### Step 3: Cache Check
**Backend (`lookup_service.py`)**
- Checks if processed data exists in `data/processed/{domain}.json`
- If cached, returns immediately (fast response)
- If not cached, proceeds to processing

```python
# Check: data/processed/airbnb.com.json exists?
# If yes → Load and return (⚡ Instant)
# If no → Process domain
```

---

### Step 4: HTML File Loading
**Backend (`batch_processor.py`)**
- Loads HTML files from `data/offline_sites/{domain}/`
- Priority order: `products.html` → `about.html` → `index.html` → `careers.html`
- Combines content from multiple files (up to 15KB per file)

```python
# Load files:
# - products.html (most important - tells WHAT they do)
# - about.html (tells WHO they are)
# - index.html (homepage)
# - careers.html (additional context)
# Combine into single text blob
```

---

### Step 5: HTML Parsing & Text Extraction
**Backend (`html_parser.py`)**
- Uses BeautifulSoup to parse HTML
- Extracts:
  - **Structured Metadata**: JSON-LD schemas (goldmine of data!)
  - **SEO Data**: Title, meta descriptions
  - **Clean Text**: Removes scripts, styles, navigation, footers
- Returns clean, structured text for LLM processing

```python
# Parse HTML:
# 1. Extract JSON-LD (structured company data)
# 2. Extract title and meta description
# 3. Clean body text (remove scripts, styles, nav, footer)
# 4. Combine: Body text + Metadata + SEO info
# Result: Clean, structured text ready for LLM
```

---

### Step 6: Technology Stack Detection
**Backend (`tech_stack_detector.py`)**
- Scans HTML for technology indicators
- Detects frameworks, libraries, tools mentioned
- Adds to company profile

```python
# Detect technologies from HTML:
# - JavaScript frameworks (React, Vue, Angular)
# - Analytics tools (Google Analytics, etc.)
# - CDN providers
# Result: List of technologies used
```

---

### Step 7: AI-Powered Data Extraction
**Backend (`llm_client.py` + `prompts.py`)**
- Sends parsed HTML content to **Llama3** via Ollama API
- LLM extracts structured company information:
  - Company name
  - Short & long descriptions
  - Industry, sub-industry, sector
  - Products/services
  - Tags/keywords

```python
# LLM Prompt Structure:
"""
Extract company information from website content:
- Company name
- Descriptions (short & long)
- Industry classification
- Tags/keywords
"""

# Ollama API Call:
POST http://localhost:11434/api/generate
{
  "model": "llama3",
  "prompt": "...",
  "format": "json"
}

# LLM Response: Structured JSON with company data
```

**Why Llama3 Offline?**
- ✅ No API keys needed
- ✅ Complete privacy (data stays local)
- ✅ No internet required for LLM processing
- ✅ Cost-effective (no per-request charges)

---

### Step 8: Industry Classification & SIC Code Mapping
**Backend (`classification_service.py`)**
- Loads `sub_Industry_Classification.csv` (3,600+ classifications)
- Matches extracted company data to sub-industry
- Assigns:
  - **SIC Code**: Standard Industrial Classification code
  - **SIC Description**: Official description
  - **Industry**: Main industry category
  - **Sector**: Broad sector
  - **Sub-Industry**: Specific classification

```python
# Classification Process:
# 1. Load CSV with 3,600+ industry classifications
# 2. Search for best match using:
#    - Company description
#    - Industry keywords
#    - Tags
# 3. Score matches and select best fit
# 4. Assign SIC code and classification
# Result: Accurate industry classification
```

**Example:**
- Company: Spotify
- Extracted: "music streaming", "audio", "entertainment"
- Matched: Sub-Industry = "Music Streaming Services"
- SIC Code: "59200" (Sound recording and music publishing activities)

---

### Step 9: Knowledge Graph Generation
**Backend (`batch_processor.py` → `_build_graph()`)**
- Creates graph structure with:
  - **Nodes**: Company, Industry, Tags, Technologies
  - **Edges**: Relationships (OPERATES_IN, TAGGED_AS, USES_TECH)
- Ensures unique node IDs (prevents duplicates)

```python
# Graph Structure:
nodes = [
  {"id": "company_airbnb.com", "label": "Airbnb", "group": "Company"},
  {"id": "industry_Travel", "label": "Travel", "group": "Industry"},
  {"id": "tag_hospitality", "label": "hospitality", "group": "Tag"},
  ...
]

edges = [
  {"source": "company_airbnb.com", "target": "industry_Travel", "label": "OPERATES_IN"},
  {"source": "company_airbnb.com", "target": "tag_hospitality", "label": "TAGGED_AS"},
  ...
]
```

---

### Step 10: Data Storage
**Backend (`json_store.py`)**
- Saves processed data to `data/processed/{domain}.json`
- Includes:
  - Company profile (all extracted data)
  - Knowledge graph (nodes & edges)
- Enables fast retrieval for future requests

```python
# Save to JSON:
{
  "profile": {
    "domain": "airbnb.com",
    "company_name": "Airbnb",
    "industry": "Travel",
    "sic_code": "79110",
    ...
  },
  "graph": {
    "nodes": [...],
    "edges": [...]
  }
}
```

---

### Step 11: API Response
**Backend (`api.py`)**
- Formats data according to output specification
- Returns JSON response to frontend

```json
{
  "domain": "airbnb.com",
  "company_name": "Airbnb",
  "short_description": "...",
  "long_description": "...",
  "industry": "Travel",
  "sub_industry": "Travel & Leisure",
  "sector": "Hospitality",
  "sic_code": "79110",
  "sic_text": "Travel agency activities",
  "tags": "travel, hospitality, booking, accommodation"
}
```

---

### Step 12: Frontend Display
**Frontend (`CompanyDetails.js`)**
- Receives JSON response
- Displays data in organized sections:
  1. **Company Overview** 🏢
     - Company name, domain, descriptions
  2. **Industry Classification** 📊
     - Industry, sub-industry, sector, SIC codes
  3. **Tags & Keywords** 🏷️
     - All extracted tags

**Design Features:**
- Vertical layout with generous spacing
- Gradient backgrounds and shadows
- Hover effects and animations
- Responsive design

---

### Step 13: Graph Visualization
**Frontend (`GraphVisualization.js`)**
- Fetches graph data: `GET /api/graph/{domain}`
- Uses **vis-network** library for interactive visualization
- Features:
  - Drag & zoom nodes
  - Color-coded by type (Company, Industry, Tag, Technology)
  - Click to focus/zoom
  - Hover tooltips

**Graph Elements:**
- 🟦 **Company** (Purple boxes) - Central node
- 🟪 **Industry** (Dark purple circles) - Main industry
- 🟩 **Tags** (Pink circles) - Keywords
- 🟨 **Technology** (Blue circles) - Tech stack

---

### Step 14: Data Export
**Frontend (`CompanyDetails.js`)**
- **Download Summary (JSON)**: Complete company data in JSON format
- **Download Details (CSV)**: Formatted CSV file for spreadsheet use

```javascript
// JSON Export:
{
  "domain": "airbnb.com",
  "company_name": "Airbnb",
  "industry": "Travel",
  ...
}

// CSV Export:
Field,Value
Domain,airbnb.com
Company Name,Airbnb
Industry,Travel
...
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **BeautifulSoup4**: HTML parsing
- **Ollama**: Local LLM runtime
- **Llama3**: Large language model (offline)
- **Python CSV**: Data processing

### Frontend
- **React 18**: UI framework
- **vis-network**: Graph visualization
- **Custom CSS**: Modern, responsive design

### Data Storage
- **JSON**: Processed company data
- **CSV**: Classification data, exports
- **HTML**: Offline website files

---

## 📊 Data Flow Diagram

```
User Input (Domain)
    │
    ▼
[Domain Validation]
    │
    ▼
[Cache Check] ──Yes──→ [Return Cached Data]
    │ No
    ▼
[Load HTML Files]
    │
    ▼
[Parse HTML] ──→ [Extract Text & Metadata]
    │
    ▼
[Detect Tech Stack]
    │
    ▼
[Send to Llama3] ──→ [AI Extraction]
    │
    ▼
[Industry Classification] ──→ [SIC Code Mapping]
    │
    ▼
[Build Knowledge Graph]
    │
    ▼
[Save to Cache]
    │
    ▼
[Return JSON Response]
    │
    ▼
[Frontend Display] ──→ [Graph Visualization]
    │
    ▼
[User Views Results]
```

---

## 🎯 Key Innovations

### 1. **Offline AI Processing**
- Uses local Llama3 model via Ollama
- No cloud API dependencies
- Complete data privacy

### 2. **Intelligent HTML Parsing**
- Extracts structured JSON-LD metadata
- Cleans and structures content for LLM
- Combines multiple HTML files for context

### 3. **Automated Industry Classification**
- Maps to 3,600+ industry classifications
- Assigns accurate SIC codes
- Uses fuzzy matching for best fit

### 4. **Knowledge Graph Visualization**
- Interactive network graph
- Shows company relationships
- Color-coded by entity type

### 5. **Smart Caching**
- Processes once, serves instantly
- Reduces LLM processing time
- Improves user experience

---

## 📈 Performance Metrics

- **First Request**: 30-60 seconds (LLM processing)
- **Cached Request**: < 1 second (instant)
- **HTML Parsing**: < 1 second
- **LLM Processing**: 20-40 seconds
- **Classification**: < 1 second
- **Graph Generation**: < 1 second

---

## 🔒 Privacy & Security

- ✅ **100% Offline Processing**: No data sent to external APIs
- ✅ **Local LLM**: Llama3 runs entirely on your machine
- ✅ **No API Keys**: No external service dependencies
- ✅ **Data Control**: All data stays in your system

---

## 🚀 Use Cases

1. **Business Intelligence**: Quick company research
2. **Market Analysis**: Industry classification and trends
3. **Competitor Analysis**: Understand market positioning
4. **Data Collection**: Bulk company data extraction
5. **Research**: Academic and commercial research

---

## 📝 Example Workflow

**Input:** `airbnb.com`

**Processing:**
1. Loads HTML files from `data/offline_sites/airbnb.com/`
2. Parses and extracts content
3. Sends to Llama3: "Extract company information..."
4. LLM returns: Company name, descriptions, industry
5. Classification service matches to "Travel & Leisure"
6. Assigns SIC code: "79110" (Travel agency activities)
7. Builds graph: Company → Industry → Tags → Technologies

**Output:**
- Company details displayed in dashboard
- Interactive knowledge graph
- Downloadable JSON/CSV files

---

## 🎓 Learning Outcomes

This project demonstrates:
- **AI Integration**: Using LLMs for data extraction
- **Data Processing**: HTML parsing and text extraction
- **Classification Systems**: Industry code mapping
- **Graph Theory**: Knowledge graph construction
- **Full-Stack Development**: React + FastAPI
- **Data Visualization**: Interactive graphs
- **API Design**: RESTful endpoints
- **Caching Strategies**: Performance optimization

---

## 🔮 Future Enhancements

- [ ] Batch processing for multiple domains
- [ ] Real-time web scraping integration
- [ ] Advanced graph analytics
- [ ] Machine learning for better classification
- [ ] Multi-language support
- [ ] Company comparison features
- [ ] Historical data tracking

---

## 📞 Technical Details

### API Endpoints
- `GET /api/lookup?domain={domain}` - Get company data
- `GET /api/graph/{domain}` - Get knowledge graph
- `GET /api/companies` - List all processed companies

### File Structure
```
project_2/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # HTML parsing, tech detection
│   │   ├── llm/          # LLM client and prompts
│   │   ├── services/     # Business logic
│   │   └── storage/      # Data storage
│   └── data/
│       ├── offline_sites/ # HTML files
│       └── processed/     # Cached JSON files
├── frontend/
│   └── src/
│       ├── components/    # React components
│       └── App.js        # Main app
└── sub_Industry_Classification.csv
```

---

## 🏆 Hackathon Highlights

**What Makes This Special:**
1. **Complete Offline Solution**: No external API dependencies
2. **AI-Powered**: Uses state-of-the-art LLM for extraction
3. **Production Ready**: Full-stack application with caching
4. **Beautiful UI**: Modern, responsive design
5. **Data Visualization**: Interactive knowledge graphs
6. **Scalable Architecture**: Clean code structure

**Technical Challenges Solved:**
- ✅ HTML parsing and cleaning
- ✅ LLM prompt engineering
- ✅ Industry classification matching
- ✅ Graph visualization
- ✅ Duplicate node handling
- ✅ Caching strategies
- ✅ Error handling

---

## 🎬 Demo Flow

1. **Start Backend**: `uvicorn app.main:app --reload`
2. **Start Frontend**: `npm start`
3. **Enter Domain**: Type `airbnb.com` in input field
4. **Watch Processing**: See loading spinner
5. **View Results**: Company details appear
6. **Explore Graph**: Interactive visualization
7. **Download Data**: Export as JSON or CSV

---

**Built with ❤️ for Hackathon 2024**

