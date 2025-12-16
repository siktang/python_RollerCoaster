import pandas as pd
import sympy as sp
import sys

x = sp.symbols('x')

def load_csv_data(file_path: str) -> pd.DataFrame:
    """
    Returns a dataframe with the input csv data; 
    returns empty dataframe if data is not available or error exists.
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
    '''
    Returns a list of segments in sympy expressions.
    '''

    # loop through each row of df
    # df = load_csv_data(csvPath)
    # only run the following loop when df is truthy
    segments = []

    for _, row in df.iterrows():
        formula = sp.sympify(row["formula"])
        start_x = sp.sympify(row["start_x"])
        end_x = sp.sympify(row["end_x"])
        segments.append((formula, start_x, end_x))
    
    return segments
    

# validation for each rule
def validate_formula(formula: object) -> bool:
    '''
    Returns true if formula is valid (contains x or no variable) and false if it is not (contains other variables).
    '''
    input_variables = formula.free_symbols
    return input_variables == { x } or input_variables == {}

def validate_ending(start: float, end: float) -> bool: 
    '''
    Returns true if ending is larger than starting, and false otherwise.
    ''' 
    return end > start

def validate_x_continuity(prev_end, current_start): 
    '''
    Returns true if the start point of the current segment matches the end point of previous segment.
    '''
    return prev_end == current_start

def validate_y_continuity(prev_formula, current_formula, prev_end, current_start):
    '''
    Returns true if the values of formula1 and formula2 are the same at x.
    '''
    return prev_formula.subs(x, prev_end) == current_formula.subs(x, current_start)



# then create a function to combine all the above validations to loop through segments
def validate_segments(segments):
    for item in segments: 
        if validate_formula(item[0]) is False: 
            sys.exit('Formula is not valid')
        elif validate_ending(item[1], item[2]) is False: 
            sys.exit('End point must be larger than start point.')
        

    
