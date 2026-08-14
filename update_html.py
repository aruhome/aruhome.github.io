import os

base_dir = r'c:\Users\TSMBHO\AndroidStudioProjects\AruHome backup\Aruhome website'

def replace_in_file(filename, old_str, new_str):
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace(old_str, new_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

# 1. Update the icon in all html files
old_icon = """<div style="width: 40px; height: 40px; background: var(--primary); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px;">A</div>"""
new_icon = """<img src="Icon.png" alt="AruHome Logo" style="width: 40px; height: 40px; border-radius: 12px; margin-right: 10px;">"""

html_files = ['index.html', 'faq.html', 'privacy.html', 'terms.html', 'contact.html']
for f in html_files:
    replace_in_file(f, old_icon, new_icon)

# Also add the favicon to the html files
old_css_link = '<link rel="stylesheet" href="styles.css">'
new_css_link = '<link rel="stylesheet" href="styles.css">\n    <link rel="icon" type="image/png" href="Icon.png">'
for f in html_files:
    replace_in_file(f, old_css_link, new_css_link)

# 2. Update the screenshots in index.html
old_hero = """<!-- Placeholder for Hero Phone Image -->
            <div class="hero-image-placeholder reveal reveal-delay-5" style="margin-top: 4rem; width: 100%; max-width: 400px; height: 600px; background: var(--bg-card); border: 2px dashed var(--border-accent); border-radius: 24px; display: flex; align-items: center; justify-content: center; margin-left: auto; margin-right: auto; color: var(--text-muted);">
                <p>App Screenshot Placeholder (Home Dashboard)</p>
            </div>"""
new_hero = """<div class="hero-image reveal reveal-delay-5" style="margin-top: 4rem; text-align: center;">
                <img src="images/google_pixel_4_xl_screenshot_1.webp" alt="AruHome Dashboard" style="max-width: 100%; height: auto; max-height: 600px; border-radius: 24px; box-shadow: var(--shadow-lg);">
            </div>"""
replace_in_file('index.html', old_hero, new_hero)

old_screens = """<div style="width: 280px; height: 500px; background: var(--bg-card); border: 2px dashed var(--border-accent); border-radius: 20px; display: flex; align-items: center; justify-content: center; color: var(--text-muted); text-align: center; padding: 20px;">
                    <p>Screenshot 1<br>(Asset Vault)</p>
                </div>
                <div style="width: 280px; height: 500px; background: var(--bg-card); border: 2px dashed var(--border-accent); border-radius: 20px; display: flex; align-items: center; justify-content: center; color: var(--text-muted); text-align: center; padding: 20px;">
                    <p>Screenshot 2<br>(Maintenance Schedule)</p>
                </div>
                <div style="width: 280px; height: 500px; background: var(--bg-card); border: 2px dashed var(--border-accent); border-radius: 20px; display: flex; align-items: center; justify-content: center; color: var(--text-muted); text-align: center; padding: 20px;">
                    <p>Screenshot 3<br>(Expense Charts)</p>
                </div>"""
new_screens = """<img src="images/google_pixel_4_xl_screenshot_2.webp" alt="Asset Vault" style="width: 280px; height: auto; border-radius: 20px; box-shadow: var(--shadow-md);">
                <img src="images/google_pixel_4_xl_screenshot_3.webp" alt="Maintenance Schedule" style="width: 280px; height: auto; border-radius: 20px; box-shadow: var(--shadow-md);">
                <img src="images/google_pixel_4_xl_screenshot_4.webp" alt="Expense Charts" style="width: 280px; height: auto; border-radius: 20px; box-shadow: var(--shadow-md);">"""
replace_in_file('index.html', old_screens, new_screens)

print("HTML files updated successfully")
