import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


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

# Load the CSV file containing affiliations
countries_data = pd.read_csv(
    r"C:\Users\Asus\CEDT-DSDE-Project-2024\Affiliationresult_country.csv"
)
countries = countries_data["affiliation-country"].tolist()

year_range = range(2018, 2025)
data = []

output_path = (
    r"C:\Users\Asus\CEDT-DSDE-Project-2024\scopus.csv"
)

# Create or overwrite the output file with headers
pd.DataFrame(columns=["Country", "Year", "Subject Area", "Number of Documents"]).to_csv(
    output_path, index=False
)

try:
    for country in countries:
        print(f"Processing data for country: {country}")
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
            # Set the year range
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

            time.sleep(2)
            # Wait for the modal containing subject areas to load
            subject_area_modal = wait_for_element(
                driver, By.CLASS_NAME, "Modal-module__HdKbm"
            )

            # Locate all subject area labels
            subject_labels = subject_area_modal.find_elements(
                By.XPATH, './/label[contains(@class, "Checkbox-module__jE3jb")]'
            )

            print(f"Found {len(subject_labels)} subject rows.")

            # Extract subject name and document count
            for label in subject_labels:
                try:
                    subject_name = label.find_element(
                        By.XPATH,
                        ".//span[contains(@class, 'Typography-module__Nfgvc')]",
                    ).text
                    document_count = label.find_element(
                        By.XPATH, ".//span[@aria-label='documents']"
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

            # Close the popup
            ClosePopup = wait_for_element(
                driver,
                By.XPATH,
                '//*[@id="container"]/micro-ui/document-search-results-page/div[1]/section[2]/div/div[1]/div[2]/div/div[2]/div/div[14]/div/div/section/header/button/span[1]',
            ).click()
            print(f"Close popup {country}, {year}")
            driver.back()

        # Append the current country's data to the output CSV
        df = pd.DataFrame(data)
        df.to_csv(output_path, mode="a", header=False, index=False)
        print(f"Data for {country} saved successfully!")
        data.clear()  # Clear data for the next country

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
    print("Script execution completed.")
