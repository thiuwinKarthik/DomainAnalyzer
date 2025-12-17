# Company Intelligence System - Presentation Slides

## Slide 1: Title Slide
**Company Intelligence System**
*AI-Powered Domain Analysis Platform*

Extract, Classify, and Visualize Company Information
Using Offline AI Processing

---

## Slide 2: Problem Statement
**The Challenge:**
- Manual company research is time-consuming
- Need structured data extraction from websites
- Require industry classification and SIC codes
- Want privacy-focused, offline solution

**Our Solution:**
AI-powered platform that processes domain names offline

---

## Slide 3: Key Features
✅ **Domain Analysis** - Extract company data from HTML files
✅ **AI-Powered** - Uses Llama3 offline for intelligent extraction
✅ **Industry Classification** - Automatic SIC code mapping
✅ **Knowledge Graph** - Interactive visualization
✅ **Data Export** - JSON and CSV downloads
✅ **Modern UI** - Beautiful, responsive dashboard

---

## Slide 4: System Architecture
```
Frontend (React) 
    ↓ HTTP API
Backend (FastAPI)
    ↓
[HTML Parser] → [LLM Client] → [Classification]
    ↓              ↓              ↓
[Text Extract] → [Llama3] → [SIC Mapping]
    ↓              ↓              ↓
         [Data Storage & Cache]
```

---

## Slide 5: Workflow Overview
1. **User Input** → Domain name entered
2. **Validation** → Check domain folder exists
3. **Cache Check** → Return if already processed
4. **HTML Loading** → Load multiple HTML files
5. **Parsing** → Extract clean text and metadata
6. **AI Processing** → Llama3 extracts company data
7. **Classification** → Map to industry and SIC codes
8. **Graph Generation** → Build knowledge graph
9. **Display** → Show results in dashboard

---

## Slide 6: AI-Powered Extraction
**Llama3 Offline Processing**

- **Input**: Clean HTML text + metadata
- **Process**: LLM analyzes content
- **Output**: Structured JSON with:
  - Company name
  - Descriptions
  - Industry classification
  - Tags and keywords

**Why Offline?**
- ✅ No API keys needed
- ✅ Complete privacy
- ✅ No internet required
- ✅ Cost-effective

---

## Slide 7: Industry Classification
**Automated SIC Code Mapping**

- **Database**: 3,600+ industry classifications
- **Process**: Fuzzy matching algorithm
- **Output**: 
  - SIC Code
  - SIC Description
  - Industry, Sector, Sub-Industry

**Example:**
Spotify → "59200" (Sound recording and music publishing)

---

## Slide 8: Knowledge Graph
**Interactive Visualization**

- **Nodes**: Company, Industry, Tags, Technologies
- **Edges**: Relationships (OPERATES_IN, TAGGED_AS)
- **Features**:
  - Drag & zoom
  - Color-coded by type
  - Click to focus
  - Hover tooltips

---

## Slide 9: Technology Stack
**Backend:**
- FastAPI (Python web framework)
- BeautifulSoup4 (HTML parsing)
- Ollama (LLM runtime)
- Llama3 (Language model)

**Frontend:**
- React 18
- vis-network (Graph visualization)
- Custom CSS

---

## Slide 10: Performance
**Speed Metrics:**

- **First Request**: 30-60 seconds (LLM processing)
- **Cached Request**: < 1 second ⚡
- **HTML Parsing**: < 1 second
- **Classification**: < 1 second

**Optimization:**
Smart caching system for instant responses

---

## Slide 11: Privacy & Security
🔒 **100% Offline Processing**
- No data sent to external APIs
- Local LLM processing
- Complete data control
- No API keys required

---

## Slide 12: Demo
**Live Demonstration**

1. Enter domain: `airbnb.com`
2. Watch AI processing
3. View company details
4. Explore knowledge graph
5. Download data

---

## Slide 13: Use Cases
- **Business Intelligence**: Quick company research
- **Market Analysis**: Industry trends
- **Competitor Analysis**: Market positioning
- **Data Collection**: Bulk extraction
- **Research**: Academic & commercial

---

## Slide 14: Innovation Highlights
🚀 **What Makes This Special:**

1. Complete offline solution
2. AI-powered extraction
3. Production-ready architecture
4. Beautiful UI/UX
5. Interactive visualizations
6. Scalable design

---

## Slide 15: Technical Challenges Solved
✅ HTML parsing and cleaning
✅ LLM prompt engineering
✅ Industry classification matching
✅ Graph visualization
✅ Duplicate node handling
✅ Caching strategies
✅ Error handling

---

## Slide 16: Future Enhancements
- Batch processing
- Real-time web scraping
- Advanced graph analytics
- ML-based classification
- Multi-language support
- Company comparisons
- Historical tracking

---

## Slide 17: Thank You!
**Questions?**

**GitHub**: [Repository Link]
**Demo**: [Live Demo Link]
**Contact**: [Your Contact]

---

## Slide 18: Q&A
**Common Questions:**

Q: Why use offline LLM?
A: Privacy, cost, and no API dependencies

Q: How accurate is classification?
A: Uses 3,600+ classifications with fuzzy matching

Q: Can it process any domain?
A: Requires HTML files in offline_sites folder

Q: Performance?
A: First request 30-60s, cached < 1s

