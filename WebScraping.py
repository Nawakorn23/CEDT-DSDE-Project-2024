from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set up the Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Open the Scopus page
driver.get("https://www.scopus.com/search/form.uri?display=basic#basic")
time.sleep(5)

# Search for affiliation
affiliation_field = driver.find_element(By.ID, "affiliation")
affiliation_field.click()
time.sleep(1)

affiliation_search = driver.find_element(
    By.ID, "scopus-homepage__affiliations_search_input-input"
)
affiliation_search.send_keys("Harvard Medical School")
time.sleep(1)

affiliation_go = driver.find_element(
    By.XPATH, '//*[@id="scopus-homepage__affiliations_search_input-suggestions"]/li[1]'
)
affiliation_go.click()
time.sleep(5)

# Extract document and author count
document_count = driver.find_element(
    By.XPATH,
    '//*[@id="main"]/div/section/div/div/div[1]/div/header/div/section/div/div[1]/div/div/div/div[1]/a/span/span',
).text
author_count = driver.find_element(
    By.XPATH,
    '//*[@id="main"]/div/section/div/div/div[1]/div/header/div/section/div/div[2]/div/div/div/div[1]/a/span/span',
).text

# Extract organization name and address
organization_name = driver.find_element(
    By.XPATH,
    "//*[@id='main']/div/section/div/div/div[1]/div/header/div/div[1]/div[1]/h1",
).text
organization_address = driver.find_element(
    By.XPATH, "//span[@data-testid='org-address']"
).text

# Locate the table containing subject area and document count
rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

# Extract data into a list of dictionaries
data = []
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) > 1:  # Ensure it's a valid row with data
        subject_area = cells[0].text
        document_count = cells[1].text
        data.append(
            {
                "Organization": organization_name,
                "Address": organization_address,
                "Subject Area": subject_area,
                "Documents": document_count,
            }
        )

# Convert to DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv(r"C:\DSDE Project\scopus_subject_areas_with_trends.csv", index=False)

print("Data exported successfully!")
