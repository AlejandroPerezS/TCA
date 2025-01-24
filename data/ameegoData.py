
import pandas as pd
from tabulate import tabulate

def load_data(file_path, file_type='csv'):
    """
    Load data from a CSV or Excel file.

    Parameters:
    file_path (str): The path to the file.
    file_type (str): The type of the file ('csv' or 'excel').

    Returns:
    pd.DataFrame: The loaded data as a pandas DataFrame.
    """
    final_file_path = "C:/Users/agnia/Downloads/"+file_path
    if file_type == 'csv':
        data = pd.read_csv(final_file_path)
        print(data.head())
    elif file_type == 'excel':
        data = pd.read_excel(final_file_path)
        print(data.head())
    else:
        raise ValueError("file_type must be either 'csv' or 'excel'")
    
    return data

data = load_data('employee_shifts_2025-01-24.csv')
