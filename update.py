import os
import re
import glob

base_dir = r"c:\Users\TSMBHO\AndroidStudioProjects\AruHome backup\Aruhome website\aruhome.github.io"
template_path = os.path.join(base_dir, "Template.txt")
maintenance_dir = os.path.join(base_dir, "maintenance")

# 1. Parse Template.txt
with open(template_path, 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

templates = []
current_template = None
current_section = None

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    # Check if line is a new template (starts with number and dot)
    if re.match(r'^\d+\.\s+', line):
        title = re.sub(r'^\d+\.\s+', '', line).strip()
        current_template = {
            'title': title,
            'before_you_start': [],
            'step_by_step': [],
            'cost_estimate': []
        }
        templates.append(current_template)
        current_section = None
    elif line == "Before You Start":
        current_section = 'before_you_start'
    elif line == "Step-by-Step Guide":
        current_section = 'step_by_step'
    elif line == "Cost Estimate":
        current_section = 'cost_estimate'
    else:
        if current_section and current_template:
            current_template[current_section].append(line)

html_files = glob.glob(os.path.join(maintenance_dir, "*.html"))

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # find title tag
    title_match = re.search(r'<title>(.*?)\s*\|\s*AruHome</title>', content)
    if not title_match:
        continue
    h1_title = title_match.group(1).strip()
    
    def normalize_title(t):
        t = t.replace('&amp;', '&').replace('"', '').replace("'", '').replace('.', '').replace('/', ' ')
        return re.sub(r'\s+', ' ', t).strip().lower()
        
    norm_h1 = normalize_title(h1_title)
    
    # map
    matched_template = next((t for t in templates if normalize_title(t['title']) == norm_h1), None)
    if not matched_template:
        matched_template = next((t for t in templates if normalize_title(t['title']) in norm_h1 or norm_h1 in normalize_title(t['title'])), None)
    
    if not matched_template:
        # Check by filename as fallback
        filename_base = os.path.basename(html_file).replace('.html', '').replace('-', ' ')
        matched_template = next((t for t in templates if filename_base in normalize_title(t['title']) or normalize_title(t['title']) in filename_base), None)
        
    if not matched_template:
        print(f"No match for {os.path.basename(html_file)} with title '{h1_title}'")
        continue

    # Update Before You Start
    # Find <ul ...> ... </ul> after "Before You Start"
    before_start_pattern = re.compile(r'(<h3[^>]*>[\s\n]*Before You Start[\s\n]*</h3>[\s\n]*<ul[^>]*>)(.*?)(</ul>)', re.DOTALL)
    
    def before_repl(m):
        ul_open = m.group(1)
        ul_close = m.group(3)
        items = matched_template['before_you_start']
        new_items = ""
        for item in items:
            new_items += f'''
              <li style="display: flex; align-items: flex-start; gap: 10px; margin-bottom: 15px; font-size: 1.1rem;">
                <svg fill="none" height="24" stroke="#ff4d4d" stroke-width="2" style="flex-shrink: 0; margin-top: 2px;"
                  viewbox="0 0 24 24" width="24">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z">
                  </path>
                  <line x1="12" x2="12" y1="9" y2="13"></line>
                  <line x1="12" x2="12.01" y1="17" y2="17"></line>
                </svg>
                {item}
              </li>'''
        return ul_open + new_items + "\n            " + ul_close

    content = before_start_pattern.sub(before_repl, content)

    # Update Step-by-Step Guide
    # Find h3 step by step guide, replace the list of divs
    step_pattern = re.compile(r'(<h3[^>]*>[\s\n]*Step-by-Step Guide[\s\n]*</h3>)(.*?)(<!-- Content Toggle / Hook -->)', re.DOTALL)
    
    def step_repl(m):
        h3_part = m.group(1)
        end_part = m.group(3)
        items = matched_template['step_by_step']
        new_items = "\n"
        for i, item in enumerate(items):
            new_items += f'''            <div style="margin-bottom: 25px; display: flex; gap: 20px;">
              <div
                style="background: var(--accent); color: #000; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">
                {i+1}</div>
              <div>
                <h4 style="color: var(--white); font-size: 1.2rem; margin-bottom: 5px;">{item}</h4>
              </div>
            </div>\n'''
        return h3_part + new_items + "            " + end_part
        
    content = step_pattern.sub(step_repl, content)

    # Update Cost Estimate
    cost_pattern = re.compile(r'(<h3[^>]*>[\s\n]*Cost Estimate[\s\n]*</h3>)(.*?)(</div>[\s\n]*<!-- App Features Teaser -->)', re.DOTALL)
    
    def cost_repl(m):
        h3_part = m.group(1)
        end_part = m.group(3)
        
        diy_cost = "Varies"
        diy_desc = ""
        pro_cost = "Varies"
        pro_desc = ""
        
        mode = None
        for line in matched_template['cost_estimate']:
            if line.startswith('DIY:'):
                diy_cost = line.split('DIY:')[1].strip()
                mode = 'diy'
            elif line.startswith('Professional:'):
                pro_cost = line.split('Professional:')[1].strip()
                mode = 'pro'
            else:
                if mode == 'diy':
                    diy_desc += line + " "
                elif mode == 'pro':
                    pro_desc += line + " "
                    
        diy_desc = diy_desc.strip()
        pro_desc = pro_desc.strip()
        
        res = h3_part + f'''
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
              <span style="color: var(--text-secondary);">DIY Cost</span>
              <span style="color: var(--accent); font-weight: bold;">{diy_cost}</span>
            </div>'''
        if diy_desc:
            res += f'''
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px;">({diy_desc})</p>'''
        else:
            res += f'''
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px;"></p>'''
            
        res += f'''
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
              <span style="color: var(--text-secondary);">Professional</span>
              <span style="color: #ff4d4d; font-weight: bold;">{pro_cost}</span>
            </div>'''
        if pro_desc:
            res += f'''
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0;">({pro_desc})</p>'''
        else:
            res += f'''
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0;"></p>'''
            
        return res + "\n          " + end_part
        
    content = cost_pattern.sub(cost_repl, content)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated {os.path.basename(html_file)}")
