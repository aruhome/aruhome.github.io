import os
import glob
from bs4 import BeautifulSoup

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # Fix main content grid
        grid_divs = soup.find_all('div', style=lambda value: value and 'grid-template-columns: 1fr 300px' in value)
        for div in grid_divs:
            # Add class content-grid
            classes = div.get('class', [])
            if 'content-grid' not in classes:
                classes.append('content-grid')
                div['class'] = classes
            # Remove inline grid styles
            styles = div.get('style', '')
            new_styles = [s.strip() for s in styles.split(';') if s.strip() and not s.strip().startswith('display: grid') and not s.strip().startswith('grid-template-columns') and not s.strip().startswith('gap:')]
            div['style'] = '; '.join(new_styles) + (';' if new_styles else '')

        # Fix related tasks flex
        flex_divs = soup.find_all('div', style=lambda value: value and 'display: flex' in value and 'gap: 20px' in value and 'flex-wrap' not in value)
        for div in flex_divs:
            # Check if it's the one under Related Tasks
            prev = div.find_previous_sibling('h3')
            if prev and 'Related Maintenance' in prev.text:
                classes = div.get('class', [])
                if 'related-tasks-flex' not in classes:
                    classes.append('related-tasks-flex')
                    div['class'] = classes
                styles = div.get('style', '')
                new_styles = [s.strip() for s in styles.split(';') if s.strip() and not s.strip().startswith('display: flex') and not s.strip().startswith('gap:')]
                div['style'] = '; '.join(new_styles) + (';' if new_styles else '')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    for f in glob.glob('maintenance/*.html'):
        process_file(f)
