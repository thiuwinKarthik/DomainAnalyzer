import re

class TechStackDetector:
    # Patterns based on the scripts found in your Salesforce HTML
    PATTERNS = {
        "Google Analytics": r"UA-\d+|G-\w+|google-analytics",
        "Google Tag Manager": r"gtm\.js|googletagmanager|GTM-[A-Z0-9]+",
        "Salesforce Cloud": r"salesforce",
        "React": r"react",
        "Optimizely": r"optimizely|cdn\.optimizely\.com",
        "Vidyard": r"vidyard",
        "OneTrust": r"onetrust",
        "Boomerang": r"boomr",
        "Akamai": r"akamai"
    }

    def detect(self, html_content: str) -> list:
        found_tech = []
        # We search the RAW html, not the cleaned text
        for tech, pattern in self.PATTERNS.items():
            if re.search(pattern, html_content, re.IGNORECASE):
                found_tech.append(tech)
        return list(set(found_tech))