import os
import csv
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
            print(f"⚠️  Classification file not found: {self.classification_file}")
            return
        
        try:
            with open(self.classification_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.classifications = list(reader)
            print(f"✅ Loaded {len(self.classifications)} classification entries")
        except Exception as e:
            print(f"❌ Error loading classifications: {e}")
    
    def find_best_match(self, company_text: str, industry: str = "", sub_industry: str = "") -> Optional[Dict]:
        """
        Find the best matching sub-industry classification based on company text and extracted industry
        
        Args:
            company_text: Combined text from company website (description, tags, etc.)
            industry: Extracted industry from LLM
            sub_industry: Extracted sub-industry from LLM
            
        Returns:
            Dictionary with classification details or None
        """
        if not self.classifications:
            return self._get_default_classification()
        
        # Normalize inputs
        search_text = (company_text + " " + industry + " " + sub_industry).lower()
        
        # Score each classification
        best_match = None
        best_score = 0
        
        for classification in self.classifications:
            score = 0
            sub_ind = classification.get('sub_industry', '').lower()
            ind = classification.get('Industry', '').lower()
            sic_desc = classification.get('sic_description', '').lower()
            
            # Check for exact matches first
            if sub_industry and sub_ind and sub_industry.lower() in sub_ind:
                score += 10
            if industry and ind and industry.lower() in ind:
                score += 8
            
            # Check for keyword matches in search text
            keywords = sub_ind.split()
            for keyword in keywords:
                if len(keyword) > 3 and keyword in search_text:
                    score += 2
            
            # Check SIC description keywords
            sic_keywords = sic_desc.split()
            for keyword in sic_keywords:
                if len(keyword) > 4 and keyword in search_text:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = classification
        
        # If we found a good match, return it
        if best_match and best_score >= 3:
            return {
                'sub_industry': best_match.get('sub_industry', ''),
                'industry': best_match.get('Industry', ''),
                'sector': best_match.get('sector', ''),
                'sic_code': best_match.get('sic_code', ''),
                'sic_description': best_match.get('sic_description', '')
            }
        
        # Fallback: try to match by industry only
        if industry:
            for classification in self.classifications:
                if industry.lower() in classification.get('Industry', '').lower():
                    return {
                        'sub_industry': classification.get('sub_industry', ''),
                        'industry': classification.get('Industry', ''),
                        'sector': classification.get('sector', ''),
                        'sic_code': classification.get('sic_code', ''),
                        'sic_description': classification.get('sic_description', '')
                    }
        
        # Default fallback
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

