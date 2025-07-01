from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import subprocess

import pandas as pd

import time

# Set target url here (omit in github)
TARGET_URL = "https://example.edu/search"
# f - fall, u - summer, s - spring
terms_to_scrape  = ["term_10s"]

def scrape_data_for_term(term):
    # restart the driver every once in a while to prevent bot detection
    num_search_before_reload = 20

    def start_search(driver, term_value, class_prefix_num):
        global course_names

        term_select = driver.find_element(By.ID, "combobox_term")
        term_select_object = Select(term_select)
        term_select_object.select_by_value(term_value)

        class_prefixes = driver.find_element(By.ID, "combobox_cp")
        class_prefix_options = []
        for class_prefix in class_prefixes.find_elements(By.TAG_NAME, "option"):
            # Make sure text is not blank
            if class_prefix.text:
                class_prefix_options.append(class_prefix.text)
        course_names = class_prefix_options

        select_object = Select(class_prefixes)
        select_object.select_by_visible_text(class_prefix_options[class_prefix_num])

        other_options = driver.find_element(By.ID, "combobox_other")
        select_object_other = Select(other_options)
        select_object_other.select_by_visible_text("Has an Evaluation")

        search_tab = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        search_tab.click()

    headers = ['Term', 'Class Section', 'Title', 'Instructor', 'Schedule']
    data_rows = []

    # there are 134 class prefix options
    for session_num in range(134 // num_search_before_reload + 1):
        chrome_options = Options()
        chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36')
        chrome_options.add_argument("--headless")

        # add header to make it seem more human
        driver = webdriver.Chrome(options=chrome_options)

        wait = WebDriverWait(driver, 10)

        driver.get(TARGET_URL)

        print(f"Session {session_num+1} starting...")
        time.sleep(5)

        for i in range(session_num*num_search_before_reload, min(134, (session_num+1)*num_search_before_reload)):
            # sleep so it doesn't spam requests
            time.sleep(3)

            # f - fall, u - summer, s - spring
            start_search(driver, term, i)

            try:
                table_first_row = wait.until(EC.presence_of_element_located((By.ID, 'r-1')))
            except:
                # sometimes there's no classes found for a specific search
                print(f"No classes found for {course_names[i]}")
                continue

            # get the parent
            tbody = table_first_row.find_element(By.XPATH, "..")
            tbody_children = tbody.find_elements(By.XPATH, './tr')
            
            # just for debug information
            num_rows_added = 0

            for table_row in tbody_children:
                table_column = 0
                row_children = table_row.find_elements(By.XPATH, "./td")
                important_data = []
                for table_cell in row_children:
                    # 0 - term, 1 - class section, 3 - title, 4 - instructor, 5 - schedule
                    if table_column in [0, 1, 3, 4, 5]:
                        important_data.append(table_cell.text)
                    table_column += 1
                data_rows.append(important_data)
                num_rows_added += 1
            
            print(f"{num_rows_added} classes found for {course_names[i]}")

        driver.quit()

    df = pd.DataFrame(data_rows, columns=headers)
    df.to_csv(term + "_scraped_data.csv", index=False)

for term in terms_to_scrape:
    scrape_data_for_term(term)
    # sleepy sleepy
    time.sleep(1600)