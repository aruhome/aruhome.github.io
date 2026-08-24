import os
import re

def update_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change href="index.html#screenshots" to href="index.html#how-it-works"
    # Note that it might be prefixed, e.g. ../index.html#screenshots
    # So we replace just the anchor part for links that are #screenshots and the text is How It Works
    # Actually, just replace '#screenshots">How It Works' with '#how-it-works">How It Works'
    
    content = re.sub(r'#screenshots">How It Works', '#how-it-works">How It Works', content)
        
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
