from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFrame,
)

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
)

from matplotlib.figure import Figure

from src.mathematics.complex_numbers import (
    ComplexNumberEngine,
)


class ComplexWindow(QWidget):
    """Interactive complex-number and phasor diagram window."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(
            "Complex Numbers & Phasor Diagram"
        )

        self.resize(1100, 750)

        self.engine = ComplexNumberEngine()

        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)

        # =========================================================
        # TITLE
        # =========================================================

        title = QLabel(
            "🧭 Complex Numbers & Phasor Diagram"
        )

        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 8px;
            }
        """)

        main_layout.addWidget(title)

        # =========================================================
        # INPUT
        # =========================================================

        input_layout = QHBoxLayout()

        input_layout.addWidget(
            QLabel("z =")
        )

        self.expression_input = QLineEdit()

        self.expression_input.setPlaceholderText(
            "Enter a complex number, e.g. 3 + 4i"
        )

        self.expression_input.setText(
            "3 + 4i"
        )

        input_layout.addWidget(
            self.expression_input
        )

        self.calculate_button = QPushButton(
            "Calculate"
        )

        self.calculate_button.clicked.connect(
            self.calculate
        )

        input_layout.addWidget(
            self.calculate_button
        )

        main_layout.addLayout(
            input_layout
        )

        # =========================================================
        # INFORMATION CARDS
        # =========================================================

        info_layout = QHBoxLayout()

        self.rectangular_label = QLabel(
            "Rectangular: —"
        )

        self.magnitude_label = QLabel(
            "Magnitude: —"
        )

        self.phase_label = QLabel(
            "Phase: —"
        )

        self.polar_label = QLabel(
            "Polar: —"
        )

        labels = [
            self.rectangular_label,
            self.magnitude_label,
            self.phase_label,
            self.polar_label,
        ]

        for label in labels:

            label.setFrameStyle(
                QFrame.Shape.StyledPanel
            )

            label.setMinimumHeight(45)

            label.setStyleSheet("""
                QLabel {
                    font-size: 15px;
                    padding: 8px;
                }
            """)

            info_layout.addWidget(
                label
            )

        main_layout.addLayout(
            info_layout
        )

        # =========================================================
        # MATPLOTLIB FIGURE
        # =========================================================

        self.figure = Figure()

        self.canvas = FigureCanvas(
            self.figure
        )

        main_layout.addWidget(
            self.canvas
        )

        # Initial calculation
        self.calculate()

    # =============================================================
    # CALCULATE
    # =============================================================

    def calculate(self):

        expression = (
            self.expression_input.text().strip()
        )

        if not expression:
            return

        try:

            details = (
                self.engine.get_details(
                    expression
                )
            )

            real = float(
                details["real"]
            )

            imaginary = float(
                details["imaginary"]
            )

            magnitude = float(
                details["magnitude"]
            )

            phase = float(
                details["phase_degrees"]
            )

            rectangular = (
                self.engine.format_complex(
                    expression
                )
            )

            polar = (
                self.engine.format_polar(
                    expression
                )
            )

            self.rectangular_label.setText(
                f"Rectangular: {rectangular}"
            )

            self.magnitude_label.setText(
                f"Magnitude: {magnitude:.6g}"
            )

            self.phase_label.setText(
                f"Phase: {phase:.6g}°"
            )

            self.polar_label.setText(
                f"Polar: {polar}"
            )

            self.plot_phasor(
                real,
                imaginary,
                magnitude,
                phase,
            )

        except Exception as exc:

            QMessageBox.warning(
                self,
                "Complex Number Error",
                (
                    "Unable to process this expression.\n\n"
                    f"{exc}"
                ),
            )

    # =============================================================
    # PLOT PHASOR
    # =============================================================

    def plot_phasor(
        self,
        real,
        imaginary,
        magnitude,
        phase,
    ):

        self.figure.clear()

        ax = self.figure.add_subplot(
            111
        )

        # Determine graph size.
        max_value = max(
            abs(real),
            abs(imaginary),
            magnitude,
            1,
        )

        limit = max_value * 1.25

        # ---------------------------------------------------------
        # Axes
        # ---------------------------------------------------------

        ax.axhline(
            0,
            linewidth=1,
        )

        ax.axvline(
            0,
            linewidth=1,
        )

        # ---------------------------------------------------------
        # Phasor vector
        # ---------------------------------------------------------

        ax.quiver(
            0,
            0,
            real,
            imaginary,
            angles="xy",
            scale_units="xy",
            scale=1,
            width=0.006,
        )

        # ---------------------------------------------------------
        # Endpoint
        # ---------------------------------------------------------

        ax.scatter(
            [real],
            [imaginary],
            s=80,
        )

        # ---------------------------------------------------------
        # Projection lines
        # ---------------------------------------------------------

        ax.plot(
            [real, real],
            [0, imaginary],
            linestyle="--",
            linewidth=1,
        )

        ax.plot(
            [0, real],
            [imaginary, imaginary],
            linestyle="--",
            linewidth=1,
        )

        # ---------------------------------------------------------
        # Vector label
        # ---------------------------------------------------------

        if imaginary >= 0:

            z_text = (
                f"z = {real:g} + "
                f"{imaginary:g}i"
            )

        else:

            z_text = (
                f"z = {real:g} - "
                f"{abs(imaginary):g}i"
            )

        ax.text(
            real,
            imaginary,
            f"  {z_text}",
            fontsize=11,
        )

        # ---------------------------------------------------------
        # Magnitude label
        # ---------------------------------------------------------

        ax.text(
            real / 2,
            imaginary / 2,
            f"|z| = {magnitude:.3g}",
            fontsize=10,
        )

        # ---------------------------------------------------------
        # Graph limits
        # ---------------------------------------------------------

        ax.set_xlim(
            -limit,
            limit,
        )

        ax.set_ylim(
            -limit,
            limit,
        )

        ax.set_aspect(
            "equal",
            adjustable="box",
        )

        # ---------------------------------------------------------
        # Labels
        # ---------------------------------------------------------

        ax.set_xlabel(
            "Real"
        )

        ax.set_ylabel(
            "Imaginary"
        )

        ax.set_title(
            "Argand Plane — "
            f"|z| = {magnitude:.4g}, "
            f"∠ {phase:.4g}°"
        )

        ax.grid(
            True,
            alpha=0.3,
        )

        self.figure.tight_layout()

        self.canvas.draw()