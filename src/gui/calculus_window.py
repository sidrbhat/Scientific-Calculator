from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
)

from PySide6.QtCore import Qt

from src.mathematics.calculus_engine import CalculusEngine


class CalculusWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.engine = CalculusEngine()

        self.setWindowTitle("Calculus - Integration & Differentiation")
        self.setMinimumSize(650, 520)

        self.setStyleSheet("""
            QDialog {
                background-color: #171827;
                color: white;
            }

            QLabel {
                color: white;
                font-size: 14px;
            }

            QLineEdit, QComboBox {
                background-color: #292b40;
                color: white;
                padding: 12px;
                border: 1px solid #555a80;
                border-radius: 8px;
                font-size: 14px;
            }

            QPushButton {
                background-color: #7657e8;
                color: white;
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #9279f5;
            }
        """)

        self.create_ui()

    def create_ui(self):

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("CALCULUS TOOLKIT")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size: 25px; font-weight: bold; color: #a995ff;"
        )

        layout.addWidget(title)

        description = QLabel(
            "Differentiate, integrate and calculate limits."
        )
        description.setAlignment(Qt.AlignCenter)

        layout.addWidget(description)

        layout.addWidget(QLabel("Choose operation"))

        self.operation = QComboBox()

        self.operation.addItems([
            "Differentiation",
            "Second Derivative",
            "Integration",
            "Definite Integration",
            "Limit",
            "Partial Differentiation",
        ])

        self.operation.currentTextChanged.connect(
            self.update_fields
        )

        layout.addWidget(self.operation)

        layout.addWidget(QLabel("Enter expression"))

        self.expression = QLineEdit()
        self.expression.setPlaceholderText(
            "Example: x^3 + 2*x^2 + 5"
        )

        layout.addWidget(self.expression)

        layout.addWidget(QLabel("Variable"))

        self.variable = QLineEdit("x")
        layout.addWidget(self.variable)

        self.point_label = QLabel("Limit point")
        self.point = QLineEdit("0")

        layout.addWidget(self.point_label)
        layout.addWidget(self.point)

        self.lower_label = QLabel("Lower limit")
        self.lower = QLineEdit("0")

        self.upper_label = QLabel("Upper limit")
        self.upper = QLineEdit("2")

        layout.addWidget(self.lower_label)
        layout.addWidget(self.lower)

        layout.addWidget(self.upper_label)
        layout.addWidget(self.upper)

        self.calculate_button = QPushButton("CALCULATE")
        self.calculate_button.clicked.connect(self.calculate)

        layout.addWidget(self.calculate_button)

        layout.addWidget(QLabel("RESULT"))

        self.result = QLineEdit()
        self.result.setReadOnly(True)
        self.result.setMinimumHeight(55)
        self.result.setStyleSheet("""
            QLineEdit {
                background-color: #22243a;
                color: #8df5bd;
                font-size: 18px;
                font-weight: bold;
            }
        """)

        layout.addWidget(self.result)

        self.update_fields()

    def update_fields(self):

        operation = self.operation.currentText()

        is_limit = operation == "Limit"
        is_definite = operation == "Definite Integration"

        self.point_label.setVisible(is_limit)
        self.point.setVisible(is_limit)

        self.lower_label.setVisible(is_definite)
        self.lower.setVisible(is_definite)

        self.upper_label.setVisible(is_definite)
        self.upper.setVisible(is_definite)

    def calculate(self):

        expression = self.expression.text().strip()
        variable = self.variable.text().strip()

        if not expression or not variable:
            QMessageBox.warning(
                self,
                "Missing input",
                "Please enter an expression and variable.",
            )
            return

        try:

            operation = self.operation.currentText()

            if operation == "Differentiation":
                answer = self.engine.differentiate(
                    expression, variable, 1
                )

            elif operation == "Second Derivative":
                answer = self.engine.differentiate(
                    expression, variable, 2
                )

            elif operation == "Integration":
                answer = self.engine.integrate(
                    expression, variable
                )

            elif operation == "Definite Integration":
                answer = self.engine.integrate(
                    expression,
                    variable,
                    self.lower.text(),
                    self.upper.text(),
                )

            elif operation == "Limit":
                answer = self.engine.calculate_limit(
                    expression,
                    variable,
                    self.point.text(),
                )

            elif operation == "Partial Differentiation":
                answer = self.engine.partial_differentiate(
                    expression,
                    variable,
                )

            else:
                answer = "Unknown operation"

            self.result.setText(answer)

        except Exception as error:
            QMessageBox.warning(
                self,
                "Calculation error",
                str(error),
            )