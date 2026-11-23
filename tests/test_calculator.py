from src.core.calculator_engine import CalculatorEngine


def test_basic_addition():

    engine = CalculatorEngine()

    assert engine.calculate(
        "2 + 3"
    ) == "5"


def test_multiplication():

    engine = CalculatorEngine()

    assert engine.calculate(
        "6 × 7"
    ) == "42"


def test_power():

    engine = CalculatorEngine()

    assert engine.calculate(
        "2^3"
    ) == "8"


def test_square_root():

    engine = CalculatorEngine()

    assert engine.calculate(
        "sqrt(25)"
    ) == "5"


def test_factorial():

    engine = CalculatorEngine()

    assert engine.calculate(
        "5!"
    ) == "120"


def test_degree_sine():

    engine = CalculatorEngine()

    engine.set_angle_mode(
        "DEG"
    )

    assert engine.calculate(
        "sin(30)"
    ) == "0.5"


def test_degree_cosine():

    engine = CalculatorEngine()

    engine.set_angle_mode(
        "DEG"
    )

    assert engine.calculate(
        "cos(60)"
    ) == "0.5"


def test_degree_tangent():

    engine = CalculatorEngine()

    engine.set_angle_mode(
        "DEG"
    )

    assert engine.calculate(
        "tan(45)"
    ) == "1"


def test_log():

    engine = CalculatorEngine()

    assert engine.calculate(
        "log10(100)"
    ) == "2"


def test_ln():

    engine = CalculatorEngine()

    assert engine.calculate(
        "ln(e)"
    ) == "1"


def test_percentage():

    engine = CalculatorEngine()

    assert engine.calculate(
        "50%"
    ) == "0.5"


def test_division_by_zero():

    engine = CalculatorEngine()

    result = engine.calculate(
        "10 / 0"
    )

    assert result.startswith(
        "Error"
    )