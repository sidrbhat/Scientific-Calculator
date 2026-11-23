import numpy as np
import sympy as sp


class GraphEngine:
    """Handles mathematical function evaluation for 2D graphing."""

    def __init__(self):
        self.x = sp.Symbol("x")

    def prepare_expression(self, expression: str):
        """Convert calculator-style notation into SymPy notation."""

        expression = expression.strip()

        # Calculator symbols
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("−", "-")
        expression = expression.replace("^", "**")
        expression = expression.replace("π", "pi")
        expression = expression.replace("√", "sqrt")

        # Common shorthand
        expression = expression.replace("sinx", "sin(x)")
        expression = expression.replace("cosx", "cos(x)")
        expression = expression.replace("tanx", "tan(x)")
        expression = expression.replace("lnx", "ln(x)")
        expression = expression.replace("logx", "log(x)")

        return expression

    def evaluate(self, expression: str, x_values):
        """Evaluate an expression for an array of x values."""

        expression = self.prepare_expression(expression)

        local_dict = {
            "x": self.x,
            "pi": sp.pi,
            "e": sp.E,
            "sqrt": sp.sqrt,
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,
            "sinh": sp.sinh,
            "cosh": sp.cosh,
            "tanh": sp.tanh,
            "log": sp.log,
            "ln": sp.log,
            "exp": sp.exp,
            "abs": sp.Abs,
        }

        expr = sp.sympify(expression, locals=local_dict)

        func = sp.lambdify(
            self.x,
            expr,
            modules=["numpy"],
        )

        return func(x_values)

    def generate_graph_data(
        self,
        expression: str,
        x_min: float = -10,
        x_max: float = 10,
        points: int = 1000,
    ):
        """Generate x and y values for plotting."""

        x_values = np.linspace(
            float(x_min),
            float(x_max),
            int(points),
        )

        try:
            y_values = self.evaluate(expression, x_values)

            y_values = np.asarray(y_values, dtype=float)

            # Replace infinity and invalid values with NaN.
            y_values[~np.isfinite(y_values)] = np.nan

            return x_values, y_values

        except Exception as exc:
            raise ValueError(
                f"Unable to evaluate expression: {exc}"
            ) from exc