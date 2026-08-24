import os
import glob
import json
import re
from bs4 import BeautifulSoup

BASE_URL = "https://aruhome.github.io/"
SITE_NAME = "AruHome"
DEFAULT_IMAGE = f"{BASE_URL}images/aruhome-preview.jpg" # Assuming this exists or will be standard

def clean_head(soup):
    # Remove existing SEO tags to avoid duplicates
    for tag in soup.head.find_all(['title', 'meta']):
        if tag.name == 'title':
            tag.decompose()
        elif tag.name == 'meta':
            # keep charset, viewport, theme-color
            if tag.get('charset') or tag.get('name') == 'viewport' or tag.get('name') == 'theme-color':
                continue
            tag.decompose()
    
    # Remove existing JSON-LD
    for script in soup.head.find_all('script', type='application/ld+json'):
        script.decompose()

def extract_content(soup, filepath):
    title = ""
    description = ""
    
    h1 = soup.find('h1')
    if h1 and h1.text.strip() and h1.text.strip() != "AruHome": # Ignore the logo text
        title = h1.text.strip()
    
    if not title:
        # Fallback to existing title or filename
        existing_title = soup.find('title')
        if existing_title:
            title = existing_title.text.strip()
        else:
            title = os.path.basename(filepath).replace('.html', '').replace('-', ' ').title()
            
    if "AruHome" not in title:
        title = f"{title} | AruHome"

    # Extract description from first meaningful paragraph
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        text = p.text.strip()
        if len(text) > 40 and not text.startswith('©'): # avoid footer
            description = text
            break
            
    if not description:
        description = "AruHome: The complete home management app. Track assets, automate maintenance, and organize financial records securely."
        
    # truncate description
    if len(description) > 160:
        description = description[:157] + "..."
        
    return title, description

def generate_seo_tags(soup, title, description, url, image_url=DEFAULT_IMAGE):
    tags = f"""
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{url}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{url}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta property="og:image" content="{image_url}">
    
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{image_url}">
    """
    return BeautifulSoup(tags, 'html.parser')

def generate_schema(soup, filepath, url, title, description):
    filename = os.path.basename(filepath)
    dirname = os.path.basename(os.path.dirname(filepath))
    
    schemas = []
    
    if filename == 'index.html' and dirname != 'blog' and dirname != 'maintenance':
        # Homepage Schemas
        schemas.append({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "AruHome",
            "applicationCategory": "ProductivityApplication",
            "operatingSystem": "Android",
            "description": description,
            "url": url,
            "image": DEFAULT_IMAGE,
            "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" }
        })
        schemas.append({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "AruHome",
            "url": url,
            "logo": f"{BASE_URL}Icon.png"
        })
        schemas.append({
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "AruHome",
            "url": url
        })
    elif filename == 'faq.html':
        # FAQ Schema
        faq_items = []
        questions = soup.find_all('h4')
        for q in questions:
            question_text = q.text.strip()
            # find next p tag for answer
            answer_p = q.find_next_sibling('p')
            if answer_p:
                answer_text = answer_p.text.strip()
                faq_items.append({
                    "@type": "Question",
                    "name": question_text,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": answer_text
                    }
                })
        schemas.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_items
        })
    elif dirname == 'blog':
        # Blog Article Schema
        # Try to extract date
        date_pub = "2026-08-01"
        meta_div = soup.find('div', class_='blog-meta')
        if meta_div:
            spans = meta_div.find_all('span')
            if spans:
                date_pub = spans[0].text.strip() # very rough, would need proper parsing ideally, but good enough for static

        schemas.append({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "image": DEFAULT_IMAGE,
            "author": {
                "@type": "Organization",
                "name": "AruHome"
            },
            "publisher": {
                "@type": "Organization",
                "name": "AruHome",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{BASE_URL}Icon.png"
                }
            },
            "datePublished": date_pub,
            "dateModified": date_pub
        })
    elif dirname == 'maintenance':
        # Maintenance Article Schema
        schemas.append({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "image": DEFAULT_IMAGE,
            "author": {
                "@type": "Organization",
                "name": "AruHome"
            }
        })
        
    return schemas

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        
        if not soup.head:
            return
            
        # Determine URL
        rel_path = os.path.relpath(filepath, '.')
        url_path = rel_path.replace('\\', '/')
        if url_path == 'index.html':
            url_path = ''
        elif url_path.endswith('/index.html'):
            url_path = url_path.replace('index.html', '')
        url = BASE_URL + url_path
        
        title, description = extract_content(soup, filepath)
        
        clean_head(soup)
        
        # Append SEO Tags
        seo_tags = generate_seo_tags(soup, title, description, url)
        soup.head.append(seo_tags)
        
        # Append Schemas
        schemas = generate_schema(soup, filepath, url, title, description)
        if schemas:
            if len(schemas) == 1:
                schema_json = json.dumps(schemas[0], indent=2)
            else:
                schema_json = json.dumps(schemas, indent=2)
            
            script_tag = soup.new_tag('script', type='application/ld+json')
            script_tag.string = f"\n{schema_json}\n"
            soup.head.append(script_tag)
            
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
        print(f"Processed {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    files = []
    for root, dirs, filenames in os.walk('.'):
        # skip hidden dirs and assets
        parts = root.split(os.sep)
        if any(part.startswith('.') and part != '.' for part in parts):
            continue
        if 'assets' in root or 'images' in root:
            continue
        for filename in filenames:
            if filename.endswith('.html'):
                files.append(os.path.join(root, filename))
                
    for f in files:
        process_file(f)
