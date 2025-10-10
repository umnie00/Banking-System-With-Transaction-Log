STYLESHEET = """
/* Global Styles - Remove ALL focus outlines */
* {
    outline: none;
}

*:focus {
    outline: none;
}

QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #1a1a2e, stop:1 #16213e);
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #ffffff;
    outline: none;
}

QLabel {
    color: #ffffff;
    font-size: 13px;
}

QLabel#titleLabel {
    font-size: 28px;
    font-weight: bold;
    color: #00d4ff;
    padding: 15px;
}

QLabel#subtitleLabel {
    font-size: 18px;
    font-weight: bold;
    color: #00d4ff;
}

QLabel#timeLabel {
    font-size: 14px;
    font-weight: bold;
    color: #2ecc71;
    padding: 8px 16px;
    background-color: #2e3f5e;
    border-radius: 6px;
    border: 2px solid #2ecc71;
}

/* Input Fields */
QLineEdit {
    background-color: #364a6d;
    border: 2px solid #4a5f8c;
    border-radius: 10px;
    padding: 12px 16px;
    color: #ffffff;
    font-size: 14px;
    selection-background-color: #00d4ff;
    outline: none;
}

QLineEdit:hover {
    border: 2px solid #5a7fac;
    background-color: #3d5478;
}

QLineEdit:focus {
    border: 2px solid #00d4ff;
    background-color: #3d5478;
    outline: none;
}

/* Buttons - Enhanced with no focus outline */
QPushButton {
    background-color: #00d4ff;
    color: #1a1a2e;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: bold;
    min-width: 120px;
    min-height: 40px;
    outline: none;
}

QPushButton:hover {
    background-color: #00e8ff;
    transform: scale(1.02);
}

QPushButton:pressed {
    background-color: #00b8e6;
}

QPushButton:focus {
    outline: none;
    border: none;
}

QPushButton#logoutButton {
    background-color: #ff4757;
    color: white;
}

QPushButton#logoutButton:hover {
    background-color: #ff5e6c;
}

QPushButton#logoutButton:pressed {
    background-color: #ee3344;
}

QPushButton#depositButton {
    background-color: #2ecc71;
    color: white;
}

QPushButton#depositButton:hover {
    background-color: #3ed67e;
}

QPushButton#depositButton:pressed {
    background-color: #27ae60;
}

QPushButton#withdrawButton {
    background-color: #e74c3c;
    color: white;
}

QPushButton#withdrawButton:hover {
    background-color: #ef5b4d;
}

QPushButton#withdrawButton:pressed {
    background-color: #c0392b;
}

QPushButton#registerButton {
    background-color: #9b59b6;
    color: white;
}

QPushButton#registerButton:hover {
    background-color: #ae6ec9;
}

QPushButton#registerButton:pressed {
    background-color: #8e44ad;
}

QPushButton#backButton {
    background-color: #95a5a6;
    color: white;
    min-width: 100px;
}

QPushButton#backButton:hover {
    background-color: #a8b8b9;
}

QPushButton#backButton:pressed {
    background-color: #7f8c8d;
}

QPushButton#searchButton {
    background-color: #9b59b6;
    color: white;
}

QPushButton#searchButton:hover {
    background-color: #ae6ec9;
}

QPushButton#searchButton:pressed {
    background-color: #8e44ad;
}

QPushButton#clearButton {
    background-color: #95a5a6;
    color: white;
}

QPushButton#clearButton:hover {
    background-color: #a8b8b9;
}

QPushButton#clearButton:pressed {
    background-color: #7f8c8d;
}

QPushButton#refreshButton {
    background-color: #3498db;
    color: white;
}

QPushButton#refreshButton:hover {
    background-color: #4fa8e5;
}

QPushButton#refreshButton:pressed {
    background-color: #2980b9;
}

QPushButton#applyButton {
    background-color: #2ecc71;
    color: white;
}

QPushButton#applyButton:hover {
    background-color: #3ed67e;
}

QPushButton#applyButton:pressed {
    background-color: #27ae60;
}

/* Table Widget */
QTableWidget {
    background-color: #2e3f5e;
    alternate-background-color: #364a6d;
    border: 2px solid #4a5f8c;
    border-radius: 12px;
    gridline-color: #4a5f8c;
    color: #ffffff;
    selection-background-color: #00d4ff;
    selection-color: #1a1a2e;
    outline: none;
}

QTableWidget:focus {
    outline: none;
}

QTableWidget::item {
    padding: 12px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #00d4ff;
    color: #1a1a2e;
}

QTableWidget::item:focus {
    outline: none;
}

QHeaderView {
    outline: none;
}

QHeaderView::section {
    background-color: #1a1a2e;
    color: #00d4ff;
    padding: 12px;
    border: none;
    border-bottom: 2px solid #4a5f8c;
    font-weight: bold;
    font-size: 13px;
    outline: none;
}

QHeaderView::section:first {
    border-top-left-radius: 10px;
}

QHeaderView::section:last {
    border-top-right-radius: 10px;
}

/* ComboBox */
QComboBox {
    background-color: #364a6d;
    border: 2px solid #4a5f8c;
    border-radius: 10px;
    padding: 10px 16px;
    color: #ffffff;
    font-size: 14px;
    min-width: 150px;
    outline: none;
}

QComboBox:hover {
    border: 2px solid #5a7fac;
    background-color: #3d5478;
}

QComboBox:focus {
    outline: none;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
    background: transparent;
}

QComboBox::down-arrow {
    image: none;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 6px solid #00d4ff;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #364a6d;
    border: 2px solid #00d4ff;
    border-radius: 8px;
    selection-background-color: #00d4ff;
    selection-color: #1a1a2e;
    color: #ffffff;
    padding: 5px;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 10px;
    border-radius: 5px;
    min-height: 30px;
    outline: none;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #4a5f8c;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #00d4ff;
    color: #1a1a2e;
}

/* ScrollBars */
QScrollBar:vertical {
    background-color: #2e3f5e;
    width: 14px;
    border-radius: 7px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #00d4ff;
    border-radius: 7px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #00e8ff;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #2e3f5e;
    height: 14px;
    border-radius: 7px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background-color: #00d4ff;
    border-radius: 7px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #00e8ff;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Message Boxes */
QMessageBox {
    background-color: #2e3f5e;
    color: #ffffff;
}

QMessageBox QPushButton {
    min-width: 80px;
    padding: 8px 16px;
}

/* Group Boxes */
QGroupBox {
    outline: none;
}

QGroupBox:focus {
    outline: none;
}
"""