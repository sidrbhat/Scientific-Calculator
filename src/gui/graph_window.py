from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDoubleSpinBox,
    QMessageBox,
)

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
)

from matplotlib.figure import Figure

from src.mathematics.graphing import GraphEngine


class GraphWindow(QWidget):
    """Window used for 2D mathematical function graphing."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Function Graphing")
        self.resize(1200, 800)

        self.engine = GraphEngine()

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # ---------------------------------------------------------
        # Title
        # ---------------------------------------------------------

        title = QLabel("📈 Function Graphing")
        title.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: bold;
                padding: 5px;
            }
        """)

        main_layout.addWidget(title)

        # ---------------------------------------------------------
        # Expression row
        # ---------------------------------------------------------

        expression_layout = QHBoxLayout()

        expression_label = QLabel("y =")

        self.expression_input = QLineEdit()
        self.expression_input.setText("sin(x)")
        self.expression_input.setPlaceholderText(
            "Enter a function, e.g. sin(x), x^2, cos(x)"
        )

        self.plot_button = QPushButton("📈 Plot")
        self.plot_button.clicked.connect(self.plot_graph)

        expression_layout.addWidget(expression_label)
        expression_layout.addWidget(self.expression_input)
        expression_layout.addWidget(self.plot_button)

        main_layout.addLayout(expression_layout)

        # ---------------------------------------------------------
        # Quick Insert
        # ---------------------------------------------------------

        quick_label = QLabel("Quick Insert")
        quick_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
        """)

        main_layout.addWidget(quick_label)

        keypad = QGridLayout()

        buttons = [
            ("x", 0, 0),
            ("+", 0, 1),
            ("−", 0, 2),
            ("×", 0, 3),
            ("÷", 0, 4),

            ("(", 1, 0),
            (")", 1, 1),
            ("^", 1, 2),
            ("√", 1, 3),
            ("π", 1, 4),

            ("sin(x)", 2, 0),
            ("cos(x)", 2, 1),
            ("tan(x)", 2, 2),
            ("log(x)", 2, 3),
            ("ln(x)", 2, 4),

            ("e^x", 3, 0),
            ("|x|", 3, 1),
            ("asin(x)", 3, 2),
            ("acos(x)", 3, 3),
            ("atan(x)", 3, 4),

            ("Clear", 4, 0, 5),
        ]

        for item in buttons:

            if len(item) == 3:
                text, row, column = item
                button = QPushButton(text)

                button.clicked.connect(
                    lambda checked=False, value=text:
                    self.quick_insert(value)
                )

                keypad.addWidget(button, row, column)

            else:
                text, row, column, colspan = item

                button = QPushButton(text)

                button.clicked.connect(self.clear_expression)

                keypad.addWidget(
                    button,
                    row,
                    column,
                    1,
                    colspan,
                )

        main_layout.addLayout(keypad)

        # ---------------------------------------------------------
        # Range controls
        # ---------------------------------------------------------

        range_layout = QHBoxLayout()

        range_layout.addWidget(QLabel("X min:"))

        self.x_min_input = QDoubleSpinBox()
        self.x_min_input.setRange(-100000, 100000)
        self.x_min_input.setValue(-10)
        self.x_min_input.setDecimals(2)

        range_layout.addWidget(self.x_min_input)

        range_layout.addWidget(QLabel("X max:"))

        self.x_max_input = QDoubleSpinBox()
        self.x_max_input.setRange(-100000, 100000)
        self.x_max_input.setValue(10)
        self.x_max_input.setDecimals(2)

        range_layout.addWidget(self.x_max_input)

        main_layout.addLayout(range_layout)

        # ---------------------------------------------------------
        # Matplotlib figure
        # ---------------------------------------------------------

        self.figure = Figure()

        self.canvas = FigureCanvas(self.figure)

        main_layout.addWidget(self.canvas)

        self.plot_graph()

    # -------------------------------------------------------------
    # Quick insert
    # -------------------------------------------------------------

    def quick_insert(self, value):
        replacements = {
            "−": "-",
            "×": "*",
            "÷": "/",
            "^": "**",
            "√": "sqrt(",
            "π": "pi",
            "e^x": "exp(x)",
            "|x|": "abs(x)",
        }

        value = replacements.get(value, value)

        self.expression_input.insert(value)

        self.expression_input.setFocus()

    # -------------------------------------------------------------
    # Clear
    # -------------------------------------------------------------

    def clear_expression(self):
        self.expression_input.clear()
        self.expression_input.setFocus()

    # -------------------------------------------------------------
    # Plot
    # -------------------------------------------------------------

    def plot_graph(self):

        expression = self.expression_input.text().strip()

        if not expression:
            QMessageBox.warning(
                self,
                "Graphing Error",
                "Please enter a function.",
            )
            return

        x_min = self.x_min_input.value()
        x_max = self.x_max_input.value()

        if x_min >= x_max:
            QMessageBox.warning(
                self,
                "Graphing Error",
                "X min must be smaller than X max.",
            )
            return

        try:

            x_values, y_values = (
                self.engine.generate_graph_data(
                    expression,
                    x_min=x_min,
                    x_max=x_max,
                    points=1000,
                )
            )

            self.figure.clear()

            ax = self.figure.add_subplot(111)

            ax.plot(
                x_values,
                y_values,
                linewidth=2,
                label=f"y = {expression}",
            )

            ax.axhline(
                0,
                linewidth=1,
            )

            ax.axvline(
                0,
                linewidth=1,
            )

            ax.grid(True, alpha=0.3)

            ax.set_xlabel("x")
            ax.set_ylabel("y")

            ax.set_title(
                f"Graph of y = {expression}"
            )

            ax.legend()

            self.figure.tight_layout()

            self.canvas.draw()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Graphing Error",
                f"Unable to graph this expression.\n\n{exc}",
            )