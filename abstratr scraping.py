from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    JavascriptException
)
import csv
import time

# Specify the path to chromedriver using a Service object
s = Service(r'C:\Users\Hemlani\Documents\Research Position\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get('http://abstrackr.cebm.brown.edu/account/login')

username_field = driver.find_element(By.ID, 'login')
password_field = driver.find_element(By.ID, 'password')
login_button = driver.find_element(By.ID, 'submit')

username_field.send_keys('phemlani1')
password_field.send_keys('DXMeCgH#RjwA3wP')

login_button.click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'login-header'))
)

project_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'screen/53929')]"))
)
project_link.click()

csv_file = open('scraped_data.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['Title', 'ID', 'Abstract'])


try:
    while True:
        # Find the citation div by its ID
        citation_div = driver.find_element(By.ID, 'citation')
        citation_text = citation_div.text

        # Scrape the ID
        try:
            id_element = driver.find_element(By.ID, 'cur_citation_id')
            id = id_element.text
        except NoSuchElementException:
            id = "ID not found"

        # Extract the title text
        try:
            title_element = citation_div.find_element(By.TAG_NAME, 'h2')
            title = title_element.text
        except NoSuchElementException:
            title = "Title not found"

        # Split the citation text into lines and find the abstract
        lines = citation_text.split("\n")
        # ... (Your existing logic for extracting the abstract goes here) ...
        # Assuming `citation_div` is already located
        citation_text = citation_div.text
        lines = citation_text.split("\n")

        # Find the line with the authors and the line with the keywords
        authors_line_index = None
        keywords_line_index = None

        for i, line in enumerate(lines):
            if "Authors:" in line:
                authors_line_index = i
            elif "Keywords:" in line:
                keywords_line_index = i
                break  # Stop the loop once we find the keywords line

        # The abstract should be between the authors and the keywords
        abstract_start_index = authors_line_index + 1 if authors_line_index is not None else None
        abstract_end_index = keywords_line_index if keywords_line_index is not None else None

        # Check if we've found the abstract's start and end lines
        if abstract_start_index is not None and abstract_end_index is not None and abstract_start_index < abstract_end_index:
            # Extract the abstract by joining the lines from start to end index
            abstract = " ".join(lines[abstract_start_index:abstract_end_index]).strip()
        else:
            # If something goes wrong, log an appropriate message
            abstract = "Abstract not found or format is unexpected."

# Write the scraped data into the CSV file
        writer.writerow([title, id, abstract])

        # Logic to navigate to the next citation goes here
        def click_element(element):
            try:
                # First strategy: Wait for the primary element to be clickable and then click
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'maybe'))
                )
                element.click()
                print("Clicked primary element using WebDriverWait.")
            except ElementClickInterceptedException as e1:
                if alternative_element_id:
                    # If the primary element click is intercepted, try the alternative element
                    try:
                        alternative_element = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, 'accept'))
                        )
                        alternative_element.click()
                        print("Clicked alternative element due to interception.")
                    except Exception as alt_e:
                        print(f"Error clicking alternative element: {alt_e}")
                else:
                    print("Primary element click intercepted, no alternative element ID provided.")
                    raise e1
            except StaleElementReferenceException:
                # If a stale element reference exception is caught, try to find the element again
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'maybe'))
                )
                element.click()
                print("Clicked after handling stale element reference.")
            except JavascriptException as e2:
                try:
                    # Second strategy: JavaScript click
                    driver.execute_script("arguments[0].click();", element)
                    print("Clicked using JavaScript.")
                except Exception as e3:
                    # If all strategies fail, log the errors
                    print("Failed to click using all strategies.")
                    print(f"Error with JavaScript click: {e2}")
                    print(f"Final exception: {e3}")
            except Exception as e:
                # Catch all other exceptions
                print(f"An unexpected error occurred: {e}")
        click_element('maybe')


except Exception as e:
    print("An error occurred:", e)
finally:
    # Close the CSV file and the WebDriver
    csv_file.close()
