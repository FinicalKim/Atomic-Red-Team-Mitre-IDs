import requests
from bs4 import BeautifulSoup
import re
import sys
import subprocess

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
    # Your existing code to get the URL and extract IDs
    # ...

    # Extract technique IDs from the provided URL
    extracted_ids = extract_ids_from_page(url)

    # Check if any IDs were extracted
    if not extracted_ids:
        print("No Technique IDs found.")
        sys.exit(1)

    # Build and execute PowerShell commands for each technique ID
    for tid in extracted_ids:
        # Prepare the PowerShell script as a multi-line string
        powershell_script = f"""
        # Set Execution Policy
        Set-ExecutionPolicy Bypass -Scope Process -Force

        # Function to check if running as Administrator
        function Test-Administrator {{
            [OutputType([bool])]
            param()
            process {{
                [Security.Principal.WindowsPrincipal]$user = [Security.Principal.WindowsIdentity]::GetCurrent();
                return $user.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator);
            }}
        }}

        if(-not (Test-Administrator)) {{
            Write-Error "This script must be executed as Administrator.";
            exit 1;
        }}

        # Import or Install Invoke-AtomicRedTeam Module
        if (Get-Module -ListAvailable -Name Invoke-AtomicRedTeam) {{
            Import-Module Invoke-AtomicRedTeam -Force
        }} else {{
            IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1');
            Install-AtomicRedTeam -getAtomics -Force
            Import-Module Invoke-AtomicRedTeam -Force
        }}

        # Run the Atomic Test for the Technique ID
        Write-Host "Running tests for Technique ID: {tid}"
        Invoke-AtomicTest {tid} -GetPrereqs -Verbose
        Invoke-AtomicTest {tid} -Verbose
        """

        # Execute the PowerShell script
        result = subprocess.run(["powershell", "-NoProfile", "-Command", powershell_script], capture_output=True, text=True)

        # Output the result
        if result.returncode != 0:
            print(f"Error running technique {tid}: {result.stderr}")
        else:
            print(f"Successfully ran technique {tid}:\n{result.stdout}")
