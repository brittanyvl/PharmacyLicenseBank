"""
This module contains functions related to the FDA 503B Outsourcing Facility Export available at
https://www.fda.gov/drugs/human-drug-compounding/registered-outsourcing-facilities

"""

import os
import time
import shutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.webdriver import Options
from webdriver_manager.chrome import ChromeDriverManager

def download_current_503b_list(download_path: str, target_path: str):
    # Set up download preferences
    options = Options()
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Navigate to the URL
        driver.get("https://www.fda.gov/drugs/human-drug-compounding/registered-outsourcing-facilities")
        time.sleep(5)  # Wait for the page to load

        # Select "All" from the dropdown
        select_element = driver.find_element(By.NAME, "DataTables_Table_0_length")
        select = Select(select_element)
        select.select_by_value("-1")
        time.sleep(2)  # Allow table to update

        # Click the export button
        export_button = driver.find_element(By.CLASS_NAME, "buttons-excel")
        export_button.click()

        # Wait for download to complete
        time.sleep(10)  # Adjust based on download speed

        # Identify the latest downloaded file
        downloaded_files = [f for f in os.listdir(download_path) if f.endswith(".xlsx")]
        if not downloaded_files:
            raise FileNotFoundError("No Excel file found in the downloads folder.")

        latest_file = max([os.path.join(download_path, f) for f in downloaded_files], key=os.path.getctime)

        # Rename and move the file
        today_date = datetime.today().strftime('%Y-%m-%d')
        new_filename = f"503B_{today_date}.xlsx"
        target_file_path = os.path.join(target_path, new_filename)

        if os.path.exists(target_file_path):
            os.remove(target_file_path)  # Overwrite existing file

        shutil.move(latest_file, target_file_path)

    finally:
        driver.quit()

    print(f"File saved as {target_file_path}")



