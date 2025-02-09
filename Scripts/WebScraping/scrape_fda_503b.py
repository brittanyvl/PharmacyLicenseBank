from Utilities import FDA

download_path = r"C:\Users\bvlma\Downloads"
target_path = r"C:\Users\bvlma\PycharmProjects\PharmacyLicenseBank\Data\FDA_503B"

# Download the latest FDA outsourcing list
FDA.download_current_503b_list(download_path, target_path)

