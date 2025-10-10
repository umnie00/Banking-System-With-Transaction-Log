from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
from config import MIN_USERNAME_LENGTH, MIN_PASSWORD_LENGTH


class RegisterPanel(QWidget):
    """Registration panel UI."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        title = QLabel(' Create New Account')
        title.setObjectName('titleLabel')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        form_widget = QWidget()
        form_widget.setMaximumWidth(1000)
        form_widget.setStyleSheet("""
            QWidget {
                background-color: #2e3f5e;
                border-radius: 15px;
                padding: 50px;
            }
        """)

        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)

        username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(f'Choose a username (min {MIN_USERNAME_LENGTH} characters)')
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)

        password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(f'Choose a password (min {MIN_PASSWORD_LENGTH} characters)')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)

        confirm_label = QLabel('Confirm Password:')
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText('Re-enter password')
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(confirm_label)
        form_layout.addWidget(self.confirm_input)

        balance_label = QLabel('Initial Balance (Optional):')
        self.balance_input = QLineEdit()
        self.balance_input.setPlaceholderText('Enter initial deposit (default: $0.00)')
        form_layout.addWidget(balance_label)
        form_layout.addWidget(self.balance_input)

        button_layout = QHBoxLayout()
        back_btn = QPushButton('Back')
        back_btn.setObjectName('backButton')
        back_btn.clicked.connect(self.go_back)
        button_layout.addWidget(back_btn)

        register_btn = QPushButton('Create Account')
        register_btn.setObjectName('registerButton')
        register_btn.clicked.connect(self.register)
        button_layout.addWidget(register_btn)

        form_layout.addLayout(button_layout)


        layout.addWidget(form_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        balance_text = self.balance_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Username and password are required!')
            return

        if len(username) < MIN_USERNAME_LENGTH:
            QMessageBox.warning(self, 'Error', f'Username must be at least {MIN_USERNAME_LENGTH} characters!')
            return

        if len(password) < MIN_PASSWORD_LENGTH:
            QMessageBox.warning(self, 'Error', f'Password must be at least {MIN_PASSWORD_LENGTH} characters!')
            return

        if password != confirm:
            QMessageBox.warning(self, 'Error', 'Passwords do not match!')
            return

        initial_balance = 0.0
        if balance_text:
            try:
                initial_balance = float(balance_text)
                if initial_balance < 0:
                    QMessageBox.warning(self, 'Error', 'Initial balance cannot be negative!')
                    return
            except ValueError:
                QMessageBox.warning(self, 'Error', 'Invalid balance amount!')
                return

        success, message = self.parent.db.register_user(username, password, initial_balance)

        if success:
            QMessageBox.information(self, 'Success',
                                    f'Account created successfully!\n\nUsername: {username}\nInitial Balance: ${initial_balance:.2f}\n\nYou can now login.')
            self.clear_fields()
            self.parent.show_login_panel()
        else:
            QMessageBox.warning(self, 'Error', message)

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_input.clear()
        self.balance_input.clear()

    def go_back(self):
        self.clear_fields()
        self.parent.show_login_panel()