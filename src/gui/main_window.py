
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
    QComboBox,
)

from PySide6.QtCore import Qt

from src.core.calculator_engine import CalculatorEngine
from src.gui.graph_window import GraphWindow
from src.gui.complex_window import ComplexWindow
from src.gui.calculus_window import CalculusWindow


class CalculatorWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.engine = CalculatorEngine()
        self.memory = 0
        self.history = []

        self.graph_window = None
        self.complex_window = None
        self.calculus_window = None

        self.setWindowTitle("Scientific Calculator")
        self.resize(1000, 720)

        self.setup_ui()
        self.apply_theme("Dark")

    # ==========================================================
    # UI SETUP
    # ==========================================================

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        title = QLabel("🧮 Scientific Calculator")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        main_layout.addWidget(title)

        # TOP TOOLBAR

        toolbar = QHBoxLayout()

        self.angle_mode = QComboBox()
        self.angle_mode.addItems(["DEG", "RAD"])
        self.angle_mode.currentTextChanged.connect(
            self.change_angle_mode
        )

        toolbar.addWidget(QLabel("Angle:"))
        toolbar.addWidget(self.angle_mode)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "Dark",
            "Light",
            "Ocean",
            "Purple",
            "Green",
            "Sunset",
        ])
        self.theme_combo.currentTextChanged.connect(
            self.apply_theme
        )

        toolbar.addWidget(QLabel("Theme:"))
        toolbar.addWidget(self.theme_combo)

        toolbar.addStretch()

        graph_button = QPushButton("📈 Graph")
        graph_button.clicked.connect(self.open_graph)
        toolbar.addWidget(graph_button)

        complex_button = QPushButton("🧭 Complex / Phasor")
        complex_button.clicked.connect(self.open_complex)
        toolbar.addWidget(complex_button)

        calculus_button = QPushButton("∫ Calculus")
        calculus_button.clicked.connect(self.open_calculus)
        toolbar.addWidget(calculus_button)

        main_layout.addLayout(toolbar)

        # DISPLAY

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setText("0")
        self.display.setMinimumHeight(65)
        self.display.setStyleSheet("""
            QLineEdit {
                font-size: 30px;
                padding: 10px;
                border-radius: 12px;
            }
        """)
        main_layout.addWidget(self.display)

        # HISTORY

        history_label = QLabel("History")
        history_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
        """)
        main_layout.addWidget(history_label)

        self.history_display = QLineEdit()
        self.history_display.setReadOnly(True)
        self.history_display.setPlaceholderText(
            "Previous calculation..."
        )
        main_layout.addWidget(self.history_display)

        # MEMORY BUTTONS

        memory_layout = QHBoxLayout()

        memory_buttons = [
            ("MC", self.memory_clear),
            ("MR", self.memory_recall),
            ("M+", self.memory_add),
            ("M-", self.memory_subtract),
            ("MS", self.memory_store),
        ]

        for text, function in memory_buttons:
            button = QPushButton(text)
            button.clicked.connect(function)
            memory_layout.addWidget(button)

        main_layout.addLayout(memory_layout)

        # CALCULATOR BUTTONS

        grid = QGridLayout()

        buttons = [
            [
                ("C", self.clear),
                ("⌫", self.backspace),
                ("(", lambda: self.add_text("(")),
                (")", lambda: self.add_text(")")),
                ("÷", lambda: self.add_text("÷")),
            ],
            [
                ("sin", lambda: self.add_function("sin(")),
                ("cos", lambda: self.add_function("cos(")),
                ("tan", lambda: self.add_function("tan(")),
                ("7", lambda: self.add_text("7")),
                ("8", lambda: self.add_text("8")),
            ],
            [
                ("sin⁻¹", lambda: self.add_function("asin(")),
                ("cos⁻¹", lambda: self.add_function("acos(")),
                ("tan⁻¹", lambda: self.add_function("atan(")),
                ("9", lambda: self.add_text("9")),
                ("×", lambda: self.add_text("×")),
            ],
            [
                ("sinh", lambda: self.add_function("sinh(")),
                ("cosh", lambda: self.add_function("cosh(")),
                ("tanh", lambda: self.add_function("tanh(")),
                ("4", lambda: self.add_text("4")),
                ("5", lambda: self.add_text("5")),
            ],
            [
                ("log", lambda: self.add_function("log10(")),
                ("ln", lambda: self.add_function("ln(")),
                ("√", lambda: self.add_function("sqrt(")),
                ("6", lambda: self.add_text("6")),
                ("−", lambda: self.add_text("−")),
            ],
            [
                ("π", lambda: self.add_text("π")),
                ("e", lambda: self.add_text("e")),
                ("x²", lambda: self.add_text("^2")),
                ("1", lambda: self.add_text("1")),
                ("2", lambda: self.add_text("2")),
            ],
            [
                ("xʸ", lambda: self.add_text("^")),
                ("eˣ", lambda: self.add_function("exp(")),
                ("10ˣ", lambda: self.add_function("10^(")),
                ("3", lambda: self.add_text("3")),
                ("+", lambda: self.add_text("+")),
            ],
            [
                ("abs", lambda: self.add_function("abs(")),
                ("floor", lambda: self.add_function("floor(")),
                ("ceil", lambda: self.add_function("ceil(")),
                ("0", lambda: self.add_text("0")),
                (".", lambda: self.add_text(".")),
            ],
        ]

        for row, button_row in enumerate(buttons):
            for column, (text, function) in enumerate(button_row):

                button = QPushButton(text)
                button.setMinimumHeight(52)
                button.setMinimumWidth(100)
                button.clicked.connect(function)

                grid.addWidget(button, row, column)

        equal_button = QPushButton("=")
        equal_button.setMinimumHeight(52)
        equal_button.clicked.connect(self.calculate)

        grid.addWidget(equal_button, 8, 0, 1, 5)

        main_layout.addLayout(grid)

        self.display.returnPressed.connect(self.calculate)

    # ==========================================================
    # CALCULATOR FUNCTIONS
    # ==========================================================

    def add_text(self, text):

        current = self.display.text()

        if current == "0":
            current = ""

        self.display.setText(current + text)

    def add_function(self, function):

        current = self.display.text()

        if current == "0":
            current = ""

        self.display.setText(current + function)

    def clear(self):
        self.display.setText("0")

    def backspace(self):

        current = self.display.text()

        if len(current) <= 1:
            self.display.setText("0")
        else:
            self.display.setText(current[:-1])

    def calculate(self):

        expression = self.display.text()

        if not expression or expression == "0":
            return

        try:
            result = self.engine.calculate(expression)

            self.history.append(
                f"{expression} = {result}"
            )

            self.history_display.setText(
                f"{expression} = {result}"
            )

            self.display.setText(str(result))

        except Exception as exc:
            QMessageBox.warning(
                self,
                "Calculation Error",
                str(exc)
            )

    # ==========================================================
    # ANGLE MODE
    # ==========================================================

    def change_angle_mode(self, mode):
        self.engine.set_angle_mode(mode)

    # ==========================================================
    # MEMORY
    # ==========================================================

    def get_numeric_display(self):

        try:
            return float(self.display.text())
        except Exception:
            return 0.0

    def memory_clear(self):
        self.memory = 0

    def memory_recall(self):
        self.display.setText(str(self.memory))

    def memory_add(self):
        self.memory += self.get_numeric_display()

    def memory_subtract(self):
        self.memory -= self.get_numeric_display()

    def memory_store(self):
        self.memory = self.get_numeric_display()

    # ==========================================================
    # OPEN CHILD WINDOWS
    # ==========================================================

    def show_child_window(self, window):

        window.setWindowFlags(
            Qt.WindowType.Window
        )

        window.setWindowModality(
            Qt.WindowModality.NonModal
        )

        window.show()
        window.raise_()
        window.activateWindow()

    def open_graph(self):

        self.graph_window = GraphWindow(self)
        self.show_child_window(self.graph_window)

    def open_complex(self):

        self.complex_window = ComplexWindow(self)
        self.show_child_window(self.complex_window)

    def open_calculus(self):

        self.calculus_window = CalculusWindow(self)
        self.show_child_window(self.calculus_window)

    # ==========================================================
    # THEMES
    # ==========================================================

    def apply_theme(self, theme):

        if theme == "Dark":

            self.setStyleSheet("""
                QWidget {
                    background-color: #181824;
                    color: #ffffff;
                }

                QPushButton {
                    background-color: #29293d;
                    color: white;
                    border: 1px solid #44445c;
                    border-radius: 10px;
                    padding: 8px;
                    font-size: 14px;
                }

                QPushButton:hover {
                    background-color: #3a3a55;
                }

                QLineEdit, QComboBox {
                    background-color: #242436;
                    color: white;
                    border: 1px solid #55556e;
                    border-radius: 8px;
                    padding: 6px;
                }
            """)

        elif theme == "Light":

            self.setStyleSheet("""
                QWidget {
                    background-color: #f4f4f4;
                    color: #111111;
                }

                QPushButton {
                    background-color: #ffffff;
                    color: #111111;
                    border: 1px solid #cccccc;
                    border-radius: 10px;
                    padding: 8px;
                    font-size: 14px;
                }

                QPushButton:hover {
                    background-color: #e5e5e5;
                }

                QLineEdit, QComboBox {
                    background-color: white;
                    color: #111111;
                    border: 1px solid #cccccc;
                    border-radius: 8px;
                    padding: 6px;
                }
            """)

        elif theme == "Ocean":

            self.setStyleSheet("""
                QWidget {
                    background-color: #071e2d;
                    color: #e6f7ff;
                }

                QPushButton {
                    background-color: #0d405c;
                    color: #e6f7ff;
                    border: 1px solid #176487;
                    border-radius: 10px;
                    padding: 8px;
                }

                QPushButton:hover {
                    background-color: #155b7c;
                }

                QLineEdit, QComboBox {
                    background-color: #0b2f43;
                    color: #e6f7ff;
                    border: 1px solid #176487;
                    border-radius: 8px;
                    padding: 6px;
                }
            """)

        elif theme == "Purple":

            self.setStyleSheet("""
                QWidget {
                    background-color: #21152e;
                    color: #f8edff;
                }

                QPushButton {
                    background-color: #4b2670;
                    color: #ffffff;
                    border: 1px solid #7540a8;
                    border-radius: 10px;
                    padding: 8px;
                }

                QPushButton:hover {
                    background-color: #613494;
                }

                QLineEdit, QComboBox {
                    background-color: #321d45;
                    color: #ffffff;
                    border: 1px solid #7540a8;
                    border-radius: 8px;
                    padding: 6px;
                }
            """)

        elif theme == "Green":

            self.setStyleSheet("""
                QWidget {
                    background-color: #102217;
                    color: #edfff2;
                }

                QPushButton {
                    background-color: #214d31;
                    color: #edfff2;
                    border: 1px solid #3c7950;
                    border-radius: 10px;
                    padding: 8px;
                }

                QPushButton:hover {
                    background-color: #2d6841;
                }

                QLineEdit, QComboBox {
                    background-color: #183522;
                    color: #edfff2;
                    border: 1px solid #3c7950;
                    border-radius: 8px;
                    padding: 6px;
                }
            """)

        elif theme == "Sunset":

            self.setStyleSheet("""
                QWidget {
                    background-color: #2b1714;
                    color: #fff4ef;
                }

                QPushButton {
                    background-color: #71352c;
                    color: #fff4ef;
                    border: 1px solid #a84d3d;
                    border-radius: 10px;
                    padding: 8px;
                }

                QPushButton:hover {
                    background-color: #914438;
                }

                QLineEdit, QComboBox {
                    background-color: #40201b;
                    color: #fff4ef;
                    border: 1px solid #a84d3d;
                    border-radius: 8px;
                    padding: 6px;
                }
            """)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = CalculatorWindow()
    window.show()

    sys.exit(app.exec())
