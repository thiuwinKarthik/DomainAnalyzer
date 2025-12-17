from bs4 import BeautifulSoup
import json
import re

class HTMLParser:
    @staticmethod
    def parse(html_content: str) -> str:
        if not html_content: return ""

        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 1. Extract JSON-LD (The Goldmine)
        goldmine = []
        for script in soup.find_all('script', type='application/ld+json'):
            if script.string:
                try:
                    data = json.loads(script.string)
                    # Dump the whole JSON string so LLM can read the structure directly
                    goldmine.append(f"STRUCTURED_METADATA: {json.dumps(data)}") 
                except: pass
        
        goldmine_text = "\n".join(goldmine)

        # 2. Extract SEO
        title = soup.title.string.strip() if soup.title else "Unknown"
        meta = soup.find("meta", attrs={"name": "description"})
        desc = meta.get("content", "").strip() if meta else ""

        # 3. Clean Body
        for element in soup(['script', 'style', 'nav', 'footer', 'iframe', 'svg', 'noscript', 'img']):
            element.decompose()
        
        body_text = soup.get_text(separator=' ', strip=True)
        body_text = re.sub(r'\s+', ' ', body_text).strip()

        # 4. FINAL ASSEMBLY - PUT GOLDMINE LAST
        # LLaMA reads top-to-bottom. Putting the best data last helps it "remember".
        return (
            f"WEBSITE CONTENT SAMPLE:\n{body_text[:8000]}\n"
            f"------------------------------------------------\n"
            f"OFFICIAL PAGE TITLE: {title}\n"
            f"OFFICIAL META DESCRIPTION: {desc}\n"
            f"{goldmine_text}\n"  # <--- Goldmine is now at the end
        )