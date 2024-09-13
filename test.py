import requests
from bs4 import BeautifulSoup
import re
import sys
import subprocess

def extract_ids_from_page(url):
    # Your existing code to extract IDs
    # ...
    return technique_ids  # Return the list of valid technique IDs

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
