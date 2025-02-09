import pandas as pd
import PharmacyBank
from PharmacyBank import data_loader

data = data_loader.load_data()

# Create Data for Metrics at top of the home page
metric_total_pharmacies = len(data)

# Round the percentage metrics to 2 decimal places
metric_percent_fda_uninspected = round((data['no_fda_inspections'].mean()) * 100, 2)
metric_percent_483s_issued = round((data['form_483_issued'].mean()) * 100, 2)
metric_percent_recalls_conducted = round((data['fda_recall_conducted'].mean()) * 100, 2)
metric_percent_intend_sterile = round((data['intends_to_compound_sterile'].mean()) * 100, 2)


