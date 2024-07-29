import pandas as pd
import re
import os

# Load the provided Excel file
file_path = '/Users/kyungwanwoo/Downloads/contact_export_1102701457545_070224_080255.xls'
df = pd.read_excel(file_path, engine='xlrd')

# Define categories and corresponding keywords
categories = {
    "University": ["university", "college", "institute", "school", "academy", "u ", "u. ", "univ", "polytechnic", "community college", "universite", "edu", "ucla", "ucsf"],
    "NGO": ["council", "foundation", "ngo", "non-profit", "nonprofit", "association", "charity", "federation", "society", "network", "cooperative"],
    "Government": ["department", "ministry", "agency", "government", "bureau", "office", "commission", "administration", "authority", "board", "service", "gov", "mil"],
    "Private": ["inc", "corp", "company", "llc", "limited", "co.", "group", "industries", "enterprise", "ventures", "solutions", "technologies", "systems"],
    "Healthcare": ["hospital", "clinic", "health center", "medical center", "health services", "healthcare", "health foundation"],
    "Research": ["research institute", "research center", "laboratory", "research foundation", "biomedical"],
    "Non-Profit": ["non-profit", "nonprofit", "charity", "foundation", "volunteer", "service organization"],
    "Educational": ["primary school", "secondary school", "high school", "elementary school", "middle school", "kindergarten", "academy"],
    "Industry Association": ["association", "federation", "chamber of commerce", "society", "consortium", "union"],
    "International Organization": ["united nations", "world bank", "international monetary fund", "world health organization", "UNICEF", "UNESCO", "international"],
    "Other": []  # Any other keywords if needed
}

# Add domain-based keywords to categories
domain_categories = {
    "University": ["edu"],
    "Government": ["gov", "mil"],
    "Non-Profit": ["org"]
}

# Function to check domain-based categorization
def categorize_by_domain(email):
    domain = email.split('@')[-1].split('.')[-1]
    for category, domains in domain_categories.items():
        if domain in domains:
            return category
    return None

# Create output directory
output_dir = '/Users/kyungwanwoo/Downloads/Categorized_Contacts'
os.makedirs(output_dir, exist_ok=True)

# Filter and save each category to a different Excel file
for category, keywords in categories.items():
    if keywords:  # Only filter if there are keywords defined
        category_df = df[df['Company'].str.contains('|'.join(keywords), case=False, na=False) | df['Email'].apply(lambda x: categorize_by_domain(x) == category if pd.notna(x) else False)]
    else:  # Handle the "other" category
        known_keywords = [item for sublist in categories.values() for item in sublist]
        category_df = df[~df['Company'].str.contains('|'.join(known_keywords), case=False, na=False)]
        known_domains = [item for sublist in domain_categories.values() for item in sublist]
        category_df = category_df[~category_df['Email'].apply(lambda x: categorize_by_domain(x) in domain_categories if pd.notna(x) else False)]

    # Define the output path for the category
    output_path = os.path.join(output_dir, f'{category}_contacts.xlsx')

    # Save the filtered DataFrame to a new Excel file
    category_df.to_excel(output_path, index=False)
    print(f"Filtered contacts for {category} saved to {output_path}")

print("All categories processed and saved.")
