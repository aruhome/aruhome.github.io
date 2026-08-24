import os
import glob
import json
from bs4 import BeautifulSoup

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Get Title and Category
        h1 = soup.find('h1')
        title = h1.text.strip() if h1 else "Maintenance Task"
        
        # Find category tag
        category = "General"
        hero_tags = soup.find_all('span', class_='hero-tag')
        if hero_tags:
            # Usually the first one is the category
            category = hero_tags[0].text.strip()
            
        # 2. Replace "Back to Library" with Breadcrumbs
        back_link = soup.find('a', href="../maintenance-library.html")
        if back_link and "Back to Library" in back_link.text:
            breadcrumb_html = f"""
            <nav aria-label="breadcrumb">
                <ol style="list-style: none; padding: 0; margin: 0; display: flex; align-items: center; gap: 8px; font-size: 0.95rem; color: var(--text-muted); flex-wrap: wrap;">
                    <li><a href="../index.html" style="color: var(--text-secondary); text-decoration: none;">AruHome</a></li>
                    <li><svg fill="none" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14"><polyline points="9 18 15 12 9 6"></polyline></svg></li>
                    <li><a href="../maintenance-library.html" style="color: var(--text-secondary); text-decoration: none;">Maintenance Library</a></li>
                    <li><svg fill="none" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14"><polyline points="9 18 15 12 9 6"></polyline></svg></li>
                    <li style="color: var(--text-secondary);">{category}</li>
                    <li><svg fill="none" height="14" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="14"><polyline points="9 18 15 12 9 6"></polyline></svg></li>
                    <li aria-current="page" style="color: var(--text-primary); font-weight: 500;">{title}</li>
                </ol>
            </nav>
            """
            new_nav = BeautifulSoup(breadcrumb_html, 'html.parser')
            back_link.replace_with(new_nav)

        # 3. Contextual CTA
        h4s = soup.find_all('h4')
        for h4 in h4s:
            if "Unlock the Full Guide" in h4.text:
                h4.string = f"Track '{title}' with AruHome"
                p = h4.find_next_sibling('p')
                if p:
                    p.string = f"Add this task to your digital maintenance schedule. Get automatic reminders, log your completion dates, and store receipts."
                a = h4.parent.find('a', class_='btn-pill')
                if a:
                    a.string = "Add to AruHome"

        # 4. JSON-LD BreadcrumbList
        exists = False
        for script in soup.head.find_all('script', type='application/ld+json'):
            if 'BreadcrumbList' in script.text:
                exists = True
                break
                
        if not exists:
            schema = {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "AruHome",
                        "item": "https://aruhome.github.io/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Maintenance Library",
                        "item": "https://aruhome.github.io/maintenance-library.html"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": category
                    },
                    {
                        "@type": "ListItem",
                        "position": 4,
                        "name": title
                    }
                ]
            }
            script_tag = soup.new_tag('script', type='application/ld+json')
            script_tag.string = f"\n{json.dumps(schema, indent=2)}\n"
            soup.head.append(script_tag)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    for f in glob.glob('maintenance/*.html'):
        process_file(f)
