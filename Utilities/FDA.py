"""
This module contains functions related to the FDA 503B Outsourcing Facility Export available at
https://www.fda.gov/drugs/human-drug-compounding/registered-outsourcing-facilities
"""
import os
import time
import shutil
from datetime import datetime
import numpy as np
import pandas as pd
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

def clean_fda_503b_list(download: pd.DataFrame) -> pd.DataFrame:

    # Create a clean copy to transform
    df = download.copy()

    # Remove non-breaking spaces throughout document
    df = df.applymap(lambda x: x.replace('\u00A0', ' ') if isinstance(x, str) else x)

    # Set the first row as the header
    df.columns = df.iloc[0]

    # Remove the first row from the DataFrame (since it's now the header)
    df = df[1:].reset_index(drop=True)

    # Cast all rows to uppercase for string parsing
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

    # Add commas before "INC", "LLC", and "DBA" if missing
    df['Facility'] = df['Facility'].str.replace(r'(?<![,])\sINC', r', INC', regex=True)
    df['Facility'] = df['Facility'].str.replace(r'(?<![,])\sLLC', r', LLC', regex=True)
    df['Facility'] = df['Facility'].str.replace(r'(?<![,])\sDBA', r', DBA', regex=True)

    # Step 1: Assign pharmacy_legal_entity the first part before the comma
    df['pharmacy_legal_entity'] = df['Facility'].str.split(',').str[0]

    # If ' INC' is found, set "INC"
    df.loc[df['Facility'].str.contains(" INC", na=False), 'pharmacy_entity_type'] = "INC"

    # If ' LLC' is found, set "LLC"
    df.loc[df['Facility'].str.contains(" LLC", na=False), 'pharmacy_entity_type'] = "LLC"

    # Create a pharmacy_name column based on if there is a DBA or not
    df['pharmacy_name'] = df.apply(
    lambda row: row['Facility'].split('DBA')[-1].split(',')[0].replace(" DBA", "").strip()
    if " DBA" in row['Facility'] else row['pharmacy_legal_entity'], axis=1
    )
    # Add the legal entity onto the back of the legal_entity
    df['pharmacy_legal_entity'] = df['pharmacy_legal_entity'].fillna('') + " " + df['pharmacy_entity_type'].fillna('')

    # Identify renamed facilities
    df['is_renamed'] = df['Facility'].str.contains("FORMERLY REGISTERED", na=False)

    # Create 'former_facility_name' column by extracting text after "FORMERLY REGISTERED AS"
    df['former_facility_name'] = np.where(
        df['is_renamed'],
        df['Facility'].str.extract(r'FORMERLY REGISTERED AS (.*)', expand=False),
        np.nan
    )

    # Cut city and state off former facility name
    df['former_facility_name'] = df['former_facility_name'].str.replace(r',\s*[^,]+,[^,]+$', '', regex=True)

    # Function to extract city and state
    def extract_city_state(facility_string):
        parts = facility_string.split(',')
        city = parts[-2].strip()  # Second to last part is the city
        state = parts[-1].strip()  # Last part is the state
        return city, state

    # Apply the function to each row and create new columns
    df[['license_city', 'license_state']] = df['Facility'].apply(lambda x: pd.Series(extract_city_state(x)))

    # Remove any + symbol with blank space
    df['Contact'] = df['Contact'].str.replace('+', '')

    def extract_name_from_503B_contact(column: pd.Series) -> pd.Series:
        return column.str.extract(r'^([^0-9]+)', expand=True)[0]

    def extract_phone_from_503B_contact(column: pd.Series) -> pd.Series:
        return column.str.extract(r'(\d.+)', expand=True)[0]

    df['license_contact_name'] = extract_name_from_503B_contact(df['Contact'])
    df['license_contact_phone'] = extract_phone_from_503B_contact(df['Contact'])

    rename_dict = {
        'Initial Registration Date 1': 'initial_registration_date',
        'Most Recent Registration Date 1': 'most_recent_registration_date',
        'Last Inspection 2' : 'last_fda_inspection_date',
        'Form 483 Issued? 3': 'form_483_issued',
        'Recall Conducted? 9': 'fda_recall_conducted',
        'Action Based on Last Inspection 4,5' : 'post_inspection_action',
        'Intends to Compound Sterile Drugs From Bulk Substances 6' : 'intends_to_compound_sterile',
    }

    df = df.rename(columns = rename_dict)

    # Cast Not Yet Inspected to np.NaN so we can properly coerce to datetime
    df['last_fda_inspection_date'] = df['last_fda_inspection_date'].replace('NOT YET INSPECTED', np.nan)
    df['last_fda_inspection_date'] = pd.to_datetime(df['last_fda_inspection_date'])
    df['no_fda_inspections'] = df['last_fda_inspection_date'].isna()

    # Cast initial_registration_date to datetime
    df['initial_registration_date'] = pd.to_datetime(df['initial_registration_date'])
    df['last_fda_inspection_date'] = pd.to_datetime(df['last_fda_inspection_date'], errors='coerce')

    # Replace N/A with np.NaN for boolean fields
    df['form_483_issued'] = df['form_483_issued'].apply(lambda x: True if x == 'YES' else False)
    df['fda_recall_conducted'] = df['fda_recall_conducted'].apply(lambda x: True if x == 'YES' else False)
    df['intends_to_compound_sterile'] = df['intends_to_compound_sterile'].apply(lambda x: True if x == 'YES' else False)

    # Clean post inspection action column
    df['post_inspection_action'] = df['post_inspection_action'].str.replace('OPEN7', 'OPEN')

    # Extract the date from the 'post_inspection_action' column
    df['post_inspection_action_date'] = df['post_inspection_action'].str.extract(r'(\d{1,2}/\d{1,2}/\d{4})')

    # Remove the date from the 'post_inspection_action' column (if a date exists)
    df['post_inspection_action'] = df['post_inspection_action'].str.replace(r'\s*\d{1,2}/\d{1,2}/\d{4}$', '', regex=True)

    # Cast post_inspectio_action_date to datetime
    df['post_inspection_action_date'] = pd.to_datetime(df['post_inspection_action_date'])


    return df
