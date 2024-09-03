MITRE ATT&CK Technique ID Extractor
Overview
This Python script is designed to extract MITRE ATT&CK technique IDs from a given webpage, specifically from the MITRE ATT&CK framework's group pages. The script parses the HTML content of the page, locates the table containing technique information, and extracts both technique and sub-technique IDs (if available).

Requirements
Python 3.x
requests library
beautifulsoup4 library
Installation of Required Libraries
You can install the required Python libraries using pip:

bash
Copy code
pip install requests beautifulsoup4
Usage
Download or Clone the Repository:

Ensure you have the script file (extract_technique_ids.py) in your working directory.
Run the Script:

The script takes one command-line argument, the URL of the MITRE ATT&CK group page from which you want to extract technique IDs.
Example usage:

bash
Copy code
python extract_technique_ids.py "https://attack.mitre.org/groups/G1017/"
Output:

The script will print the extracted technique IDs to the console. Only valid MITRE ATT&CK IDs following the format Txxxx or Txxxx.xxx will be included.
How It Works
Fetch the Webpage:

The script uses the requests library to fetch the HTML content of the provided URL.
Parse the HTML:

It then uses BeautifulSoup to parse the HTML content and locate the table containing the technique data.
Extract Technique IDs:

The script identifies rows in the table where technique IDs are present, combining the main technique ID with any sub-technique IDs (e.g., T1087.002).
It uses a regular expression to ensure that only valid IDs are extracted.
Output:

The script prints out the extracted technique IDs in a clean format.
Example Output
If run against the URL https://attack.mitre.org/groups/G1017/, the script might output:

python
Copy code
Extracted Technique IDs:
T1087.002
T1560.001
T1059.001
...
Troubleshooting
No IDs Found: Ensure the URL is correct and points to a MITRE ATT&CK group page with a valid table containing technique data.
Unwanted Text: The script uses a regular expression to filter out non-technique text, but page structure changes might require adjustments to the script.
Contributing
Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvement.

License
This project is licensed under the MIT License - see the LICENSE file for details.
