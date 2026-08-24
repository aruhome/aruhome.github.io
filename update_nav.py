import os
import re

def update_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Change 'Screenshots' text to 'How It Works'
    content = re.sub(r'(<a href="[^"]*?index\.html#screenshots">)Screenshots(</a>)', r'\g<1>How It Works\g<2>', content)
    
    # 2. Change 'Library' text to 'Maintenance Library'
    content = re.sub(r'(<a href="[^"]*?maintenance-library\.html">)Library(</a>)', r'\g<1>Maintenance Library\g<2>', content)
    
    # 3. Remove Calendar
    content = re.sub(r'\s*<li><a href="[^"]*?maintenance-calendar\.html">Calendar</a></li>', '', content)
    
    # 4. Remove Privacy from nav
    content = re.sub(r'\s*<li><a href="[^"]*?privacy\.html">Privacy</a></li>', '', content)
    
    # 5. Remove Contact from nav
    content = re.sub(r'\s*<li><a href="[^"]*?contact\.html">Contact</a></li>', '', content)
    
    # 6. Change 'Download App' to 'Download'
    content = re.sub(r'Download App(\s*</a>)', r'Download\g<1>', content)
    
    # 7. Add Contact to footer if not already there
    # Look for terms.html link in footer-links
    terms_match = re.search(r'<a href="([^"]*?terms\.html)">Terms of Service</a>', content)
    if terms_match:
        terms_href = terms_match.group(1)
        contact_href = terms_href.replace('terms.html', 'contact.html')
        # Check if Contact is already there to avoid duplicates
        if contact_href + '">Contact</a>' not in content:
            content = re.sub(
                r'(<a href="[^"]*?terms\.html">Terms of Service</a>)',
                r'\g<1>\n                    <a href="' + contact_href + '">Contact</a>',
                content
            )
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            try:
                update_html_file(os.path.join(root, file))
            except Exception as e:
                print(f"Error processing {file}: {e}")
print("Done")
