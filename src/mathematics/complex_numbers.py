import sympy as sp

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)


class ComplexNumberEngine:
    """Handles complex-number and phasor calculations."""

    def __init__(self):
        self.transformations = (
            standard_transformations
            + (
                implicit_multiplication_application,
                convert_xor,
            )
        )

    def parse(self, expression: str):
        """Convert user input into a SymPy complex expression."""

        expression = expression.strip()

        if not expression:
            raise ValueError("Please enter a complex number.")

        # Calculator-style operators
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("−", "-")
        expression = expression.replace("^", "**")

        # Allow both i and I as the imaginary unit.
        expression = expression.replace("i", "I")

        local_dict = {
            "I": sp.I,
            "i": sp.I,
            "pi": sp.pi,
            "π": sp.pi,
            "e": sp.E,
        }

        return parse_expr(
            expression,
            local_dict=local_dict,
            transformations=self.transformations,
        )

    def rectangular_form(self, expression: str):
        """Return real and imaginary parts."""

        z = self.parse(expression)

        real_part, imaginary_part = z.as_real_imag()

        return (
            sp.simplify(real_part),
            sp.simplify(imaginary_part),
        )

    def magnitude(self, expression: str):
        """Return the magnitude |z|."""

        z = self.parse(expression)

        return sp.simplify(sp.Abs(z))

    def phase_radians(self, expression: str):
        """Return the phase angle in radians."""

        z = self.parse(expression)

        return sp.arg(z)

    def phase_degrees(self, expression: str):
        """Return the phase angle in degrees."""

        angle = self.phase_radians(expression)

        return sp.N(
            angle * 180 / sp.pi,
            12,
        )

    def polar_form(self, expression: str):
        """Return magnitude and phase angle."""

        magnitude = self.magnitude(expression)
        phase = self.phase_degrees(expression)

        return magnitude, phase

    def get_details(self, expression: str):
        """Return complete information about a complex number."""

        z = sp.simplify(self.parse(expression))

        real_part, imaginary_part = z.as_real_imag()

        magnitude = sp.Abs(z)
        phase_radians = sp.arg(z)

        phase_degrees = sp.N(
            phase_radians * 180 / sp.pi,
            12,
        )

        return {
            "expression": z,
            "real": sp.simplify(real_part),
            "imaginary": sp.simplify(imaginary_part),
            "magnitude": sp.simplify(magnitude),
            "phase_radians": phase_radians,
            "phase_degrees": phase_degrees,
        }

    def format_complex(self, expression: str):
        """Format a complex number in rectangular form."""

        z = sp.simplify(self.parse(expression))

        real_part, imaginary_part = z.as_real_imag()

        real_part = sp.simplify(real_part)
        imaginary_part = sp.simplify(imaginary_part)

        if imaginary_part == 0:
            return str(real_part)

        if real_part == 0:

            if imaginary_part == 1:
                return "i"

            if imaginary_part == -1:
                return "-i"

            return f"{imaginary_part}i"

        if imaginary_part > 0:

            if imaginary_part == 1:
                return f"{real_part} + i"

            return f"{real_part} + {imaginary_part}i"

        if imaginary_part == -1:
            return f"{real_part} - i"

        return (
            f"{real_part} - "
            f"{sp.Abs(imaginary_part)}i"
        )

    def format_polar(self, expression: str):
        """Format a complex number as r ∠ θ°."""

        magnitude = self.magnitude(expression)
        phase = self.phase_degrees(expression)

        magnitude = sp.N(magnitude, 10)
        phase = sp.N(phase, 8)

        return f"{magnitude} ∠ {phase}°"

    def get_plot_coordinates(self, expression: str):
        """Return real and imaginary coordinates for plotting."""

        real_part, imaginary_part = (
            self.rectangular_form(expression)
        )

        return (
            float(sp.N(real_part)),
            float(sp.N(imaginary_part)),
        )