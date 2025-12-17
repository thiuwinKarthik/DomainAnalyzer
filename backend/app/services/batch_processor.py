import os
import json
import re
import csv
from app.core.html_parser import HTMLParser
from app.core.tech_stack_detector import TechStackDetector
from app.llm.llm_client import LLMClient
from app.services.graph_builder import GraphBuilder
from app.services.classification_service import ClassificationService
from app.storage.json_store import JSONStore
from app.config import OFFLINE_SITES_DIR, PROCESSED_DIR

class BatchProcessor:
    # --- 1. THE TRUTH TABLE (Extended) ---
    # Maps specific keywords found in About/Products pages to accurate SIC Codes
    SIC_MAP = {
        # Finance (Zerodha, Stripe)
        "broker": ("66120", "Security and commodity contracts brokerage"),
        "trading": ("66120", "Security and commodity contracts brokerage"),
        "stock": ("66120", "Security and commodity contracts brokerage"),
        "invest": ("66120", "Security and commodity contracts brokerage"),
        "payment": ("66190", "Activities auxiliary to financial services"),
        "fintech": ("64999", "Financial service activities n.e.c."),
        "bank": ("64191", "Banks"),
        
        # Media & Entertainment (Spotify, Netflix)
        "music": ("59200", "Sound recording and music publishing activities"),
        "audio": ("59200", "Sound recording and music publishing activities"),
        "song": ("59200", "Sound recording and music publishing activities"),
        "video": ("59111", "Motion picture production activities"),
        "movie": ("59111", "Motion picture production activities"),
        "stream": ("59111", "Motion picture production activities"),
        "entertainment": ("59111", "Motion picture production activities"),

        # Travel (Airbnb, Uber)
        "hotel": ("55100", "Hotels and similar accommodation"),
        "stay": ("55100", "Hotels and similar accommodation"),
        "booking": ("55100", "Hotels and similar accommodation"),
        "travel": ("79110", "Travel agency activities"),
        "taxi": ("49320", "Taxi operation"),
        "ride": ("49320", "Taxi operation"),

        # Retail (Amazon, Shopify)
        "shop": ("47910", "Retail sale via mail order houses or via Internet"),
        "retail": ("47910", "Retail sale via mail order houses or via Internet"),
        "commerce": ("47910", "Retail sale via mail order houses or via Internet"),
        "fashion": ("47710", "Retail sale of clothing in specialised stores"),

        # Tech (Salesforce, Zoho - The fallback)
        "crm": ("62012", "Business and domestic software development"),
        "saas": ("62012", "Business and domestic software development"),
        "software": ("62012", "Business and domestic software development"),
        "cloud": ("63110", "Data processing, hosting and related activities"),
        "consult": ("62020", "Information technology consultancy activities")
    }

    def __init__(self):
        self.parser = HTMLParser()
        self.llm = LLMClient()
        self.graph_builder = GraphBuilder()
        self.tech_detector = TechStackDetector()
        self.classifier = ClassificationService()
        
        self.csv_file = os.path.join(PROCESSED_DIR, "companies.csv")
        self._init_csv()

    def _init_csv(self):
        if not os.path.exists(PROCESSED_DIR): 
            os.makedirs(PROCESSED_DIR)
        # CSV headers will be written on first append if file doesn't exist

    def process_domain(self, domain: str):
        # 1. Clean Domain Name (Fix googleusercontent/proxy issues)
        clean_domain = domain
        if "googleusercontent" in domain and "spotify" in domain:
            clean_domain = "spotify.com"
        elif "/" in domain:
            clean_domain = domain.split("/")[-1]

        print(f"⚙️  Processing {clean_domain}...")

        # 2. LOAD ALL FILES (Index + About + Products + Careers)
        domain_dir = os.path.join(OFFLINE_SITES_DIR, domain) # Use original folder name
        combined_html = ""
        is_blocked = True
        
        if os.path.exists(domain_dir):
            # Priority order: Products tells us WHAT they do, About tells us WHO they are
            for fname in ["products.html", "about.html", "index.html", "careers.html"]:
                fpath = os.path.join(domain_dir, fname)
                if os.path.exists(fpath):
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            content = f.read()
                            if len(content) > 500 and "Access Denied" not in content:
                                # Add header so AI knows source
                                combined_html += f"\n\n=== SOURCE: {fname.upper()} ===\n" 
                                combined_html += content[:15000] # Limit size per file
                                is_blocked = False
                    except: pass

        # 3. Extract Context
        # We parse the giant combined string
        clean_text = self.parser.parse(combined_html) if not is_blocked else ""
        detected_tech = self.tech_detector.detect(combined_html) if not is_blocked else []
        soup_title = clean_domain.split('.')[0].capitalize()

        # 4. Generate Profile (Pass the RICH context)
        result = self._generate_profile(clean_domain, context=clean_text, title=soup_title, use_memory=is_blocked, existing_tech=detected_tech)
        profile = result["profile"]

        # 5. CLASSIFICATION USING SUB-INDUSTRY CLASSIFICATION CSV
        # Use the classification service to map to proper SIC codes
        self._apply_classification(profile, clean_text)

        # 6. Final Build & Save
        final_graph = self._build_graph(profile)
        final_result = {"profile": profile, "graph": final_graph}
        
        # Save using clean domain ID
        JSONStore.save(clean_domain, final_result)
        self._append_to_csv(profile)
        
        print(f"   ✅ Success: {profile['company_name']} | {profile['industry']} | SIC: {profile['sic_code']}")
        return final_result

    def _generate_profile(self, domain, context="", title="", use_memory=False, existing_tech=None):
        source = "Analyze the provided website sections (Products, About, Home, Contact)." if not use_memory else f"Use internal knowledge about '{domain}'."
        content = f"WEBSITE CONTENT:\n{context[:25000]}" if not use_memory else ""
        
        prompt = f"""
        {source}
        Extract complete company information for "{domain}" (Name: "{title}").
        
        CRITICAL INSTRUCTIONS:
        1. Identify the specific industry and sub-industry from the content
        2. Extract 5-8 relevant tags/keywords
        3. NO "Unknown" or empty values - use reasonable defaults if not found
        4. Focus on company description, industry classification, and business information
        
        JSON SCHEMA:
        {{
            "company_name": "Official Company Name",
            "short_description": "1 sentence summary of what the company does",
            "long_description": "3-4 sentences describing the company and its main products/services",
            "industry": "Main industry category (e.g., 'Information Technology', 'Financial Services')",
            "sub_industry": "Specific sub-industry (e.g., 'Software Development & Services', 'Payment Processing')",
            "sector": "Broad sector category (e.g., 'Information Technology', 'Financial Services')",
            "products_services": ["product1", "product2", "service1"],
            "tags": "tag1, tag2, tag3, tag4, tag5"
        }}
        {content}
        """
        try:
            raw = self.llm.query_json(prompt)
            profile = self._parse_json(raw)
            
            profile["domain"] = domain
            if not profile.get("company_name") or profile["company_name"] == "Official Name":
                profile["company_name"] = title or domain.split('.')[0].capitalize()
            
            if existing_tech: profile["tech_stack"] = list(set(existing_tech))
            else: profile["tech_stack"] = []

            return {"profile": profile, "graph": {}}
        except Exception as e:
            print(f"❌ Error generating profile: {e}")
            return {"profile": {}, "graph": {}}

    def _apply_classification(self, profile, raw_text):
        """
        Apply sub-industry classification using the classification service.
        Maps extracted data to proper SIC codes from sub_Industry_Classification.csv
        """
        # Combine all text for classification matching
        search_text = (
            str(profile.get("long_description", "")) + " " +
            str(profile.get("short_description", "")) + " " +
            str(profile.get("tags", "")) + " " +
            str(profile.get("industry", "")) + " " +
            str(profile.get("sub_industry", "")) + " " +
            raw_text[:3000]
        )
        
        # Get classification from service
        classification = self.classifier.find_best_match(
            company_text=search_text,
            industry=profile.get("industry", ""),
            sub_industry=profile.get("sub_industry", "")
        )
        
        # Apply classification results
        if classification:
            profile["sic_code"] = classification.get("sic_code", "")
            profile["sic_text"] = classification.get("sic_description", "")
            # Update industry/sector/sub_industry if they were missing or generic
            if not profile.get("industry") or profile.get("industry") in ["Unknown", "Technology", "Tech"]:
                profile["industry"] = classification.get("industry", profile.get("industry", "Information Technology"))
            if not profile.get("sector"):
                profile["sector"] = classification.get("sector", "Information Technology")
            if not profile.get("sub_industry") or profile.get("sub_industry") in ["Unknown", "Digital Services"]:
                profile["sub_industry"] = classification.get("sub_industry", profile.get("sub_industry", "Software Development & Services"))
        
        # Ensure all required fields have values
        name = profile.get("company_name", "Unknown Company")
        ind = profile.get("industry", "Information Technology")
        
        if not profile.get("short_description") or profile["short_description"] in ["Unknown", ""]:
            profile["short_description"] = f"A leading {ind} company."
            
        if not profile.get("long_description") or len(str(profile.get("long_description"))) < 10:
            profile["long_description"] = f"{name} is a key player in the {ind} sector, offering specialized services."
        
        if not profile.get("sector"):
            profile["sector"] = "Information Technology"
        
        if not profile.get("sub_industry"):
            profile["sub_industry"] = "Software Development & Services"
        
        # Ensure tags is a string
        if not profile.get("tags"):
            profile["tags"] = f"{ind.lower()}, technology, business, services"
        elif isinstance(profile["tags"], list):
            profile["tags"] = ", ".join(profile["tags"])
        
        # Ensure contact fields exist (even if empty)
        for field in ["text", "full_address", "phone", "sales_phone", "fax", "mobile", "other_numbers", "email", "hours_of_operation"]:
            if field not in profile:
                profile[field] = ""

    def _build_graph(self, profile):
        domain = profile.get("domain")
        name = profile.get("company_name")
        ind = profile.get("industry", "Business")
        
        # Use sets to track unique node IDs to prevent duplicates
        seen_ids = set()
        nodes = []
        edges = []
        
        # Add company node
        if domain:
            company_id = f"company_{domain}"
            if company_id not in seen_ids:
                nodes.append({"id": company_id, "label": name or domain, "group": "Company"})
                seen_ids.add(company_id)
        
        # Add industry node with unique ID
        if ind:
            industry_id = f"industry_{ind}"
            if industry_id not in seen_ids:
                nodes.append({"id": industry_id, "label": ind, "group": "Industry"})
                seen_ids.add(industry_id)
            
            # Add edge from company to industry
            if domain:
                edges.append({"source": f"company_{domain}", "target": industry_id, "label": "OPERATES_IN"})
        
        # Add tag nodes with unique IDs
        tags = str(profile.get("tags", "")).split(',')
        for t in tags[:5]:
            clean_t = t.strip()
            if clean_t:
                tag_id = f"tag_{clean_t}"
                if tag_id not in seen_ids:
                    nodes.append({"id": tag_id, "label": clean_t, "group": "Tag"})
                    seen_ids.add(tag_id)
                
                # Add edge from company to tag
                if domain:
                    edges.append({"source": f"company_{domain}", "target": tag_id, "label": "TAGGED_AS"})
                
        # Add technology nodes with unique IDs
        for tech in profile.get("tech_stack", [])[:8]:
            if tech:
                tech_id = f"tech_{tech}"
                if tech_id not in seen_ids:
                    nodes.append({"id": tech_id, "label": tech, "group": "Technology"})
                    seen_ids.add(tech_id)
                
                # Add edge from company to tech
                if domain:
                    edges.append({"source": f"company_{domain}", "target": tech_id, "label": "USES_TECH"})
            
        return {"nodes": nodes, "edges": edges}

    def _append_to_csv(self, data):
        try:
            # Check if file exists and has headers
            file_exists = os.path.exists(self.csv_file)
            
            with open(self.csv_file, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header if file is new
                if not file_exists:
                    writer.writerow([
                        "domain", "text", "company_name", "full_address", "phone", 
                        "sales_phone", "fax", "mobile", "other_numbers", "email",
                        "hours_of_operation", "sic_code", "sic_text", "sub_industry",
                        "industry", "sector", "short_description", "long_description", "tags"
                    ])
                
                # Write data row matching Excel format
                writer.writerow([
                    data.get("domain", ""),
                    data.get("text", ""),
                    data.get("company_name", ""),
                    data.get("full_address", "").replace("\n", " "),
                    data.get("phone", ""),
                    data.get("sales_phone", ""),
                    data.get("fax", ""),
                    data.get("mobile", ""),
                    data.get("other_numbers", ""),
                    data.get("email", ""),
                    data.get("hours_of_operation", ""),
                    data.get("sic_code", ""),
                    data.get("sic_text", ""),
                    data.get("sub_industry", ""),
                    data.get("industry", ""),
                    data.get("sector", ""),
                    data.get("short_description", "").replace("\n", " "),
                    data.get("long_description", "").replace("\n", " "),
                    data.get("tags", "")
                ])
        except Exception as e:
            print(f"⚠️  Error appending to CSV: {e}")

    def _parse_json(self, raw):
        if not raw: return {}
        try:
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                return json.loads(match.group(0).replace(",\n}", "\n}"))
        except: pass
        return {}