import pandas as pd
import SymPy as sp


def load_csv_data(file_path: str) -> pd.DataFrame:
    """
    Load roller coaster data from a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file containing roller coaster data.

    Returns:
    pd.DataFrame: A DataFrame containing the roller coaster data.
    """
    df = pd.read_csv(file_path)
    df_columns = set(df.columns)
    required_columns = {"formula", "start_x", "end_x"}
    missing_columns = required_columns - df_columns
    
    try:
        if not required_columns.issubset(df_columns):
            print(f"Missing column(s): {missing_columns}")
            return pd.DataFrame()
        return df    
    except FileNotFoundError:
        print(f"Invalida file path.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print("The file is empty.")
        return pd.DataFrame()
    except pd.errors.ParserError:
        print("Error parsing the file.")
        return pd.DataFrame()

def create_segments(df: pd.DataFrame) -> list:
    # loop through each row of df
    # df = load_csv_data(csvPath)
    # only run the following loop when df is truthy
    for index, row in df.iterrows():
        formula = row["formula"]
        start_x = row["start_x"]
        end_x = row["end_x"]
    
