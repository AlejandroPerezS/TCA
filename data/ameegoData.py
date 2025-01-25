
import pandas as pd
from tabulate import tabulate

def load_data(file_path, file_type='csv'):
    """
    Load data from a CSV or Excel file and trim it to specific columns.

    Parameters:
    file_path (str): The path to the file.
    file_type (str): The type of the file ('csv' or 'excel').

    Returns:
    pd.DataFrame: The loaded and trimmed data as a pandas DataFrame.
    """
    final_file_path = "C:/Users/agnia/Downloads/" + file_path
    
    if file_type == 'csv':
        data = pd.read_csv(final_file_path)
    elif file_type == 'excel':
        data = pd.read_excel(final_file_path)
    else:
        raise ValueError("file_type must be either 'csv' or 'excel'")
    
    # Trim the data to specific columns
    columns_to_keep = ['Name','Wage', 'Start', 'End', 'Unpaid Breaks', 'Worked Hrs']
    trimmed_data = data[columns_to_keep]
    
    print(tabulate(trimmed_data, headers='keys', tablefmt='psql'))
    
    return trimmed_data


