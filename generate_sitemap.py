import os
import glob
from datetime import datetime

BASE_URL = "https://aruhome.github.io"

def generate_sitemap():
    urls = []
    
    # Priority 1.0
    urls.append({'loc': '/', 'priority': '1.0', 'changefreq': 'weekly'})
    
    # Priority 0.8
    important_pages = [
        'faq.html',
        'maintenance-library.html',
        'blog/index.html'
    ]
    for p in important_pages:
        urls.append({'loc': f'/{p}', 'priority': '0.8', 'changefreq': 'weekly'})
        
    # Priority 0.6
    for filepath in glob.glob('maintenance/*.html'):
        rel_path = filepath.replace('\\', '/')
        urls.append({'loc': f'/{rel_path}', 'priority': '0.6', 'changefreq': 'monthly'})
        
    for filepath in glob.glob('blog/*.html'):
        rel_path = filepath.replace('\\', '/')
        if rel_path != 'blog/index.html':
            urls.append({'loc': f'/{rel_path}', 'priority': '0.6', 'changefreq': 'monthly'})
            
    # Priority 0.5
    legal_pages = ['privacy.html', 'terms.html']
    for p in legal_pages:
        urls.append({'loc': f'/{p}', 'priority': '0.5', 'changefreq': 'yearly'})
        
    # Build XML
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    lastmod = datetime.now().strftime("%Y-%m-%d")
    
    for u in urls:
        xml.append('  <url>')
        xml.append(f'    <loc>{BASE_URL}{u["loc"]}</loc>')
        xml.append(f'    <lastmod>{lastmod}</lastmod>')
        xml.append(f'    <changefreq>{u["changefreq"]}</changefreq>')
        xml.append(f'    <priority>{u["priority"]}</priority>')
        xml.append('  </url>')
        
    xml.append('</urlset>')
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml))
        
    print(f"Generated sitemap.xml with {len(urls)} URLs")
    
def generate_robots():
    content = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Generated robots.txt")

if __name__ == "__main__":
    generate_sitemap()
    generate_robots()
