from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time


# Function to wait for an element to appear
def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


# Function to wait for all elements to appear
def wait_for_elements(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((by, value))
    )


# Set up the Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Define the country and year range
# Load the CSV file containing affiliations
country = pd.read_csv(
    r"C:\Users\Asus\CEDT-DSDE-Project-2024\Affiliationresult_country.csv"
)  # Update the path
countries = country["affiliation-country"].tolist()  # Replace with your column name

year_range = range(2018, 2025)
data = []

try:
    for country in countries:
        # Open the Scopus page
        driver.get("https://www.scopus.com/search/form.uri?display=basic#basic")
        wait_for_element(driver, By.CLASS_NAME, "Select-module__vDMww", timeout=15)

        # Select "Affiliation country" from the dropdown
        dropdown = Select(driver.find_element(By.CLASS_NAME, "Select-module__vDMww"))
        dropdown.select_by_visible_text("Affiliation country")

        # Enter the country in the affiliation search bar
        affiliation_search = wait_for_element(
            driver, By.XPATH, '//*[@id="pendo-main-search-bar"]/div/div/label/input'
        )
        affiliation_search.clear()
        affiliation_search.send_keys(country + Keys.ENTER)
        time.sleep(3)  # Allow results to load

        for year in year_range:
            time.sleep(1)
            year_from = wait_for_element(
                driver,
                By.XPATH,
                '//*[@id="year-section"]/div/div/div/div[2]/div/div[2]/div/div/div/div/div[1]/div/label/input',
            )
            year_from.clear()
            year_from.send_keys(str(year))

            year_to = wait_for_element(
                driver,
                By.XPATH,
                '//*[@id="year-section"]/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/label/input',
            )
            year_to.clear()
            year_to.send_keys(Keys.CONTROL + "a")  # Select all text
            year_to.send_keys(Keys.BACKSPACE)  # Clear existing value
            year_to.send_keys(str(year))  # Set new value

            # Click "Apply" for the year range
            button_year = wait_for_element(
                driver,
                By.XPATH,
                '//*[@id="year-section"]/div/div/div/div[2]/div/div[2]/button',
            )
            button_year.click()

            # Open the subject area filter
            subject_all = wait_for_element(
                driver, By.XPATH, '//*[@id="subject-area-section"]/div/div/div/button'
            )
            subject_all.click()

            # Wait for the Subject Area section to load
            subject_area_section = wait_for_element(
                driver,
                By.XPATH,
                '//div[@data-testid="facet-group-subject-area"]',
            )

            # Locate all subject rows within the Subject Area section
            subject_rows = subject_area_section.find_elements(
                By.XPATH, './/label[@class="Checkbox-module__jE3jb"]'
            )
            print(f"Found {len(subject_rows)} subject rows.")

            time.sleep(5)
            # Extract Subject Area and Number of Documents
            for row in subject_rows:
                try:
                    subject_name = row.find_element(
                        By.XPATH,
                        './/span[contains(@class, "Typography-module__Nfgvc")]',
                    ).text
                    document_count = row.find_element(
                        By.XPATH, './/span[@aria-label="documents"]'
                    ).text
                    data.append(
                        {
                            "Country": country,
                            "Year": year,
                            "Subject Area": subject_name,
                            "Number of Documents": document_count,
                        }
                    )
                except Exception as e:
                    print(f"Error extracting data for {country}, {year}: {e}")

            print(f"Data for {country}, {year} collected successfully!")
            ClosePopup = wait_for_element(
                driver,
                By.XPATH,
                '//*[@id="container"]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[1]/div[2]/div/div[2]/div/div[14]/div/div/section/header/button/span[1]',
            ).click()
            print(f"Close popup {country}, {year}")

            reset_year = wait_for_element(
                driver,
                By.XPATH,
                '//*[@id="container"]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/button/span',
            )
            reset_year.click()

    # Save data to a CSV file
    df = pd.DataFrame(data)
    output_path = r"C:\Users\Asus\CEDT-DSDE-Project-2024\scopus_multiple_countries_years_top_five.csv"
    df.to_csv(output_path, index=False)
    print(f"All data exported successfully to {output_path}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
