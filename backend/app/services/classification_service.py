import os
import csv
import re
from typing import Dict, List, Optional, Tuple

class ClassificationService:
    """Service to map company data to sub-industry classification and SIC codes"""
    
    def __init__(self):
        # Get the backend directory (where sub_Industry_Classification.csv is located)
        current_file = os.path.abspath(__file__)
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        self.classification_file = os.path.join(backend_dir, "sub_Industry_Classification.csv")
        self.classifications: List[Dict] = []
        self._load_classifications()
    
    def _load_classifications(self):
        """Load sub-industry classification data from CSV"""
        if not os.path.exists(self.classification_file):
            print(f"[WARN] Classification file not found: {self.classification_file}")
            return
        
        try:
            with open(self.classification_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                self.classifications = list(reader)
            print(f"[INFO] Loaded {len(self.classifications)} classification entries")
        except Exception as e:
            print(f"[ERROR] Error loading classifications: {e}")
    
    def _tokenize(self, text: str) -> set:
        """Helper to convert text into a set of lowercase keywords"""
        if not text:
            return set()
        # Keep only alphanumeric chars
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        tokens = set(text.split())
        # Remove common stop words (very basic list)
        stop_words = {'and', 'or', 'the', 'a', 'an', 'of', 'in', 'for', 'services', 'service', 'limited', 'ltd', 'inc', 'co', 'company'}
        return tokens - stop_words

    def find_best_match(self, company_text: str, industry: str = "", sub_industry: str = "") -> Optional[Dict]:
        """
        Find the best matching sub-industry classification based on company text and extracted industry.
        Uses a scored matching approach.
        """
        if not self.classifications:
            return self._get_default_classification()
        
        # Prepare input tokens
        # We weigh the explicit 'sub_industry' and 'industry' args higher if provided
        input_sub_tokens = self._tokenize(sub_industry)
        input_ind_tokens = self._tokenize(industry)
        input_text_tokens = self._tokenize(company_text)
        
        # Combine all for a broad search
        all_input_tokens = input_sub_tokens | input_ind_tokens | input_text_tokens
        
        best_match = None
        best_score = 0.0
        
        # Debug: track candidates for visibility
        candidates = []

        for row in self.classifications:
            score = 0.0
            
            # Extract row fields
            row_sub = row.get('sub_industry', '')
            row_ind = row.get('Industry', '')
            row_sector = row.get('sector', '')
            row_sic_desc = row.get('sic_description', '')
            row_text = f"{row_sub} {row_ind} {row_sector} {row_sic_desc}"
            
            row_sub_tokens = self._tokenize(row_sub)
            row_ind_tokens = self._tokenize(row_ind)
            row_tokens = self._tokenize(row_text)
            
            # --- SCORING LOGIC ---
            
            # 1. Sub-Industry Match (Highest Priority)
            # If the user specifically identified a sub-industry, we want to match that closely.
            if input_sub_tokens and row_sub_tokens:
                intersection = input_sub_tokens & row_sub_tokens
                if intersection:
                    # Score based on fraction of tokens matched
                    term_match_score = len(intersection) / len(input_sub_tokens)
                    score += term_match_score * 15  # High weight

            # 2. Industry Match
            if input_ind_tokens and row_ind_tokens:
                intersection = input_ind_tokens & row_ind_tokens
                if intersection:
                    term_match_score = len(intersection) / len(input_ind_tokens)
                    score += term_match_score * 10

            # 3. Broad Keyword Match (Context)
            # Check how many input keywords appear in this row
            if all_input_tokens and row_tokens:
                intersection = all_input_tokens & row_tokens
                # Base score is number of matches
                score += len(intersection) * 1.5
            
            # 4. Exact Phrase Bonuses (Case insensitive)
            search_str = (company_text + " " + industry + " " + sub_industry).lower()
            if row_sub.lower() in search_str and len(row_sub) > 4:
                score += 20  # Massive bonus for exact sub-industry phrase match
            if row_sic_desc.lower() in search_str and len(row_sic_desc) > 4:
                score += 10

            if score > 0:
                candidates.append((score, row))

            if score > best_score:
                best_score = score
                best_match = row
        
        # Sort candidates for debug (optional, can remove in prod)
        # candidates.sort(key=lambda x: x[0], reverse=True)
        # if candidates:
        #      print(f"[DEBUG] Top match for '{sub_industry} | {industry}': {candidates[0][1]['sub_industry']} (Score: {candidates[0][0]})")

        # Threshold: 
        # Previously it was 3. Now we allow lower if we have no better options, 
        # but let's say at least some meaningful match happened (score >= 2).
        if best_match and best_score >= 2:
            return {
                'sub_industry': best_match.get('sub_industry', ''),
                'industry': best_match.get('Industry', ''),
                'sector': best_match.get('sector', ''),
                'sic_code': best_match.get('sic_code', ''),
                'sic_description': best_match.get('sic_description', '')
            }
        
        # Fallback: If we extracted a specific industry but failed to match a sub-industry,
        # try to find ANY entry in that industry to at least get the Sector right.
        if industry:
            for row in self.classifications:
                if industry.lower() in row.get('Industry', '').lower():
                    return {
                        'sub_industry': row.get('sub_industry', ''),
                        'industry': row.get('Industry', ''),
                        'sector': row.get('sector', ''),
                        'sic_code': row.get('sic_code', ''),
                        'sic_description': row.get('sic_description', '')
                    }
        
        # Default fallback
        print(f"[INFO] No good match found for '{sub_industry}' / '{industry}'. Using default.")
        return self._get_default_classification()
    
    def _get_default_classification(self) -> Dict:
        """Return default classification for unknown companies"""
        return {
            'sub_industry': 'Software Development & Services',
            'industry': 'Information Technology',
            'sector': 'Information Technology',
            'sic_code': '62012',
            'sic_description': 'Business and domestic software development'
        }
    
    def get_classification_by_sic_code(self, sic_code: str) -> Optional[Dict]:
        """Get classification details by SIC code"""
        for classification in self.classifications:
            if classification.get('sic_code') == sic_code:
                return {
                    'sub_industry': classification.get('sub_industry', ''),
                    'industry': classification.get('Industry', ''),
                    'sector': classification.get('sector', ''),
                    'sic_code': classification.get('sic_code', ''),
                    'sic_description': classification.get('sic_description', '')
                }
        return None

