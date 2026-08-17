import re

with open("maintenance-library.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update filter to include Renter Maintenance, Electrical & Safety, Windows & Interior
# First, insert new categories into the select options.
new_categories = """
                    <option value="electrical & safety">Electrical & Safety</option>
                    <option value="windows & interior">Windows & Interior</option>
                    <option value="renters">Renter-Friendly</option>
"""
# Find </select> for category filter
if '<option value="renters">Renter-Friendly</option>' not in content:
    content = content.replace('<option value="luxury / niche assets">Luxury / Niche Assets</option>', '<option value="luxury / niche assets">Luxury / Niche Assets</option>' + new_categories)

# 2. Add renters to appropriate existing cards
renter_friendly_titles = [
    "clean refrigerator condenser coils",
    "change hvac air filter",
    "clean garbage disposal",
    "clean range hood filter",
    "home router security audit",
    "subscription audit",
    "cloud backup verification",
    "digital legacy setup",
    "medicine cabinet purge",
    "first aid kit restock",
    "emergency go-bag check",
    "pet gear sanitation"
]

for title in renter_friendly_titles:
    # We need to find data-category="..." for the card with data-title="title"
    # and append ", renters" to it.
    pattern = r'(data-title="{}"\s+data-category=")([^"]+)(")'.format(title)
    def repl(m):
        cat = m.group(2)
        if 'renters' not in cat:
            cat += ", renters"
        return m.group(1) + cat + m.group(3)
    content = re.sub(pattern, repl, content)


# 3. Create the HTML for the new cards
new_ideas = [
    # Appliances
    ("Clean Washing Machine Drum", "laundry & appliances, renters", "Low", "Bi-Annual", "Washing Machine Drum", "Run a hot cycle with vinegar or a specialized cleaner to remove mold and odors.", "rgba(59, 226, 154, 0.1)", "rgba(59, 226, 154, 0.3)", "var(--accent)"),
    ("Clean Detergent Drawer", "laundry & appliances, renters", "Low", "Quarterly", "Washer Detergent Drawer", "Remove and scrub the detergent drawer to prevent mold buildup.", "rgba(59, 226, 154, 0.1)", "rgba(59, 226, 154, 0.3)", "var(--accent)"),
    ("Clean Dryer Lint Screen", "laundry & appliances, renters", "High", "Monthly", "Dryer Lint Screen", "Deep clean the lint screen with soap and water to remove invisible fabric softener residue.", "rgba(59, 226, 154, 0.1)", "rgba(59, 226, 154, 0.3)", "var(--accent)"),
    ("Inspect Dryer Vent Hose", "laundry & appliances", "High", "Annual", "Dryer Vent Hose", "Check the flexible hose for kinks, damage, or excessive lint buildup.", "rgba(59, 226, 154, 0.1)", "rgba(59, 226, 154, 0.3)", "var(--accent)"),
    ("Clean Dishwasher Spray Arms", "kitchen appliances, renters", "Medium", "Bi-Annual", "Dishwasher Spray Arms", "Use a toothpick to clear clogged holes in the spinning spray arms.", "rgba(59, 226, 154, 0.1)", "rgba(59, 226, 154, 0.3)", "var(--accent)"),
    ("Clean Refrigerator Seals", "kitchen appliances, renters", "Low", "Quarterly", "Refrigerator Door Seals", "Wipe down rubber gaskets with warm soapy water to ensure a tight seal and save energy.", "rgba(59, 226, 154, 0.1)", "rgba(59, 226, 154, 0.3)", "var(--accent)"),
    ("Clean Fridge Drain Hole", "kitchen appliances, renters", "Medium", "Annual", "Fridge Drain Hole", "Clear the defrost drain hole at the back of the fridge to prevent water pooling.", "rgba(59, 226, 154, 0.1)", "rgba(59, 226, 154, 0.3)", "var(--accent)"),
    ("Clean Coffee Maker", "kitchen appliances, renters", "Low", "Monthly", "Clean Coffee Maker", "Run a descaling solution or vinegar-water mix through your machine to remove mineral scale.", "rgba(59, 226, 154, 0.1)", "rgba(59, 226, 154, 0.3)", "var(--accent)"),
    ("Descale Electric Kettle", "kitchen appliances, renters", "Low", "Quarterly", "Descale Electric Kettle", "Boil a mixture of water and white vinegar to remove hard water deposits.", "rgba(59, 226, 154, 0.1)", "rgba(59, 226, 154, 0.3)", "var(--accent)"),
    ("Clean Air Fryer", "kitchen appliances, renters", "Medium", "Monthly", "Clean Air Fryer", "Deep clean the heating element and basket to prevent grease fires and smoking.", "rgba(59, 226, 154, 0.1)", "rgba(59, 226, 154, 0.3)", "var(--accent)"),
    
    # Plumbing
    ("Clean Faucet Aerator", "plumbing, renters", "Low", "Bi-Annual", "Faucet Aerator", "Unscrew and soak aerators in vinegar to restore smooth water flow.", "rgba(37, 99, 235, 0.1)", "rgba(37, 99, 235, 0.3)", "var(--primary-bright)"),
    ("Descale Showerhead", "plumbing, renters", "Low", "Bi-Annual", "Descale Showerhead", "Tie a bag of vinegar around the showerhead overnight to dissolve scale.", "rgba(37, 99, 235, 0.1)", "rgba(37, 99, 235, 0.3)", "var(--primary-bright)"),
    ("Clean Sink Drain", "plumbing, renters", "Medium", "Monthly", "Clean Sink Drain", "Pour boiling water or baking soda & vinegar to prevent grease and hair clogs.", "rgba(37, 99, 235, 0.1)", "rgba(37, 99, 235, 0.3)", "var(--primary-bright)"),
    ("Inspect Under-Sink Plumbing", "plumbing, renters", "High", "Bi-Annual", "Under-Sink Plumbing", "Check for slow drips or water damage under kitchen and bathroom sinks.", "rgba(37, 99, 235, 0.1)", "rgba(37, 99, 235, 0.3)", "var(--primary-bright)"),
    ("Check for Toilet Leaks", "plumbing, renters", "High", "Annual", "Hidden Toilet Leaks", "Put food coloring in the tank; if it bleeds into the bowl, the flapper needs replacing.", "rgba(37, 99, 235, 0.1)", "rgba(37, 99, 235, 0.3)", "var(--primary-bright)"),
    ("Inspect Washer Hoses", "plumbing", "High", "Annual", "Washing Machine Hoses", "Check for bulges or cracks. Replace rubber hoses with braided stainless steel if possible.", "rgba(37, 99, 235, 0.1)", "rgba(37, 99, 235, 0.3)", "var(--primary-bright)"),
    ("Inspect Dishwasher Hose", "plumbing", "High", "Annual", "Dishwasher Supply Hose", "Inspect the water supply line under the dishwasher for signs of leaking or wear.", "rgba(37, 99, 235, 0.1)", "rgba(37, 99, 235, 0.3)", "var(--primary-bright)"),
    ("Check Water Pressure", "plumbing", "Medium", "Annual", "Check Water Pressure", "Use a pressure gauge on an outdoor spigot to ensure pressure is under 80 PSI.", "rgba(37, 99, 235, 0.1)", "rgba(37, 99, 235, 0.3)", "var(--primary-bright)"),
    ("Clean Shower Drain", "plumbing, renters", "Medium", "Monthly", "Clean Shower Drain", "Remove hair and debris from the drain cover and trap.", "rgba(37, 99, 235, 0.1)", "rgba(37, 99, 235, 0.3)", "var(--primary-bright)"),
    ("Inspect Tub/Shower Drain", "plumbing, renters", "Medium", "Monthly", "Tub/Shower Drain", "Verify the drain stopper works and water drains at a normal speed.", "rgba(37, 99, 235, 0.1)", "rgba(37, 99, 235, 0.3)", "var(--primary-bright)"),

    # HVAC & Indoor Air
    ("Clean HVAC Return Grilles", "hvac, renters", "Low", "Bi-Annual", "HVAC Return Grilles", "Vacuum dust off the return grilles to maintain optimal airflow.", "rgba(245, 158, 11, 0.1)", "rgba(245, 158, 11, 0.3)", "#f59e0b"),
    ("Clean Supply Vents", "hvac, renters", "Low", "Bi-Annual", "Clean Supply Vents", "Wipe down ceiling or floor supply vents to prevent dust blowing into rooms.", "rgba(245, 158, 11, 0.1)", "rgba(245, 158, 11, 0.3)", "#f59e0b"),
    ("Clean Portable AC Filter", "hvac, renters", "Medium", "Monthly", "Portable AC Filter", "Wash or vacuum the filter to maintain cooling efficiency.", "rgba(245, 158, 11, 0.1)", "rgba(245, 158, 11, 0.3)", "#f59e0b"),
    ("Clean Window AC Filter", "hvac, renters", "Medium", "Monthly", "Window AC Filter", "Clean the front air filter; check the exterior fins for debris.", "rgba(245, 158, 11, 0.1)", "rgba(245, 158, 11, 0.3)", "#f59e0b"),
    ("Clean Dehumidifier", "hvac, renters", "Medium", "Monthly", "Clean Dehumidifier", "Empty and wash the water bucket; vacuum the air intake filter.", "rgba(245, 158, 11, 0.1)", "rgba(245, 158, 11, 0.3)", "#f59e0b"),
    ("Clean Air Purifier Filter", "hvac, renters", "Medium", "Monthly", "Air Purifier Filter", "Vacuum the pre-filter and check if the HEPA filter needs replacement.", "rgba(245, 158, 11, 0.1)", "rgba(245, 158, 11, 0.3)", "#f59e0b"),
    ("Clean Ceiling Fan Blades", "hvac, renters", "Low", "Bi-Annual", "Ceiling Fan Blades", "Wipe blades with a damp cloth; switch fan direction for summer/winter.", "rgba(245, 158, 11, 0.1)", "rgba(245, 158, 11, 0.3)", "#f59e0b"),
    ("Check Indoor Humidity", "hvac, renters", "Low", "Monthly", "Check Indoor Humidity", "Ensure indoor humidity stays between 30-50% to prevent mold and dry skin.", "rgba(245, 158, 11, 0.1)", "rgba(245, 158, 11, 0.3)", "#f59e0b"),

    # Electrical & Safety
    ("Test AFCI Protection", "electrical & safety", "Medium", "Monthly", "Test AFCI Protection", "Press the TEST button on AFCI breakers/outlets to verify arc-fault protection.", "rgba(239, 68, 68, 0.1)", "rgba(239, 68, 68, 0.3)", "#ef4444"),
    ("Inspect Extension Cords", "electrical & safety, renters", "High", "Annual", "Inspect Extension Cords", "Check for frayed wires or signs of overheating; discard damaged cords.", "rgba(239, 68, 68, 0.1)", "rgba(239, 68, 68, 0.3)", "#ef4444"),
    ("Inspect Power Strips", "electrical & safety, renters", "High", "Annual", "Inspect Power Strips", "Ensure surge protectors aren't overloaded or expired.", "rgba(239, 68, 68, 0.1)", "rgba(239, 68, 68, 0.3)", "#ef4444"),
    ("Replace Smoke Det. Battery", "electrical & safety, renters", "High", "Annual", "Smoke Detector Batteries", "Test alarms monthly; replace standard batteries annually.", "rgba(239, 68, 68, 0.1)", "rgba(239, 68, 68, 0.3)", "#ef4444"),
    ("Replace CO Det. Battery", "electrical & safety, renters", "High", "Annual", "CO Detector Batteries", "Test Carbon Monoxide alarms; replace batteries annually.", "rgba(239, 68, 68, 0.1)", "rgba(239, 68, 68, 0.3)", "#ef4444"),
    ("Test Emergency Lighting", "electrical & safety", "Medium", "Bi-Annual", "Test Emergency Lighting", "Verify any battery-powered emergency or security lights function correctly.", "rgba(239, 68, 68, 0.1)", "rgba(239, 68, 68, 0.3)", "#ef4444"),
    ("Check Outlet/Switch Cond.", "electrical & safety, renters", "Medium", "Annual", "Outlet/Switch Condition", "Check for loose plugs, warm faceplates, or buzzing sounds.", "rgba(239, 68, 68, 0.1)", "rgba(239, 68, 68, 0.3)", "#ef4444"),
    ("Review Emergency Contacts", "health & safety, renters", "High", "Annual", "Emergency Contacts", "Update the physical list of doctors, plumbers, and local emergency numbers.", "rgba(245, 158, 11, 0.1)", "rgba(245, 158, 11, 0.3)", "#f59e0b"),

    # Windows & Interior
    ("Clean Window Screens", "windows & interior, renters", "Low", "Annual", "Clean Window Screens", "Remove screens and wash gently with soapy water to improve air flow.", "rgba(14, 165, 233, 0.1)", "rgba(14, 165, 233, 0.3)", "#0ea5e9"),
    ("Clean Window Weep Holes", "windows & interior", "Medium", "Annual", "Clean Window Weep Holes", "Clear the small drain holes at the bottom of window frames.", "rgba(14, 165, 233, 0.1)", "rgba(14, 165, 233, 0.3)", "#0ea5e9"),
    ("Lubricate Door Hinges", "windows & interior, renters", "Low", "Annual", "Lubricate Door Hinges", "Apply silicone spray or WD-40 to stop squeaks and reduce wear.", "rgba(14, 165, 233, 0.1)", "rgba(14, 165, 233, 0.3)", "#0ea5e9"),
    ("Lubricate Sliding Tracks", "windows & interior, renters", "Medium", "Bi-Annual", "Sliding Door Tracks", "Vacuum dirt from tracks and apply dry silicone lubricant.", "rgba(14, 165, 233, 0.1)", "rgba(14, 165, 233, 0.3)", "#0ea5e9"),
    ("Inspect Door Sweep", "windows & interior, renters", "Medium", "Annual", "Inspect Door Sweep", "Check exterior door sweeps for gaps to prevent drafts and bugs.", "rgba(14, 165, 233, 0.1)", "rgba(14, 165, 233, 0.3)", "#0ea5e9"),
    ("Inspect Interior Caulking", "windows & interior, renters", "Medium", "Annual", "Interior Caulking", "Look for cracked caulk around tubs, sinks, and windows; re-caulk if needed.", "rgba(14, 165, 233, 0.1)", "rgba(14, 165, 233, 0.3)", "#0ea5e9"),
    ("Touch Up Wall Damage", "windows & interior, renters", "Low", "Annual", "Touch Up Wall Damage", "Fill nail holes and touch up scuffed paint.", "rgba(14, 165, 233, 0.1)", "rgba(14, 165, 233, 0.3)", "#0ea5e9"),
    ("Inspect Flooring for Damage", "windows & interior, renters", "Medium", "Annual", "Flooring Damage", "Check for loose tiles, lifted laminate, or carpet snags.", "rgba(14, 165, 233, 0.1)", "rgba(14, 165, 233, 0.3)", "#0ea5e9"),

    # Exterior / Property
    ("Inspect Exterior Drainage", "exterior", "High", "Bi-Annual", "Exterior Drainage", "Ensure soil slopes away from the foundation; check downspout extensions.", "rgba(139, 92, 246, 0.1)", "rgba(139, 92, 246, 0.3)", "#a78bfa"),
    ("Clean Exterior Light Fixtures", "exterior, renters", "Low", "Annual", "Exterior Light Fixtures", "Remove bugs and cobwebs; check weather seals on fixtures.", "rgba(139, 92, 246, 0.1)", "rgba(139, 92, 246, 0.3)", "#a78bfa"),
    ("Inspect Outdoor Faucets", "exterior", "High", "Annual", "Outdoor Faucets", "Detach hoses before freezing weather; check for leaks or drips.", "rgba(139, 92, 246, 0.1)", "rgba(139, 92, 246, 0.3)", "#a78bfa"),
    ("Inspect Patio/Porch", "exterior", "Medium", "Annual", "Inspect Patio/Porch", "Check for loose boards, wood rot, or uneven pavers.", "rgba(139, 92, 246, 0.1)", "rgba(139, 92, 246, 0.3)", "#a78bfa"),
    ("Check Outdoor Furniture", "exterior, renters", "Low", "Annual", "Outdoor Furniture", "Inspect for rust or loose screws; clean cushions before storage.", "rgba(139, 92, 246, 0.1)", "rgba(139, 92, 246, 0.3)", "#a78bfa"),
    ("Inspect Attic for Pests", "exterior", "High", "Bi-Annual", "Attic Moisture/Pests", "Look for signs of roof leaks, mold, or rodent droppings in the attic.", "rgba(139, 92, 246, 0.1)", "rgba(139, 92, 246, 0.3)", "#a78bfa")
]

new_html = ""
for i, item in enumerate(new_ideas):
    title_data, cats, priority, freq, tag, desc, bg, border, color = item
    priority_color = "#f59e0b"
    if priority == "High":
        priority_color = "#ef4444"
    elif priority == "Low":
        priority_color = "var(--accent)"
        
    card = f"""
                <div class="task-card-link" data-title="{title_data.lower()}" data-category="{cats}" data-priority="{priority.lower()}" style="display: block;">
                    <div class="feature-card reveal" style="padding: 30px; transition: transform 0.3s; height: 100%; border: 1px solid var(--border);">
                        <span class="hero-tag" style="background: {bg}; border-color: {border}; color: {color}; font-size: 0.75rem; margin-bottom: 10px;">{tag}</span>
                        <h3 style="margin-top: 10px; font-size: 1.4rem;">{title_data}</h3>
                        <p style="font-size: 0.95rem; margin-bottom: 20px;">{desc}</p>
                        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border); padding-top: 15px;">
                            <span style="font-size: 0.85rem; font-weight: 600; color: {priority_color};">Priority: {priority}</span>
                            <span style="font-size: 0.85rem; color: var(--text-muted);">Frequency: {freq}</span>
                        </div>
                    </div>
                </div>
"""
    new_html += card

content = content.replace('            </div>\n            \n            <div style="text-align: center; margin-top: 50px;">', new_html + '\n            </div>\n            \n            <div style="text-align: center; margin-top: 50px;">')

with open("maintenance-library.html", "w", encoding="utf-8") as f:
    f.write(content)

# Update script.js to support comma separated categories
with open("script.js", "r", encoding="utf-8") as f:
    script_content = f.read()

# Replace: const matchesCategory = category === 'all' || cardCat === category;
# With: const matchesCategory = category === 'all' || cardCat.split(',').map(s=>s.trim()).includes(category);
script_content = script_content.replace(
    "const matchesCategory = category === 'all' || cardCat === category;",
    "const matchesCategory = category === 'all' || cardCat.split(',').map(s=>s.trim()).includes(category);"
)

with open("script.js", "w", encoding="utf-8") as f:
    f.write(script_content)

