import pandas as pd
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import sys

x = sp.symbols('x')

# File parsing
def load_csv_data(file_path: str) -> pd.DataFrame:
    """
    Returns a dataframe with the input csv data; 
    returns empty dataframe if data is not available or error exists.
    """    
    try:
        df = pd.read_csv(file_path)
        df_columns = set(df.columns)
        required_columns = {"formula", "start_x", "end_x"}
        missing_columns = required_columns - df_columns
        
        if not required_columns.issubset(df_columns):
            print(f"Missing column(s): {missing_columns}")
            return pd.DataFrame()
        return df  
      
    except FileNotFoundError:
        print(f"Invalida file path.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print("File is empty.")
        return pd.DataFrame()
    except pd.errors.ParserError:
        print("Error parsing the file.")
        return pd.DataFrame()

def create_segments(df: pd.DataFrame) -> list:
    '''
    Returns a list of segments in sympy expressions.
    '''
    segments = []

    for _, row in df.iterrows():
        formula = sp.sympify(row["formula"])
        start_x = sp.sympify(row["start_x"])
        end_x = sp.sympify(row["end_x"])
        segments.append((formula, start_x, end_x))
    
    return segments
    

# Validation for each rule
def validate_formula(formula: object) -> bool:
    '''
    Returns true if formula is valid (contains x or no variable) and false if it is not (contains other variables).
    '''
    input_variables = formula.free_symbols
    return input_variables.issubset({x})

def validate_ending(start: float, end: float) -> bool: 
    '''
    Returns true if ending is larger than starting, and false otherwise.
    ''' 
    return end > start

def validate_x_continuity(prev_end: float, current_start: float): 
    '''
    Returns true if the start point of the current segment matches the end point of previous segment.
    '''
    return prev_end == current_start

def validate_y_continuity(prev_formula: object, current_formula: object, prev_end: float, current_start: float):
    '''
    Returns true if the values of formula1 and formula2 are the same at x.
    '''
    return prev_formula.subs(x, prev_end) == current_formula.subs(x, current_start)

def validate_smoothness(prev_formula: object, current_formula: object, prev_end: float, current_start: float):
    '''
    Returns true if the derivatives are equal at the meeting points between previous and current formulas.
    '''
    return sp.diff(prev_formula, x).subs(x, prev_end) == sp.diff(current_formula, x).subs(x, current_start)


# Combine all the above validations to loop through segments
def validate_segments(segments):
    for item in segments: 
        if not validate_formula(item[0]): 
            sys.exit("Formula is not valid")
        elif not validate_ending(item[1], item[2]): 
            sys.exit("End point must be larger than start point.")
    
    for i in range(1, len(segments)):
        prev_formula, _, prev_end = segments[i-1]
        current_formula, current_start, _ = segments[i]
        if not validate_x_continuity(prev_end, current_start):
            sys.exit("There are gaps in x domains.")
        elif not validate_y_continuity(prev_formula, current_formula, prev_end, current_start):
            sys.exit("Segments are not connecting vertically.")
        elif not validate_smoothness(prev_formula, current_formula, prev_end, current_start):
            sys.exit("The transition is not smooth due to different derivative values.")
    
    return True

# Function to generate graph/svg
def generate_graph(segments, svgFile): 
    plt.figure()

    for item in segments:
        f = sp.lambdify(x, item[0], "numpy")
        xs = np.linspace(float(item[1]), float(item[2]), 300)
        ys = f(xs)
        if np.isscalar(ys):
            ys = np.full_like(xs, ys)
        plt.plot(xs, ys)
    
    plt.ylabel("f(x)")
    plt.savefig(svgFile, format="svg")

def main(): 
    csvFile = input('Enter file path for CSV:')
    svgFile = input('Enter file name for SVG:')

    if not svgFile.lower().endswith(".svg"):
        svgFile += ".svg"

    df = load_csv_data(csvFile)

    if df.empty:
        sys.exit("No data available.")

    segments = create_segments(df)

    validate_segments(segments)
    generate_graph(segments, svgFile)

if __name__ == "__main__":
    main()

        

    
