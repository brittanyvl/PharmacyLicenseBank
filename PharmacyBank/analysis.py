import pandas as pd

def calculate_average_age(data: pd.DataFrame):
    return data["Age"].mean()
