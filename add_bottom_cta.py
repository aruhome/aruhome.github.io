import os
import glob

cta_html = """
    <!-- Bottom CTA Section -->
    <section class="cta-section reveal" style="padding: 80px 0; background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(56, 189, 248, 0.05) 100%); border-top: 1px solid var(--border-accent); text-align: center;">
        <div class="container">
            <h2 style="font-size: clamp(2rem, 4vw, 3rem); color: var(--text-primary); margin-bottom: 20px;">Take control of your home</h2>
            <p style="font-size: 1.15rem; color: var(--text-secondary); max-width: 600px; margin: 0 auto 40px auto; line-height: 1.6;">Keep your inventory, maintenance, warranties and records organized in one place.</p>
            <a href="#" class="nav-cta" style="display: inline-flex; align-items: center; justify-content: center; padding: 14px 28px; font-size: 1.1rem; font-weight: 600; color: #ffffff; background: linear-gradient(135deg, var(--primary) 0%, #a78bfa 100%); border-radius: 12px; text-decoration: none; box-shadow: 0 4px 14px rgba(139, 92, 246, 0.4); transition: transform 0.3s ease, box-shadow 0.3s ease; border: none;">
                <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" style="width:24px;height:24px;margin-right:10px;">
                    <path d="M3.18 23.76c.35.2.75.24 1.13.1l12.09-6.96-2.76-2.76L3.18 23.76z" />
                    <path d="M22.32 10.66a1.74 1.74 0 000-3.02l-2.88-1.66-3.06 3.06 3.06 3.06 2.88-1.44z" />
                    <path d="M2.04 1.2A1.74 1.74 0 001 2.76v18.48c0 .66.36 1.26.9 1.56l.14.08 10.35-10.35L2.04 1.2z" />
                    <path d="M16.4 5.1L4.31.14C3.93 0 3.53.04 3.18.24l10.46 10.46L16.4 5.1z" />
                </svg>
                Get AruHome on Google Play
            </a>
        </div>
    </section>
"""

# files to update
files = [
    'faq.html',
    'maintenance-library.html'
]
files.extend(glob.glob('maintenance/*.html'))
files.extend(glob.glob('blog/*.html'))

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already added
        if 'Take control of your home' not in content:
            # Insert before <footer
            if '<footer' in content:
                content = content.replace('<footer', cta_html + '\n    <footer', 1)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {filepath}")
            else:
                print(f"No footer found in {filepath}")
