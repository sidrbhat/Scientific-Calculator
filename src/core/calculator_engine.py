import re
import sympy as sp

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
    factorial_notation,
)


class CalculatorEngine:
    """Scientific calculator mathematical engine."""

    def __init__(self):
        self.angle_mode = "DEG"

        self.transformations = (
            standard_transformations
            + (
                factorial_notation,
                implicit_multiplication_application,
                convert_xor,
            )
        )

    # ---------------------------------------------------------
    # MAIN CALCULATION
    # ---------------------------------------------------------

    def calculate(self, expression: str) -> str:
        if not expression or not expression.strip():
            return ""

        try:
            prepared = self.prepare_expression(expression)

            result = parse_expr(
                prepared,
                local_dict=self.get_local_dict(),
                transformations=self.transformations,
                evaluate=True,
            )

            # Explicitly detect SymPy's infinity / undefined results
            if result in (
                sp.zoo,
                sp.oo,
                -sp.oo,
                sp.nan,
            ):
                return "Error: Invalid result"

            return self.format_result(result)

        except ZeroDivisionError:
            return "Error: Division by zero"

        except ValueError as error:
            return f"Error: {error}"

        except Exception as error:
            error_text = str(error).lower()

            if "division by zero" in error_text:
                return "Error: Division by zero"

            return "Error: Invalid expression"

    # ---------------------------------------------------------
    # PREPARE EXPRESSION
    # ---------------------------------------------------------

    def prepare_expression(self, expression: str) -> str:
        expression = expression.strip()

        replacements = {
            "×": "*",
            "÷": "/",
            "−": "-",
            "π": "pi",
            "√": "sqrt",
            "x²": "**2",
            "xʸ": "**",
            "sin⁻¹": "asin",
            "cos⁻¹": "acos",
            "tan⁻¹": "atan",
            "eˣ": "exp",
            "10ˣ": "pow10",
        }

        for old, new in replacements.items():
            expression = expression.replace(old, new)

        expression = self.convert_percentages(expression)
        expression = self.convert_angle_functions(expression)

        return expression

    # ---------------------------------------------------------
    # PERCENTAGE
    # ---------------------------------------------------------

    @staticmethod
    def convert_percentages(expression: str) -> str:
        return re.sub(
            r"(\d+(?:\.\d+)?)%",
            r"(\1/100)",
            expression,
        )

    # ---------------------------------------------------------
    # ANGLE MODE
    # ---------------------------------------------------------

    def convert_angle_functions(self, expression: str) -> str:

        # In RAD mode, use normal SymPy trig functions.
        if self.angle_mode == "RAD":
            return expression

        functions = {
            "sin": "sind",
            "cos": "cosd",
            "tan": "tand",
            "asin": "asind",
            "acos": "acosd",
            "atan": "atand",
        }

        for old, new in functions.items():
            pattern = rf"\b{old}\s*\("
            expression = re.sub(
                pattern,
                f"{new}(",
                expression,
            )

        return expression

    # ---------------------------------------------------------
    # SYMPY FUNCTIONS
    # ---------------------------------------------------------

    def get_local_dict(self):

        return {
            # Constants
            "pi": sp.pi,
            "e": sp.E,

            # Basic mathematics
            "sqrt": sp.sqrt,
            "abs": sp.Abs,

            # Logarithms
            "log": sp.log,
            "ln": sp.log,
            "log10": lambda x: sp.log(x, 10),

            # Exponential
            "exp": sp.exp,
            "pow10": lambda x: 10 ** x,

            # Trigonometry
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,

            # Inverse trigonometry
            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,

            # Degree trigonometry
            "sind": lambda x: sp.sin(sp.pi * x / 180),
            "cosd": lambda x: sp.cos(sp.pi * x / 180),
            "tand": lambda x: sp.tan(sp.pi * x / 180),

            # Degree inverse trigonometry
            "asind": lambda x: 180 * sp.asin(x) / sp.pi,
            "acosd": lambda x: 180 * sp.acos(x) / sp.pi,
            "atand": lambda x: 180 * sp.atan(x) / sp.pi,

            # Hyperbolic functions
            "sinh": sp.sinh,
            "cosh": sp.cosh,
            "tanh": sp.tanh,

            # Inverse hyperbolic
            "asinh": sp.asinh,
            "acosh": sp.acosh,
            "atanh": sp.atanh,

            # Rounding
            "floor": sp.floor,
            "ceil": sp.ceiling,

            # Factorial
            "factorial": sp.factorial,
        }

    # ---------------------------------------------------------
    # RESULT FORMATTING
    # ---------------------------------------------------------

    @staticmethod
    def format_result(result):

        # Exact integers
        if result.is_Integer:
            return str(result)

        # Exact rational numbers
        #
        # Calculator-style output is more useful as a decimal.
        # For example:
        #
        #     50%      -> 0.5
        #     sin(30)  -> 0.5
        #     cos(60)  -> 0.5
        #
        if result.is_Rational:

            numerator = float(result.p)
            denominator = float(result.q)

            value = numerator / denominator

            if abs(value) < 1e-12:
                return "0"

            if value.is_integer():
                return str(int(value))

            return f"{value:.12g}"

        # Symbolic expression
        if not result.is_number:
            return str(result)

        try:

            numeric = sp.N(result, 12)

            if numeric.is_real:

                value = float(numeric)

                if abs(value) < 1e-12:
                    return "0"

                if value.is_integer():
                    return str(int(value))

                return f"{value:.12g}"

            return str(numeric)

        except Exception:
            return str(result)

    # ---------------------------------------------------------
    # ANGLE MODE CONTROLS
    # ---------------------------------------------------------

    def set_angle_mode(self, mode):

        mode = mode.upper()

        if mode not in ("DEG", "RAD"):
            raise ValueError(
                "Angle mode must be DEG or RAD"
            )

        self.angle_mode = mode

    def toggle_angle_mode(self):

        self.angle_mode = (
            "RAD"
            if self.angle_mode == "DEG"
            else "DEG"
        )

        return self.angle_mode

    def get_angle_mode(self):
        return self.angle_mode
    