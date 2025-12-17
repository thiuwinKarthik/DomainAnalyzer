# Company Intelligence Frontend

A React-based frontend application for visualizing company intelligence data extracted from domain names.

## Features

- 🔍 **Domain Analysis**: Enter any domain name to extract company information
- 📊 **Detailed Information Display**: View all company attributes in organized sections
- 🕸️ **Interactive Graph Visualization**: Visualize company relationships using network graphs
- 💾 **Download Functionality**: Download company details as JSON or CSV
- 🎨 **Modern UI**: Beautiful, responsive design with custom CSS

## Installation

1. Install dependencies:
```bash
npm install
```

## Running the Application

1. Make sure the backend is running on `http://localhost:8000`

2. Start the frontend:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Usage

1. Enter a domain name in the input field (e.g., `airbnb.com`, `spotify.com`)
2. Click "Analyze" to fetch company data
3. View the detailed company information
4. Explore the interactive knowledge graph
5. Download company details using the download buttons

## Components

- **DomainInput**: Input form for domain entry
- **CompanyDetails**: Displays all company attributes in organized sections
- **GraphVisualization**: Interactive network graph using vis-network
- **LoadingSpinner**: Loading indicator during API calls

## API Integration

The frontend connects to the backend API at `http://localhost:8000`:
- `GET /api/lookup?domain={domain}` - Fetch company data
- `GET /api/graph/{domain}` - Fetch graph data

## Technologies

- React 18
- vis-network for graph visualization
- Axios for API calls
- Custom CSS for styling


