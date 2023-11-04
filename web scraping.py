import requests
import xml.etree.ElementTree as ET
import csv

# Define the base URL for ESearch
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# Define your search parameters
params = {
    "db": "pubmed",       # Database to search
    "term": "economics AND covid",     # Your search term
    "retmax": 100,        # Number of results to return
    "usehistory": "y",    # Use history to cache results
}

# Make the request to ESearch
response = requests.get(base_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the XML response
    root = ET.fromstring(response.text)

    # Retrieve PMIDs from the XML response
    pmids = [id_tag.text for id_tag in root.findall("IdList/Id")]

    with open('pmids.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['PMID'])  # Header
        for pmid in pmids:
            writer.writerow([pmid])

    # Print the PMIDs
    print(pmids)
else:
    print(f"Error: {response.status_code}")
