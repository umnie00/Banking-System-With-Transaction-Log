import sys
from PyQt6.QtWidgets import QApplication
from database.db_manager import DatabaseManager
from ui.main_window import BankingSystem


def main():
    app = QApplication(sys.argv)
    db = DatabaseManager()
    window = BankingSystem(db)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()