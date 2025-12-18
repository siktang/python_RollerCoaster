import sympy as sp
import pandas as pd
import pytest

from roller_coaster import (
    validate_formula,
    validate_ending,
    validate_x_continuity,
    validate_y_continuity,
    validate_smoothness,
    create_segments,
    load_csv_data
)

def test_load_csv_data(tmp_path, capsys):
    # Case: valid data 
    mock_csv = """formula,start_x,end_x
x**2,0,2
2*x,2,4
"""
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text(mock_csv)

    df = load_csv_data(str(csv_file))

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["formula", "start_x", "end_x"]
    assert len(df) == 2

    # Case: missing column
    mock_invalid_csv = """formula,start_x
x**2,0
2*x,2
"""

    invalid_csv_file = tmp_path / "invalid.csv"
    invalid_csv_file.write_text(mock_invalid_csv)

    invalid_df = load_csv_data(str(invalid_csv_file))

    captured_invalid = capsys.readouterr()

    assert invalid_df.empty
    assert "Missing column(s)" in captured_invalid.out

    # Case: empty file
    empty_csv_file = tmp_path / "empty.csv"
    empty_csv_file.write_text("")

    empty_df = load_csv_data(str(empty_csv_file))

    captured_empty = capsys.readouterr()

    assert empty_df.empty
    assert "File is empty." in captured_empty.out

def test_create_segments(): 
    sample_data = [
        {"formula": "x**2", "start_x": "0", "end_x": "2"},
        {"formula": "x + 1", "start_x": "2", "end_x": "4"}
    ]

    sample_df = pd.DataFrame(sample_data)

    sample_segments = create_segments(sample_df)

    assert len(sample_segments) == 2

    for seg in sample_segments:
        assert isinstance(seg[0], sp.Basic)
        assert isinstance(seg[1], (int, float, sp.Expr))
        assert isinstance(seg[2], (int, float, sp.Expr))

    x = sp.symbols("x")
    formula1 = sample_segments[0][0]
    assert formula1.subs(x, 1) == 1

def test_validate_formula():
    assert validate_formula(sp.sympify("x**3 + 3")) is True
    assert validate_formula(sp.sympify("sin(x)")) is True
    assert validate_formula(sp.sympify("7")) is True
    assert validate_formula(sp.sympify("x + y")) is False

def test_validate_ending():
    assert validate_ending(0, 5) is True
    assert validate_ending(3, 3) is False
    assert validate_ending(5, 2) is False

def test_validate_x_continuity():
    assert validate_x_continuity(2, 2) is True
    assert validate_x_continuity(2, 3) is False

def test_validate_y_continuity():
    formula1 = sp.sympify("x**2")
    formula2 = sp.sympify("x+2")

    assert validate_y_continuity(formula1, formula2, 2, 2) is True
    assert validate_y_continuity(formula1, formula2, 3, 3) is False

def test_validate_smoothness():
    formula1 = sp.sympify("x**2")
    formula2 = sp.sympify("2*x")

    assert validate_smoothness(formula1, formula2, 1, 1) is True
    assert validate_smoothness(formula1, formula2, 2, 2) is False



