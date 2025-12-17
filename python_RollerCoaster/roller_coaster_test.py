import sympy as sp

from roller_coaster import (
    validate_formula,
    validate_ending,
    validate_x_continuity,
    validate_y_continuity,
    validate_smoothness,
    create_segments
)

def test_validate_formula():
    assert validate_formula(sp.sympify("x**3 + 3")) is True
    assert validate_formula(sp.sympify("sin(x)")) is True
    assert validate_formula(sp.sympify("7")) is True
    assert validate_formula(sp.sympify("x + y")) is False