import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt


class BankWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.balance = 1000

        self.setWindowTitle("Bank Terminal")
        self.setFixedSize(420, 380)

        self.setStyleSheet(open("style.qss", encoding="utf-8").read())

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.title_label = QLabel("Pinky Bank")
        self.title_label.setObjectName("title")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hint_label = QLabel("Выберите операцию и введите сумму")
        self.hint_label.setObjectName("hint")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.balance_label = QLabel("Баланс: " + str(self.balance) + " руб.")
        self.balance_label.setObjectName("баланс")
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.operation_box = QComboBox()
        self.operation_box.addItem("Пополнить")
        self.operation_box.addItem("Снять")

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Введите сумму")

        self.run_button = QPushButton("Выполнить")
        self.run_button.clicked.connect(self.do_operation)

    def create_layout(self):
        row_layout = QHBoxLayout()
        row_layout.addWidget(self.operation_box)
        row_layout.addWidget(self.amount_input)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.hint_label)
        main_layout.addWidget(self.balance_label)
        main_layout.addLayout(row_layout)
        main_layout.addWidget(self.run_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_error(self, text):
        QMessageBox.warning(self, "Ошибка", text)

    def do_operation(self):
        text = self.amount_input.text().strip()

        if text == "":
            self.show_error("Вы ничего не ввели. Введите сумму.")
            return

        if text.startswith("-"):
            self.show_error("Сумма не может быть отрицательной.")
            return

        if not text.isdigit():
            self.show_error("Сумма должна состоять только из цифр.")
            return

        amount = int(text)

        if amount == 0:
            self.show_error("Сумма должна быть больше нуля.")
            return

        operation = self.operation_box.currentText()

        if operation == "Пополнить":
            self.balance = self.balance + amount
            QMessageBox.information(self, "Успех", "Счёт пополнен на " + str(amount) + " руб.")
        else:
            if amount > self.balance:
                self.show_error("Недостаточно средств на счёте.")
                return
            self.balance = self.balance - amount
            QMessageBox.information(self, "Успех", "Вы сняли " + str(amount) + " руб.")

        self.balance_label.setText("Баланс: " + str(self.balance) + " руб.")
        self.amount_input.clear()


app = QApplication(sys.argv)
app.setStyle("Fusion") 
window = BankWindow()
window.show()
sys.exit(app.exec())