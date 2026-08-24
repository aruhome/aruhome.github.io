import os
from bs4 import BeautifulSoup

customizations = {
    'maintenance/subscription-audit.html': {
        'time': '30 mins', 'difficulty': 'Easy', 'skill': 'Beginner',
        'why': 'Unused subscriptions (streaming services, gym memberships, apps) quietly drain your bank account every month. A regular audit can easily save you hundreds of dollars a year.',
        'step1_title': 'Gather Statements',
        'step1_desc': 'Review your last two months of credit card and bank statements.',
        'step2_title': 'Identify and List',
        'step2_desc': 'List every recurring charge. Highlight any service you haven\'t used in the past 30 days.',
        'step3_title': 'Cancel Unused Services',
        'step3_desc': 'Log into those accounts or call customer service to cancel the subscriptions you no longer need.',
        'mistake': 'Forgetting about annual subscriptions that only charge once a year. Be sure to check your history for large yearly renewals.',
        'diy_cost': '$0', 'pro_cost': 'N/A'
    },
    'maintenance/digital-legacy-setup.html': {
        'time': '1 hour', 'difficulty': 'Moderate', 'skill': 'Intermediate',
        'why': 'In the event of an emergency or passing, your loved ones will need access to your digital life. Setting up legacy contacts ensures they aren\'t locked out of important accounts, photos, and documents.',
        'step1_title': 'Apple/Google Legacy Contacts',
        'step1_desc': 'Navigate to your Apple ID or Google Account settings and assign a trusted family member as your official Legacy Contact.',
        'step2_title': 'Password Manager Access',
        'step2_desc': 'If you use a password manager, set up an emergency access protocol or ensure a trusted person knows where to find your master password.',
        'step3_title': 'Document and Share',
        'step3_desc': 'Write down instructions on how to access your phone and computer, and store this in a secure location like a fireproof safe.',
        'mistake': 'Setting someone as a legacy contact but never telling them about it. Make sure they know they have been designated and understand what to do.',
        'diy_cost': '$0', 'pro_cost': '$100-$300'
    },
    'maintenance/medicine-cabinet-purge.html': {
        'time': '15 mins', 'difficulty': 'Easy', 'skill': 'Beginner',
        'why': 'Expired medications can lose their effectiveness or even become dangerous. Keeping a cluttered cabinet also makes it harder to find what you need in an emergency.',
        'step1_title': 'Empty and Inspect',
        'step1_desc': 'Take everything out of the cabinet. Check the expiration dates on all prescription and over-the-counter medications.',
        'step2_title': 'Safely Dispose',
        'step2_desc': 'Do not flush most medications down the toilet. Mix expired pills with unappealing materials like coffee grounds in a sealed bag, or take them to a local pharmacy drop-off.',
        'step3_title': 'Reorganize',
        'step3_desc': 'Wipe down the shelves and organize the remaining unexpired items by category, keeping daily medications easily accessible.',
        'mistake': 'Throwing prescription bottles with your personal information directly into the recycling bin. Always peel off or black out the labels first.',
        'diy_cost': '$0', 'pro_cost': 'N/A'
    },
    'maintenance/first-aid-kit-restock.html': {
        'time': '20 mins', 'difficulty': 'Easy', 'skill': 'Beginner',
        'why': 'Accidents happen without warning. A fully stocked and up-to-date first aid kit is critical for handling minor injuries at home before they become severe.',
        'step1_title': 'Inventory Current Supplies',
        'step1_desc': 'Open your kit and throw away any expired ointments, dried-out wipes, or damaged bandages.',
        'step2_title': 'Identify Missing Items',
        'step2_desc': 'Check your inventory against a standard Red Cross list. Make sure you have enough sterile gauze, adhesive bandages, antiseptic wipes, and medical tape.',
        'step3_title': 'Purchase and Restock',
        'step3_desc': 'Buy replacement supplies for anything that is missing or expired, and neatly pack them back into the kit.',
        'mistake': 'Forgetting to restock customized items like family-specific allergy medications or an EpiPen.',
        'diy_cost': '$10-$30', 'pro_cost': 'N/A'
    },
    'maintenance/emergency-go-bag-check.html': {
        'time': '45 mins', 'difficulty': 'Moderate', 'skill': 'Beginner',
        'why': 'In the event of a fire, flood, or natural disaster, you may have only minutes to evacuate. A ready-to-go emergency bag ensures you have survival essentials and important documents.',
        'step1_title': 'Check Food and Water',
        'step1_desc': 'Replace any expired emergency rations, protein bars, or bottled water with fresh supplies.',
        'step2_title': 'Test Electronics',
        'step2_desc': 'Check the batteries in your flashlights and emergency radios. Replace them if necessary and pack extra batteries.',
        'step3_title': 'Update Documents and Cash',
        'step3_desc': 'Ensure you have a small amount of emergency cash and that the photocopies of your IDs and insurance documents are current.',
        'mistake': 'Making the bag too heavy to comfortably carry for long distances. Stick strictly to lightweight essentials.',
        'diy_cost': '$20-$50', 'pro_cost': 'N/A'
    }
}

for filepath, data in customizations.items():
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Update Quick Stats
    stats_spans = soup.find_all('span', style=lambda value: value and 'font-size: 1.2rem' in value)
    if len(stats_spans) >= 3:
        stats_spans[0].string = data['time']
        stats_spans[1].string = data['difficulty']
        stats_spans[2].string = data['skill']
        
    # 2. Update Why It Matters
    why_h3 = soup.find('h3', string=lambda text: text and 'Why It Matters' in text)
    if why_h3:
        why_p = why_h3.find_next_sibling('p')
        if why_p:
            why_p.string = data['why']
            
    # 3. Update Steps
    step1_div = soup.find('div', string="1")
    if step1_div:
        step1_h4 = step1_div.parent.find('h4')
        if step1_h4: step1_h4.string = data['step1_title']
        step1_p = step1_div.parent.find('p')
        if step1_p: step1_p.string = data['step1_desc']
        
    step2_div = soup.find('div', string="2")
    if step2_div:
        step2_h4 = step2_div.parent.find('h4')
        if step2_h4: step2_h4.string = data['step2_title']
        step2_p = step2_div.parent.find('p')
        if step2_p: step2_p.string = data['step2_desc']

    step3_div = soup.find('div', string="3")
    if step3_div:
        step3_h4 = step3_div.parent.find('h4')
        if step3_h4: step3_h4.string = data['step3_title']
        step3_p = step3_div.parent.find('p')
        if step3_p: step3_p.string = data['step3_desc']
        
    # 4. Update Common Mistake
    mistake_h3 = soup.find('h3', string=lambda text: text and 'Common Mistake' in text)
    if mistake_h3:
        mistake_p = mistake_h3.find_next_sibling('p')
        if mistake_p: mistake_p.string = data['mistake']
        
    # 5. Update Costs
    cost_estimate_h3 = soup.find('h3', string=lambda text: text and 'Cost Estimate' in text)
    if cost_estimate_h3:
        diy_span = cost_estimate_h3.find_next_sibling('div').find_all('span')[1]
        diy_span.string = data['diy_cost']
        pro_span = cost_estimate_h3.find_next_sibling('div').find_next_sibling('div').find_all('span')[1]
        pro_span.string = data['pro_cost']

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Updated {filepath}")
