import requests
import json
from concurrent.futures import ThreadPoolExecutor

# Define Base URL
BASE_URL = "https://api.elsevier.com/content/search/scopus"

# API keys
api_keys = [
    #api
]

# List of subject abbreviations
subject_abbreviations = [
    "MULT", "AGRI", "ARTS", "BIOC", "BUSI", "CENG", "CHEM", "COMP", "DECI", "EART",
    "ECON", "ENER", "ENGI", "ENVI", "IMMU", "MATE", "MATH", "MEDI", "NEUR", "NURS",
    "PHAR", "PHYS", "PSYC", "SOCI", "VETE", "DENT", "HEAL"
]

# Function to fetch research articles for a specific year and subject area
def fetch_research(year, abbrev, total_results=20, results_per_request=20, api_key=""):
    results = []
    for start in range(0, total_results, results_per_request):
        headers = {
            "Accept": "application/json",
            "X-ELS-APIKey": api_key
        }
        params = {
            "query": f"PUBYEAR = {year} AND SUBJAREA({abbrev})",
            "count": results_per_request,
            "start": start,
            "sort": "-date"  # Sort by date (oldest to newest)
        }
        try:
            response = requests.get(BASE_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            entries = data.get("search-results", {}).get("entry", [])
            results.extend(entries)
            print(f"Fetched {len(entries)} articles for {abbrev} starting at index {start}. Total: {len(results)}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {abbrev} at start {start}: {e}")
            break
    return abbrev, results[:total_results]

# Function to parallelize fetching across abbreviations and API keys
def fetch_all_subjects(year, abbreviations, total_results=20):
    results = {}
    with ThreadPoolExecutor(max_workers=len(api_keys)) as executor:
        futures = []
        for i, abbrev in enumerate(abbreviations):
            api_key = api_keys[i % len(api_keys)]  # Rotate through API keys
            futures.append(executor.submit(fetch_research, year, abbrev, total_results, 20, api_key))
        for future in futures:
            abbrev, data = future.result()
            results[abbrev] = data
    return results

# Fetch data for the year 2024
year = 2024
all_results = fetch_all_subjects(year, subject_abbreviations, total_results=20)

# Save data to JSON file
output_file = "scopus_20_search.json"
with open(output_file, "w") as f:
    json.dump(all_results, f, indent=4)

print(f"Data saved to {output_file}. Total abbreviations processed: {len(subject_abbreviations)}")
