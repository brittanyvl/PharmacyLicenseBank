
import pandas as pd
import openpyxl
import sys
import os

# Get the absolute path of the project root (one level up from WebScraping)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

from Utilities import FDA



# Declare file
download = pd.read_excel(r"C:\Users\bvlma\PycharmProjects\PharmacyLicenseBank\Data\FDA_503B\503B_2025-03-22.xlsx", dtype=str)
target_path = r"C:\Users\bvlma\PycharmProjects\503BWatch\Data\FDA_503B"

# Clean File
cleaned_503b = FDA.clean_fda_503b_list(download)


# Save the file
saved = FDA.save_clean_503B_list(cleaned_503b, target_path)
