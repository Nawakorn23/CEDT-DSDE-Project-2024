import json
import pandas as pd

# Input and output file paths
input_file = "scopus_20_search.json"
output_file = "scopus_20_search.csv"

# Load the JSON data
with open(input_file, "r") as file:
    data = json.load(file)

# Prepare the data for CSV export with specified fields
rows = []
for subject, articles in data.items():
    for article in articles:
        affiliations = article.get("affiliation", [])
        if len(affiliations) == 1:
            # Single affiliation: keep one record
            rows.append({
                "Subject": subject,
                "URL": article.get("prism:url"),
                "Identifier": article.get("dc:identifier"),
                "EID": article.get("eid"),
                "Title": article.get("dc:title"),
                "Creator": article.get("dc:creator"),
                "Publication Name": article.get("prism:publicationName"),
                "Publication Date": article.get("prism:coverDate"),
                "DOI": article.get("prism:doi"),
                "Cited By Count": article.get("citedby-count"),
                "Affiliation Name": affiliations[0].get("affilname"),
                "Affiliation City": affiliations[0].get("affiliation-city"),
                "Affiliation Country": affiliations[0].get("affiliation-country")
            })
        elif len(affiliations) > 1:
            # Multiple affiliations: create separate records for each
            for affiliation in affiliations:
                rows.append({
                    "Subject": subject,
                    "URL": article.get("prism:url"),
                    "Identifier": article.get("dc:identifier"),
                    "EID": article.get("eid"),
                    "Title": article.get("dc:title"),
                    "Creator": article.get("dc:creator"),
                    "Publication Name": article.get("prism:publicationName"),
                    "Publication Date": article.get("prism:coverDate"),
                    "DOI": article.get("prism:doi"),
                    "Cited By Count": article.get("citedby-count"),
                    "Affiliation Name": affiliation.get("affilname"),
                    "Affiliation City": affiliation.get("affiliation-city"),
                    "Affiliation Country": affiliation.get("affiliation-country")
                })
        else:
            # No affiliations: single record with None for affiliation fields
            rows.append({
                "Subject": subject,
                "URL": article.get("prism:url"),
                "Identifier": article.get("dc:identifier"),
                "EID": article.get("eid"),
                "Title": article.get("dc:title"),
                "Creator": article.get("dc:creator"),
                "Publication Name": article.get("prism:publicationName"),
                "Publication Date": article.get("prism:coverDate"),
                "DOI": article.get("prism:doi"),
                "Cited By Count": article.get("citedby-count"),
                "Affiliation Name": None,
                "Affiliation City": None,
                "Affiliation Country": None
            })

# Convert to DataFrame
df = pd.DataFrame(rows)

# Save to CSV
df.to_csv(output_file, index=False)

print(f"JSON data successfully converted to CSV and saved to {output_file}")
