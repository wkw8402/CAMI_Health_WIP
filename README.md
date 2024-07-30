# Contact Categorizer

This project is designed to categorize contact information from an Excel file into different categories based on company names and email domains. The categories include University, NGO, Government, Private, Healthcare, Research, Non-Profit, Educational, Industry Association, International Organization, UK, and Other. The categorized contacts are then saved into separate Excel files for easier management and access.

## Features

- **Company Name Categorization:** Categorizes contacts based on keywords in company names.
- **Email Domain Categorization:** Categorizes contacts based on email domains.
- **Customizable Categories:** Easily add or modify categories and their corresponding keywords.
- **Excel File Handling:** Reads contacts from an Excel file and saves categorized contacts into separate Excel files.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/contact-categorizer.git
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd contact-categorizer
   ```
3. **Install Required Packages:**
   Ensure you have `pandas` and `openpyxl` installed. If not, you can install them using pip:
   ```bash
   pip install pandas openpyxl
   ```

## Usage

1. **Prepare Your Excel File:**
   - Ensure your Excel file has columns named `Company` and `Email`.

2. **Update the File Path:**
   - In the script, update the `file_path` variable with the path to your Excel file:
     ```python
     file_path = '/path/to/your/Other_contacts.xlsx'
     ```

3. **Run the Script:**
   ```bash
   python categorize_contacts.py
   ```

4. **Output:**
   - The script will generate a directory named `Categorized_Contacts` in the same directory as the original file, containing separate Excel files for each category.

## Script Overview

### Categories and Keywords

The script uses predefined categories and their corresponding keywords to filter contacts. You can customize these categories and keywords as needed.

### Domain-Based Categorization

The script also categorizes contacts based on email domains. For example, `.edu` emails are categorized under "University", `.gov` emails under "Government", and `.uk` emails under "UK".

### Filtering and Saving

The script filters contacts based on both company names and email domains, and saves the filtered contacts into separate Excel files for each category.

## Customization

- **Add or Modify Categories:**
  - Edit the `categories` and `domain_categories` dictionaries to add or modify categories and their keywords.

## Example

Here's a simplified example of how the script works:

```python
import pandas as pd
import re
import os

# Load the provided Excel file
file_path = '/Users/kyungwanwoo/Downloads/contact_export_1102701457545_072924_112559.xls'
df = pd.read_excel(file_path, engine='xlrd')

# Define categories and corresponding keywords
categories = {
    "University": ["university", "college", "institute", "school", "academy", "u ", "u. ", "univ", "polytechnic", "community college", "universite", "edu", "UCLA", "UCSF", "UNSW"],
    "NGO": ["council", "foundation", "ngo", "non-profit", "nonprofit", "association", "charity", "federation", "society", "network", "cooperative"],
    "Government": ["department", "ministry", "agency", "government", "bureau", "office", "commission", "administration", "authority", "board", "service", "gov", "mil", "NIH", "CDC", "WHRI", "USAID"],
    "Private": ["inc", "corp", "company", "llc", "limited", "co.", "group", "industries", "enterprise", "ventures", "solutions", "technologies", "systems", "Intel", "IBM Watson Health", ],
    "Healthcare": ["hospital", "clinic", "health center", "medical center", "health services", "healthcare", "health foundation"],
    "Research": ["research institute", "research center", "laboratory", "research foundation", "biomedical", "Wits RHI"],
    "Non-Profit": ["non-profit", "nonprofit", "charity", "foundation", "volunteer", "service organization"],
    "Educational": ["primary school", "secondary school", "high school", "elementary school", "middle school", "kindergarten", "academy"],
    "Industry Association": ["association", "federation", "chamber of commerce", "society", "consortium", "union"],
    "International Organization": ["united nations", "world bank", "international monetary fund", "world health organization", "WHO","UNICEF", "UNESCO", "UNFPA", "UNITAID", "Unitaid", "international", "int"],
    "UK": ["London", "UK"],
    "India": ["India"],
    "Canada": ["Canada"],
    "Australia": ["Australia"],
    "Other": []  # Any other keywords if needed
}

# Add domain-based keywords to categories
domain_categories = {
    "University": ["edu", "ac"],
    "Government": ["gov", "mil", "state", "govt", "us", "ca"],
    "Non-Profit": ["org", "ngo"],
    "International Organization": ["int"],
    "UK": ["uk"],
    "India": ["in"],
    "Canada": ["ca"],
    "Australia": ["au"],
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
        category_df = df[df['Company'].str.contains('|'.join(keywords), case=False, na=False) | df['Email address'].apply(lambda x: categorize_by_domain(x) == category if pd.notna(x) else False)]
    else:  # Handle the "other" category
        known_keywords = [item for sublist in categories.values() for item in sublist]
        category_df = df[~df['Company'].str.contains('|'.join(known_keywords), case=False, na=False)]
        known_domains = [item for sublist in domain_categories.values() for item in sublist]
        category_df = category_df[~category_df['Email address'].apply(lambda x: categorize_by_domain(x) in domain_categories if pd.notna(x) else False)]

    # Define the output path for the category
    output_path = os.path.join(output_dir, f'{category}_contacts.xlsx')

    # Save the filtered DataFrame to a new Excel file
    category_df.to_excel(output_path, index=False)
    print(f"Filtered contacts for {category} saved to {output_path}")

print("All categories processed and saved.")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions to enhance this project! Please create a pull request with detailed descriptions of your changes.

## Issues

If you encounter any issues or have suggestions, please open an issue on GitHub.

---

Thank you for using Contact Categorizer! We hope it helps you manage your contacts more efficiently.
