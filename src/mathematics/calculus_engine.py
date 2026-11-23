import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


class CalculusEngine:

    def __init__(self):
        self.x = sp.Symbol("x")
        self.y = sp.Symbol("y")
        self.z = sp.Symbol("z")

        self.local_dict = {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "pi": sp.pi,
            "e": sp.E,
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,
            "sqrt": sp.sqrt,
            "log": sp.log,
            "ln": sp.log,
            "exp": sp.exp,
            "abs": sp.Abs,
        }

    def parse(self, expression):
        return parse_expr(
            expression,
            local_dict=self.local_dict,
            transformations=TRANSFORMATIONS,
            evaluate=True,
        )

    def differentiate(self, expression, variable="x", order=1):
        expr = self.parse(expression)
        symbol = sp.Symbol(variable)

        result = sp.diff(expr, symbol, order)

        return str(sp.simplify(result))

    def integrate(
        self,
        expression,
        variable="x",
        lower=None,
        upper=None,
    ):
        expr = self.parse(expression)
        symbol = sp.Symbol(variable)

        if lower is not None and upper is not None:
            result = sp.integrate(
                expr,
                (symbol, sp.sympify(lower), sp.sympify(upper)),
            )
        else:
            result = sp.integrate(expr, symbol)

        return str(sp.simplify(result))

    def calculate_limit(
        self,
        expression,
        variable="x",
        point="0",
        direction="+-",
    ):
        expr = self.parse(expression)
        symbol = sp.Symbol(variable)

        result = sp.limit(
            expr,
            symbol,
            sp.sympify(point),
            dir=direction,
        )

        return str(result)

    def partial_differentiate(
        self,
        expression,
        variable="x",
        order=1,
    ):
        return self.differentiate(
            expression,
            variable,
            order,
        )