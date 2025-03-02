
import pandas as pd
import openpyxl
import sys
import os

# Get the absolute path of the project root (one level up from WebScraping)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

from Utilities import FDA



# Declare file
download = pd.read_excel(r"C:\Users\bvlma\PycharmProjects\PharmacyLicenseBank\Data\FDA_503B\503B_2025-03-01.xlsx", dtype=str)

# Clean File
cleaned_503b = FDA.clean_fda_503b_list(download)