from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from ui.style import STYLESHEET
from ui.login_panel import LoginPanel
from ui.register_panel import RegisterPanel
from ui.user_panel import UserPanel
from ui.admin_panel import AdminPanel


class BankingSystem(QMainWindow):
    """Main application window."""

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        """Initialize main window and panels."""
        self.setWindowTitle('Banking System')
        self.setGeometry(200, 200, 0, 0)
        self.setStyleSheet(STYLESHEET)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_panel = LoginPanel(self)
        self.register_panel = RegisterPanel(self)
        self.user_panel = UserPanel(self)
        self.admin_panel = AdminPanel(self)

        self.stacked_widget.addWidget(self.login_panel)
        self.stacked_widget.addWidget(self.register_panel)
        self.stacked_widget.addWidget(self.user_panel)
        self.stacked_widget.addWidget(self.admin_panel)

        self.show_login_panel()

    def set_current_user(self, user):
        """Set the currently logged-in user."""
        self.current_user = user

    def show_login_panel(self):
        """Display login panel."""
        self.stacked_widget.setCurrentWidget(self.login_panel)

    def show_register_panel(self):
        """Display registration panel."""
        self.stacked_widget.setCurrentWidget(self.register_panel)

    def show_user_panel(self):
        """Display user dashboard."""
        self.user_panel.update_display()
        self.stacked_widget.setCurrentWidget(self.user_panel)

    def show_admin_panel(self):
        """Display admin dashboard."""
        self.admin_panel.load_transactions()
        self.stacked_widget.setCurrentWidget(self.admin_panel)

    def closeEvent(self, event):
        """Handle application close."""
        self.db.close()
        event.accept()