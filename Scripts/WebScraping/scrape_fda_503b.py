import sys
import os

# Get the absolute path of the project root (one level up from WebScraping)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

from Utilities import FDA

download_path = r"C:\Users\bvlma\Downloads"
target_path = r"C:\Users\bvlma\PycharmProjects\PharmacyLicenseBank\Data\FDA_503B"

# Download the latest FDA outsourcing list
FDA.download_current_503b_list(download_path, target_path)

