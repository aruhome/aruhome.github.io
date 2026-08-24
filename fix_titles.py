import os
import glob
from bs4 import BeautifulSoup

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # Get correct Title
        h1s = soup.find_all('h1')
        title = "Maintenance Task"
        for h1 in h1s:
            if h1.text.strip() and h1.text.strip() != "AruHome":
                title = h1.text.strip()
                break
                
        # Fix Breadcrumb
        breadcrumb_items = soup.find_all('li', {"aria-current": "page"})
        for item in breadcrumb_items:
            if item.text.strip() == "AruHome":
                item.string = title

        # Fix Contextual CTA
        h4s = soup.find_all('h4')
        for h4 in h4s:
            if h4.text.startswith("Track '"):
                h4.string = f"Track '{title}' with AruHome"

        # Fix JSON-LD BreadcrumbList
        for script in soup.head.find_all('script', type='application/ld+json'):
            if 'BreadcrumbList' in script.text:
                import json
                try:
                    schema = json.loads(script.text)
                    if schema.get('@type') == 'BreadcrumbList':
                        for item in schema.get('itemListElement', []):
                            if item.get('position') == 4:
                                item['name'] = title
                        script.string = f"\n{json.dumps(schema, indent=2)}\n"
                except:
                    pass

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Fixed {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    for f in glob.glob('maintenance/*.html'):
        process_file(f)
