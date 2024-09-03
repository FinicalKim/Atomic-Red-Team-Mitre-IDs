import requests
from bs4 import BeautifulSoup
import re
import sys

def extract_ids_from_page(url):
    try:
        # Fetch the content from the URL using an HTTP GET request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        page_content = response.text  # Get the content of the page as text
        
        # Parse the HTML content with BeautifulSoup to make it easier to navigate
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # Find all tables on the page; technique data is usually stored in a table
        tables = soup.find_all('table')
        
        # Regular expression to match MITRE ATT&CK technique IDs
        # Pattern explanation:
        # ^T\d{4}(\.\d{3})?$ 
        # - ^T: Start with "T"
        # - \d{4}: Followed by exactly 4 digits
        # - (\.\d{3})?: Optionally followed by a period and exactly 3 digits
        # - $: End of the string
        technique_pattern = re.compile(r'^T\d{4}(\.\d{3})?$')
        
        technique_ids = []  # List to store the extracted technique IDs
        
        # Iterate over each table to find the correct one containing the technique data
        for table in tables:
            # Check if the table header contains 'ID', which indicates technique data
            headers = table.find_all('th')
            if headers and any('ID' in header.get_text() for header in headers):
                # Debug print to confirm we're looking at the right table
                print(f"Correct table found with headers: {[header.get_text() for header in headers]}")
                
                # Extract rows from the table
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) > 1:  # Ensure there are enough cells in the row
                        # Extract the technique ID (e.g., "T1087")
                        technique_id = cells[1].get_text().strip()
                        # Extract the sub-technique ID if present and valid (e.g., ".002")
                        sub_technique_id = cells[2].get_text().strip() if len(cells) > 2 and cells[2].get_text().strip().startswith('.') else ''
                        # Combine the technique ID with the sub-technique ID
                        full_id = technique_id + sub_technique_id
                        # Only add IDs that match the expected format
                        if technique_pattern.match(full_id):
                            technique_ids.append(full_id)
        
        return technique_ids  # Return the list of valid technique IDs
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch content from URL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if the script was run with exactly one argument (the URL)
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)
    
    # Get the URL from the first argument provided in the command line
    url = sys.argv[1]
    
    # Extract technique IDs from the provided URL
    extracted_ids = extract_ids_from_page(url)
    
    # Print the extracted IDs if any are found
    if extracted_ids:
        print("Extracted Technique IDs:")
        for tid in extracted_ids:
            print(tid)
    else:
        print("No Technique IDs found.")
