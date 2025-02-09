import sys
import os

# Add the Utilities folder to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Utilities')))

import FDA
import pandas as pd
import openpyxl

download = pd.read_excel(r"C:\Users\bvlma\PycharmProjects\PharmacyLicenseBank\Data\FDA_503B\503B_2025-02-09.xlsx",
                       dtype=str)

cleaned_503b = FDA.clean_fda_503b_list(download)
