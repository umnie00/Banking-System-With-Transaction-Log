from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox)
from PyQt6.QtCore import Qt



class LoginPanel(QWidget):
    """Login panel UI."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel('🏦¦ Banking System With Transaction Log')
        title.setObjectName('titleLabel')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        form_widget = QWidget()
        form_widget.setMaximumWidth(400)
        form_widget.setStyleSheet("""
            QWidget {
                background-color: #2e3f5e;
                border-radius: 15px;
                padding: 30px;
            }
        """)

        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)

        username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        self.username_input.returnPressed.connect(self.login)
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)

        password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.login)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.login)
        button_layout.addWidget(login_btn)

        register_btn = QPushButton('Register')
        register_btn.setObjectName('registerButton')
        register_btn.clicked.connect(self.show_register)
        button_layout.addWidget(register_btn)

        form_layout.addLayout(button_layout)


        layout.addWidget(form_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password.')
            return

        user = self.parent.db.authenticate(username, password)

        if user:
            self.parent.set_current_user(user)
            if user.role == 'admin':
                self.parent.show_admin_panel()
            else:
                self.parent.show_user_panel()
            self.clear_fields()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password.')

    def show_register(self):
        self.parent.show_register_panel()

    def clear_fields(self):
        self.username_input.clear()