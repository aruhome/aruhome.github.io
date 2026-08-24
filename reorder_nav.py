import os
import re

def reorder_nav(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the nav-links block
    nav_match = re.search(r'(<ul class="nav-links" id="navLinks">)(.*?)(</ul>)', content, re.DOTALL)
    if nav_match:
        nav_start = nav_match.group(1)
        nav_items_str = nav_match.group(2)
        nav_end = nav_match.group(3)

        # Extract items
        # They look like: <li><a href="...">...</a></li>
        items = re.findall(r'(\s*<li>.*?</li>)', nav_items_str, re.DOTALL)
        
        # We need to swap the first and second items
        # Usually:
        # items[0] is Features
        # items[1] is How It Works
        # Let's check if they contain what we expect before swapping
        if len(items) >= 2 and 'Features' in items[0] and 'How It Works' in items[1]:
            items[0], items[1] = items[1], items[0]
            
            # Reconstruct the nav block
            new_nav_items_str = ''.join(items)
            new_nav = nav_start + new_nav_items_str + "\n                " + nav_end
            
            content = content[:nav_match.start()] + new_nav + content[nav_match.end():]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            try:
                reorder_nav(os.path.join(root, file))
            except Exception as e:
                print(f"Error processing {file}: {e}")
print("Done")
