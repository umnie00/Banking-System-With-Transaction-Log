# import sys
# import sqlite3
# import time
# from datetime import datetime
# from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
#                              QHBoxLayout, QLabel, QLineEdit, QPushButton,
#                              QTableWidget, QTableWidgetItem, QMessageBox,
#                              QStackedWidget, QComboBox, QHeaderView)
# from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
# from PyQt6.QtGui import QFont
#
#
# # AVL Tree Node
# class AVLNode:
#     def __init__(self, transaction_data):
#         self.data = transaction_data
#         self.left = None
#         self.right = None
#         self.height = 1
#
#
# # AVL Tree Implementation
# class AVLTree:
#     def __init__(self):
#         self.root = None
#         self.result_list = []
#
#     def get_height(self, node):
#         if not node:
#             return 0
#         return node.height
#
#     def get_balance(self, node):
#         if not node:
#             return 0
#         return self.get_height(node.left) - self.get_height(node.right)
#
#     def right_rotate(self, y):
#         x = y.left
#         T2 = x.right
#         x.right = y
#         y.left = T2
#         y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
#         x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
#         return x
#
#     def left_rotate(self, x):
#         y = x.right
#         T2 = y.left
#         y.left = x
#         x.right = T2
#         x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
#         y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
#         return y
#
#     def insert(self, node, transaction_data):
#         if not node:
#             return AVLNode(transaction_data)
#
#         if transaction_data['amount'] < node.data['amount']:
#             node.left = self.insert(node.left, transaction_data)
#         else:
#             node.right = self.insert(node.right, transaction_data)
#
#         node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
#         balance = self.get_balance(node)
#
#         if balance > 1 and transaction_data['amount'] < node.left.data['amount']:
#             return self.right_rotate(node)
#
#         if balance < -1 and transaction_data['amount'] >= node.right.data['amount']:
#             return self.left_rotate(node)
#
#         if balance > 1 and transaction_data['amount'] >= node.left.data['amount']:
#             node.left = self.left_rotate(node.left)
#             return self.right_rotate(node)
#
#         if balance < -1 and transaction_data['amount'] < node.right.data['amount']:
#             node.right = self.right_rotate(node.right)
#             return self.left_rotate(node)
#
#         return node
#
#     def add_transaction(self, transaction_data):
#         self.root = self.insert(self.root, transaction_data)
#
#     def inorder_traversal(self, node, result_list):
#         if node:
#             self.inorder_traversal(node.left, result_list)
#             result_list.append(node.data)
#             self.inorder_traversal(node.right, result_list)
#
#     def search_greater_than(self, node, min_amount, result_list):
#         if not node:
#             return
#         if node.data['amount'] > min_amount:
#             self.search_greater_than(node.left, min_amount, result_list)
#             result_list.append(node.data)
#         self.search_greater_than(node.right, min_amount, result_list)
#
#     def search_less_than(self, node, max_amount, result_list):
#         if not node:
#             return
#         self.search_less_than(node.left, max_amount, result_list)
#         if node.data['amount'] < max_amount:
#             result_list.append(node.data)
#             self.search_less_than(node.right, max_amount, result_list)
#
#     def search_range(self, node, min_amount, max_amount, result_list):
#         if not node:
#             return
#         if node.data['amount'] > min_amount:
#             self.search_range(node.left, min_amount, max_amount, result_list)
#         if min_amount <= node.data['amount'] <= max_amount:
#             result_list.append(node.data)
#         if node.data['amount'] < max_amount:
#             self.search_range(node.right, min_amount, max_amount, result_list)
#
#     def get_all_sorted(self):
#         result = []
#         self.inorder_traversal(self.root, result)
#         return result
#
#     def filter_greater_than(self, min_amount):
#         result = []
#         self.search_greater_than(self.root, min_amount, result)
#         return result
#
#     def filter_less_than(self, max_amount):
#         result = []
#         self.search_less_than(self.root, max_amount, result)
#         return result
#
#     def filter_range(self, min_amount, max_amount):
#         result = []
#         self.search_range(self.root, min_amount, max_amount, result)
#         return result
#
#
# # Database Manager
# class DatabaseManager:
#     def __init__(self):
#         self.conn = sqlite3.connect('banking_system.db')
#         self.cursor = self.conn.cursor()
#         self.init_database()
#
#     def init_database(self):
#         # Check if accounts table exists and get its columns
#         self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'")
#         table_exists = self.cursor.fetchone()
#
#         if table_exists:
#             # Check if created_at column exists
#             self.cursor.execute("PRAGMA table_info(accounts)")
#             columns = [column[1] for column in self.cursor.fetchall()]
#
#             if 'created_at' not in columns:
#                 # Add created_at column to existing table
#                 try:
#                     self.cursor.execute("ALTER TABLE accounts ADD COLUMN created_at TEXT DEFAULT ''")
#                     self.conn.commit()
#                 except sqlite3.OperationalError:
#                     pass
#         else:
#             # Create new table with created_at column
#             self.cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS accounts (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     username TEXT UNIQUE NOT NULL,
#                     password TEXT NOT NULL,
#                     role TEXT NOT NULL,
#                     balance REAL DEFAULT 0.0,
#                     created_at TEXT DEFAULT ''
#                 )
#             ''')
#
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS transactions (
#                 transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 account_id INTEGER NOT NULL,
#                 type TEXT NOT NULL,
#                 amount REAL NOT NULL,
#                 timestamp TEXT NOT NULL,
#                 FOREIGN KEY (account_id) REFERENCES accounts (id)
#             )
#         ''')
#
#         try:
#             timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             self.cursor.execute('''
#                 INSERT INTO accounts (username, password, role, balance, created_at)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', ('admin', 'admin123', 'admin', 0.0, timestamp))
#
#             self.cursor.execute('''
#                 INSERT INTO accounts (username, password, role, balance, created_at)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', ('user', 'user123', 'user', 1000.0, timestamp))
#
#             self.conn.commit()
#         except sqlite3.IntegrityError:
#             pass
#
#     def authenticate(self, username, password):
#         self.cursor.execute('''
#             SELECT id, username, role, balance FROM accounts
#             WHERE username = ? AND password = ?
#         ''', (username, password))
#         return self.cursor.fetchone()
#
#     def register_user(self, username, password, initial_balance=0.0):
#         try:
#             timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             self.cursor.execute('''
#                 INSERT INTO accounts (username, password, role, balance, created_at)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', (username, password, 'user', initial_balance, timestamp))
#             self.conn.commit()
#             return True, "Registration successful!"
#         except sqlite3.IntegrityError:
#             return False, "Username already exists!"
#
#     def get_balance(self, account_id):
#         self.cursor.execute('SELECT balance FROM accounts WHERE id = ?', (account_id,))
#         result = self.cursor.fetchone()
#         return result[0] if result else 0.0
#
#     def update_balance(self, account_id, new_balance):
#         self.cursor.execute('UPDATE accounts SET balance = ? WHERE id = ?', (new_balance, account_id))
#         self.conn.commit()
#
#     def add_transaction(self, account_id, trans_type, amount):
#         timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         self.cursor.execute('''
#             INSERT INTO transactions (account_id, type, amount, timestamp)
#             VALUES (?, ?, ?, ?)
#         ''', (account_id, trans_type, amount, timestamp))
#         self.conn.commit()
#
#     def get_user_transactions(self, account_id):
#         self.cursor.execute('''
#             SELECT transaction_id, type, amount, timestamp
#             FROM transactions
#             WHERE account_id = ?
#             ORDER BY transaction_id DESC
#         ''', (account_id,))
#         return self.cursor.fetchall()
#
#     def get_all_transactions(self):
#         self.cursor.execute('''
#             SELECT t.transaction_id, a.username, t.type, t.amount, t.timestamp
#             FROM transactions t
#             JOIN accounts a ON t.account_id = a.id
#             ORDER BY t.transaction_id DESC
#         ''')
#         return self.cursor.fetchall()
#
#     def close(self):
#         self.conn.close()
#
#
# # Stylesheet
# STYLESHEET = """
# QMainWindow {
#     background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
#                                 stop:0 #1a1a2e, stop:1 #16213e);
# }
#
# QWidget {
#     font-family: 'Segoe UI', Arial, sans-serif;
#     color: #ffffff;
# }
#
# QLabel {
#     color: #ffffff;
#     font-size: 13px;
# }
#
# QLabel#titleLabel {
#     font-size: 28px;
#     font-weight: bold;
#     color: #00d4ff;
#     padding: 15px;
# }
#
# QLabel#subtitleLabel {
#     font-size: 18px;
#     font-weight: bold;
#     color: #00d4ff;
# }
#
# QLabel#timeLabel {
#     font-size: 14px;
#     font-weight: bold;
#     color: #2ecc71;
#     padding: 8px 16px;
#     background-color: #2e3f5e;
#     border-radius: 6px;
#     border: 2px solid #2ecc71;
# }
#
# QLineEdit {
#     background-color: #2e3f5e;
#     border: 2px solid #4a5f8c;
#     border-radius: 8px;
#     padding: 12px;
#     color: #ffffff;
#     font-size: 14px;
#     selection-background-color: #00d4ff;
# }
#
# QLineEdit:focus {
#     border: 2px solid #00d4ff;
#     background-color: #364a6d;
# }
#
# QPushButton {
#     background-color: #00d4ff;
#     color: #1a1a2e;
#     border: none;
#     border-radius: 8px;
#     padding: 12px 24px;
#     font-size: 14px;
#     font-weight: bold;
#     min-width: 120px;
# }
#
# QPushButton:hover {
#     background-color: #00b8e6;
# }
#
# QPushButton:pressed {
#     background-color: #0099cc;
# }
#
# QPushButton#logoutButton {
#     background-color: #ff4757;
# }
#
# QPushButton#logoutButton:hover {
#     background-color: #ee3344;
# }
#
# QPushButton#depositButton {
#     background-color: #2ecc71;
# }
#
# QPushButton#depositButton:hover {
#     background-color: #27ae60;
# }
#
# QPushButton#withdrawButton {
#     background-color: #e74c3c;
# }
#
# QPushButton#withdrawButton:hover {
#     background-color: #c0392b;
# }
#
# QPushButton#registerButton {
#     background-color: #9b59b6;
# }
#
# QPushButton#registerButton:hover {
#     background-color: #8e44ad;
# }
#
# QPushButton#backButton {
#     background-color: #95a5a6;
#     min-width: 100px;
# }
#
# QPushButton#backButton:hover {
#     background-color: #7f8c8d;
# }
#
# QTableWidget {
#     background-color: #2e3f5e;
#     alternate-background-color: #364a6d;
#     border: 2px solid #4a5f8c;
#     border-radius: 8px;
#     gridline-color: #4a5f8c;
#     color: #ffffff;
#     selection-background-color: #00d4ff;
#     selection-color: #1a1a2e;
# }
#
# QTableWidget::item {
#     padding: 8px;
# }
#
# QHeaderView::section {
#     background-color: #1a1a2e;
#     color: #00d4ff;
#     padding: 10px;
#     border: 1px solid #4a5f8c;
#     font-weight: bold;
#     font-size: 13px;
# }
#
# QComboBox {
#     background-color: #2e3f5e;
#     border: 2px solid #4a5f8c;
#     border-radius: 8px;
#     padding: 10px;
#     color: #ffffff;
#     font-size: 14px;
#     min-width: 150px;
# }
#
# QComboBox:hover {
#     border: 2px solid #00d4ff;
# }
#
# QComboBox::drop-down {
#     border: none;
#     width: 30px;
# }
#
# QComboBox::down-arrow {
#     image: none;
#     border-left: 5px solid transparent;
#     border-right: 5px solid transparent;
#     border-top: 5px solid #00d4ff;
#     margin-right: 10px;
# }
#
# QComboBox QAbstractItemView {
#     background-color: #2e3f5e;
#     border: 2px solid #4a5f8c;
#     selection-background-color: #00d4ff;
#     selection-color: #1a1a2e;
#     color: #ffffff;
# }
# """
#
#
# # Login Panel
# class LoginPanel(QWidget):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         self.init_ui()
#
#     def init_ui(self):
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.setSpacing(20)
#
#         title = QLabel('🏦 Banking System')
#         title.setObjectName('titleLabel')
#         title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(title)
#
#         form_widget = QWidget()
#         form_widget.setMaximumWidth(400)
#         form_widget.setStyleSheet("""
#             QWidget {
#                 background-color: #2e3f5e;
#                 border-radius: 15px;
#                 padding: 30px;
#             }
#         """)
#
#         form_layout = QVBoxLayout(form_widget)
#         form_layout.setSpacing(15)
#
#         username_label = QLabel('Username:')
#         self.username_input = QLineEdit()
#         self.username_input.setPlaceholderText('Enter username')
#         self.username_input.returnPressed.connect(self.login)
#         form_layout.addWidget(username_label)
#         form_layout.addWidget(self.username_input)
#
#         password_label = QLabel('Password:')
#         self.password_input = QLineEdit()
#         self.password_input.setPlaceholderText('Enter password')
#         self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
#         self.password_input.returnPressed.connect(self.login)
#         form_layout.addWidget(password_label)
#         form_layout.addWidget(self.password_input)
#
#         button_layout = QHBoxLayout()
#
#         login_btn = QPushButton('Login')
#         login_btn.clicked.connect(self.login)
#         button_layout.addWidget(login_btn)
#
#         register_btn = QPushButton('Register')
#         register_btn.setObjectName('registerButton')
#         register_btn.clicked.connect(self.show_register)
#         button_layout.addWidget(register_btn)
#
#         form_layout.addLayout(button_layout)
#
#         info_label = QLabel('Default Credentials:\nAdmin: admin/admin123\nUser: user/user123')
#         info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         info_label.setStyleSheet('color: #888; font-size: 11px; margin-top: 10px;')
#         form_layout.addWidget(info_label)
#
#         layout.addWidget(form_widget, alignment=Qt.AlignmentFlag.AlignCenter)
#         self.setLayout(layout)
#
#     def login(self):
#         username = self.username_input.text().strip()
#         password = self.password_input.text()
#
#         if not username or not password:
#             QMessageBox.warning(self, 'Error', 'Please enter both username and password.')
#             return
#
#         user_data = self.parent.db.authenticate(username, password)
#
#         if user_data:
#             self.parent.current_user = {
#                 'id': user_data[0],
#                 'username': user_data[1],
#                 'role': user_data[2],
#                 'balance': user_data[3]
#             }
#
#             if user_data[2] == 'admin':
#                 self.parent.show_admin_panel()
#             else:
#                 self.parent.show_user_panel()
#
#             self.username_input.clear()
#             self.password_input.clear()
#         else:
#             QMessageBox.warning(self, 'Error', 'Invalid username or password.')
#
#     def show_register(self):
#         self.parent.show_register_panel()
#
#
# # Register Panel
# class RegisterPanel(QWidget):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         self.init_ui()
#
#     def init_ui(self):
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.setSpacing(20)
#
#         title = QLabel('📝 Create New Account')
#         title.setObjectName('titleLabel')
#         title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(title)
#
#         form_widget = QWidget()
#         form_widget.setMaximumWidth(400)
#         form_widget.setStyleSheet("""
#             QWidget {
#                 background-color: #2e3f5e;
#                 border-radius: 15px;
#                 padding: 30px;
#             }
#         """)
#
#         form_layout = QVBoxLayout(form_widget)
#         form_layout.setSpacing(15)
#
#         username_label = QLabel('Username:')
#         self.username_input = QLineEdit()
#         self.username_input.setPlaceholderText('Choose a username (min 3 characters)')
#         form_layout.addWidget(username_label)
#         form_layout.addWidget(self.username_input)
#
#         password_label = QLabel('Password:')
#         self.password_input = QLineEdit()
#         self.password_input.setPlaceholderText('Choose a password (min 4 characters)')
#         self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
#         form_layout.addWidget(password_label)
#         form_layout.addWidget(self.password_input)
#
#         confirm_label = QLabel('Confirm Password:')
#         self.confirm_input = QLineEdit()
#         self.confirm_input.setPlaceholderText('Re-enter password')
#         self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
#         form_layout.addWidget(confirm_label)
#         form_layout.addWidget(self.confirm_input)
#
#         balance_label = QLabel('Initial Balance (Optional):')
#         self.balance_input = QLineEdit()
#         self.balance_input.setPlaceholderText('Enter initial deposit (default: $0.00)')
#         form_layout.addWidget(balance_label)
#         form_layout.addWidget(self.balance_input)
#
#         button_layout = QHBoxLayout()
#
#         back_btn = QPushButton('Back')
#         back_btn.setObjectName('backButton')
#         back_btn.clicked.connect(self.go_back)
#         button_layout.addWidget(back_btn)
#
#         register_btn = QPushButton('Create Account')
#         register_btn.setObjectName('registerButton')
#         register_btn.clicked.connect(self.register)
#         button_layout.addWidget(register_btn)
#
#         form_layout.addLayout(button_layout)
#
#         info_label = QLabel(
#             '⚠️ Username must be unique\n✓ Password must be at least 4 characters\n✓ Initial balance is optional')
#         info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         info_label.setStyleSheet('color: #888; font-size: 11px; margin-top: 10px;')
#         form_layout.addWidget(info_label)
#
#         layout.addWidget(form_widget, alignment=Qt.AlignmentFlag.AlignCenter)
#         self.setLayout(layout)
#
#     def register(self):
#         username = self.username_input.text().strip()
#         password = self.password_input.text()
#         confirm = self.confirm_input.text()
#         balance_text = self.balance_input.text().strip()
#
#         if not username or not password:
#             QMessageBox.warning(self, 'Error', 'Username and password are required!')
#             return
#
#         if len(username) < 3:
#             QMessageBox.warning(self, 'Error', 'Username must be at least 3 characters!')
#             return
#
#         if len(password) < 4:
#             QMessageBox.warning(self, 'Error', 'Password must be at least 4 characters!')
#             return
#
#         if password != confirm:
#             QMessageBox.warning(self, 'Error', 'Passwords do not match!')
#             return
#
#         initial_balance = 0.0
#         if balance_text:
#             try:
#                 initial_balance = float(balance_text)
#                 if initial_balance < 0:
#                     QMessageBox.warning(self, 'Error', 'Initial balance cannot be negative!')
#                     return
#             except ValueError:
#                 QMessageBox.warning(self, 'Error', 'Invalid balance amount!')
#                 return
#
#         success, message = self.parent.db.register_user(username, password, initial_balance)
#
#         if success:
#             QMessageBox.information(self, 'Success',
#                                     f'Account created successfully!\n\nUsername: {username}\nInitial Balance: ${initial_balance:.2f}\n\nYou can now login with your credentials.')
#             self.clear_fields()
#             self.parent.show_login_panel()
#         else:
#             QMessageBox.warning(self, 'Error', message)
#
#     def clear_fields(self):
#         self.username_input.clear()
#         self.password_input.clear()
#         self.confirm_input.clear()
#         self.balance_input.clear()
#
#     def go_back(self):
#         self.clear_fields()
#         self.parent.show_login_panel()
#
#
# # User Panel
# class UserPanel(QWidget):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         self.init_ui()
#
#     def init_ui(self):
#         layout = QVBoxLayout()
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)
#
#         header = QHBoxLayout()
#         title = QLabel('User Dashboard')
#         title.setObjectName('titleLabel')
#         header.addWidget(title)
#         header.addStretch()
#
#         self.username_label = QLabel()
#         self.username_label.setStyleSheet('font-size: 14px; color: #00d4ff;')
#         header.addWidget(self.username_label)
#
#         logout_btn = QPushButton('Logout')
#         logout_btn.setObjectName('logoutButton')
#         logout_btn.clicked.connect(self.logout)
#         header.addWidget(logout_btn)
#         layout.addLayout(header)
#
#         self.balance_label = QLabel()
#         self.balance_label.setObjectName('subtitleLabel')
#         self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.balance_label)
#
#         trans_layout = QHBoxLayout()
#
#         amount_label = QLabel('Amount:')
#         self.amount_input = QLineEdit()
#         self.amount_input.setPlaceholderText('Enter amount')
#         trans_layout.addWidget(amount_label)
#         trans_layout.addWidget(self.amount_input)
#
#         deposit_btn = QPushButton('Deposit')
#         deposit_btn.setObjectName('depositButton')
#         deposit_btn.clicked.connect(self.deposit)
#         trans_layout.addWidget(deposit_btn)
#
#         withdraw_btn = QPushButton('Withdraw')
#         withdraw_btn.setObjectName('withdrawButton')
#         withdraw_btn.clicked.connect(self.withdraw)
#         trans_layout.addWidget(withdraw_btn)
#
#         layout.addLayout(trans_layout)
#
#         history_label = QLabel('Transaction History:')
#         history_label.setObjectName('subtitleLabel')
#         layout.addWidget(history_label)
#
#         self.transaction_table = QTableWidget()
#         self.transaction_table.setColumnCount(4)
#         self.transaction_table.setHorizontalHeaderLabels(['ID', 'Type', 'Amount', 'Timestamp'])
#         self.transaction_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
#         self.transaction_table.setAlternatingRowColors(True)
#         self.transaction_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
#         layout.addWidget(self.transaction_table)
#
#         self.setLayout(layout)
#
#     def update_display(self):
#         user = self.parent.current_user
#         self.username_label.setText(f'👤 {user["username"]}')
#         balance = self.parent.db.get_balance(user['id'])
#         self.balance_label.setText(f'💰 Current Balance: ${balance:.2f}')
#
#         transactions = self.parent.db.get_user_transactions(user['id'])
#         self.transaction_table.setRowCount(len(transactions))
#
#         for row, trans in enumerate(transactions):
#             self.transaction_table.setItem(row, 0, QTableWidgetItem(str(trans[0])))
#
#             trans_type = trans[1].upper()
#             type_item = QTableWidgetItem(trans_type)
#             if trans_type == 'DEPOSIT':
#                 type_item.setForeground(Qt.GlobalColor.green)
#             else:
#                 type_item.setForeground(Qt.GlobalColor.red)
#             self.transaction_table.setItem(row, 1, type_item)
#
#             self.transaction_table.setItem(row, 2, QTableWidgetItem(f'${trans[2]:.2f}'))
#             self.transaction_table.setItem(row, 3, QTableWidgetItem(trans[3]))
#
#     def deposit(self):
#         try:
#             amount = float(self.amount_input.text())
#             if amount <= 0:
#                 QMessageBox.warning(self, 'Error', 'Amount must be positive.')
#                 return
#
#             user_id = self.parent.current_user['id']
#             current_balance = self.parent.db.get_balance(user_id)
#             new_balance = current_balance + amount
#
#             self.parent.db.update_balance(user_id, new_balance)
#             self.parent.db.add_transaction(user_id, 'deposit', amount)
#
#             QMessageBox.information(self, 'Success', f'Deposited ${amount:.2f} successfully!')
#             self.amount_input.clear()
#             self.update_display()
#         except ValueError:
#             QMessageBox.warning(self, 'Error', 'Please enter a valid amount.')
#
#     def withdraw(self):
#         try:
#             amount = float(self.amount_input.text())
#             if amount <= 0:
#                 QMessageBox.warning(self, 'Error', 'Amount must be positive.')
#                 return
#
#             user_id = self.parent.current_user['id']
#             current_balance = self.parent.db.get_balance(user_id)
#
#             if amount > current_balance:
#                 QMessageBox.warning(self, 'Error', 'Insufficient balance.')
#                 return
#
#             new_balance = current_balance - amount
#             self.parent.db.update_balance(user_id, new_balance)
#             self.parent.db.add_transaction(user_id, 'withdraw', amount)
#
#             QMessageBox.information(self, 'Success', f'Withdrew ${amount:.2f} successfully!')
#             self.amount_input.clear()
#             self.update_display()
#         except ValueError:
#             QMessageBox.warning(self, 'Error', 'Please enter a valid amount.')
#
#     def logout(self):
#         self.parent.current_user = None
#         self.parent.show_login_panel()
#
#
# # Admin Panel
# class AdminPanel(QWidget):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
#         self.avl_tree = AVLTree()
#         self.init_ui()
#
#     def init_ui(self):
#         layout = QVBoxLayout()
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)
#
#         header = QHBoxLayout()
#         title = QLabel('Admin Dashboard')
#         title.setObjectName('titleLabel')
#         header.addWidget(title)
#         header.addStretch()
#
#         logout_btn = QPushButton('Logout')
#         logout_btn.setObjectName('logoutButton')
#         logout_btn.clicked.connect(self.logout)
#         header.addWidget(logout_btn)
#         layout.addLayout(header)
#
#         filter_layout = QHBoxLayout()
#
#         filter_label = QLabel('Filter by Amount:')
#         filter_layout.addWidget(filter_label)
#
#         self.filter_combo = QComboBox()
#         self.filter_combo.addItems(['All Transactions', 'Greater Than', 'Less Than', 'Range'])
#         self.filter_combo.currentTextChanged.connect(self.toggle_filter_inputs)
#         filter_layout.addWidget(self.filter_combo)
#
#         self.min_input = QLineEdit()
#         self.min_input.setPlaceholderText('Min Amount')
#         self.min_input.setMaximumWidth(150)
#         self.min_input.hide()
#         filter_layout.addWidget(self.min_input)
#
#         self.max_input = QLineEdit()
#         self.max_input.setPlaceholderText('Max Amount')
#         self.max_input.setMaximumWidth(150)
#         self.max_input.hide()
#         filter_layout.addWidget(self.max_input)
#
#         apply_btn = QPushButton('Apply Filter')
#         apply_btn.clicked.connect(self.apply_filter)
#         filter_layout.addWidget(apply_btn)
#
#         refresh_btn = QPushButton('Refresh')
#         refresh_btn.clicked.connect(self.load_transactions)
#         filter_layout.addWidget(refresh_btn)
#
#         # Add running time label
#         self.time_label = QLabel('⏱️ Running Time: 0.0000s')
#         self.time_label.setObjectName('timeLabel')
#         filter_layout.addWidget(self.time_label)
#
#         filter_layout.addStretch()
#         layout.addLayout(filter_layout)
#
#         table_label = QLabel('All Transactions (Sorted by AVL Tree):')
#         table_label.setObjectName('subtitleLabel')
#         layout.addWidget(table_label)
#
#         self.transaction_table = QTableWidget()
#         self.transaction_table.setColumnCount(5)
#         self.transaction_table.setHorizontalHeaderLabels(['ID', 'Username', 'Type', 'Amount', 'Timestamp'])
#         self.transaction_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
#         self.transaction_table.setAlternatingRowColors(True)
#         self.transaction_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
#         layout.addWidget(self.transaction_table)
#
#         self.setLayout(layout)
#
#     def toggle_filter_inputs(self, filter_type):
#         self.min_input.hide()
#         self.max_input.hide()
#
#         if filter_type == 'Greater Than':
#             self.min_input.show()
#             self.min_input.setPlaceholderText('Min Amount')
#         elif filter_type == 'Less Than':
#             self.min_input.show()
#             self.min_input.setPlaceholderText('Max Amount')
#         elif filter_type == 'Range':
#             self.min_input.show()
#             self.max_input.show()
#
#     def load_transactions(self):
#         start_time = time.perf_counter()
#
#         self.avl_tree = AVLTree()
#         transactions = self.parent.db.get_all_transactions()
#
#         for trans in transactions:
#             trans_data = {
#                 'id': trans[0],
#                 'username': trans[1],
#                 'type': trans[2],
#                 'amount': trans[3],
#                 'timestamp': trans[4]
#             }
#             self.avl_tree.add_transaction(trans_data)
#
#         self.display_transactions(self.avl_tree.get_all_sorted())
#
#         end_time = time.perf_counter()
#         elapsed_time = end_time - start_time
#         self.time_label.setText(f'⏱️ Running Time: {elapsed_time:.6f}s')
#
#     def apply_filter(self):
#         filter_type = self.filter_combo.currentText()
#         start_time = time.perf_counter()
#
#         try:
#             if filter_type == 'All Transactions':
#                 self.display_transactions(self.avl_tree.get_all_sorted())
#
#             elif filter_type == 'Greater Than':
#                 min_amount = float(self.min_input.text())
#                 filtered = self.avl_tree.filter_greater_than(min_amount)
#                 self.display_transactions(filtered)
#
#             elif filter_type == 'Less Than':
#                 max_amount = float(self.min_input.text())
#                 filtered = self.avl_tree.filter_less_than(max_amount)
#                 self.display_transactions(filtered)
#
#             elif filter_type == 'Range':
#                 min_amount = float(self.min_input.text())
#                 max_amount = float(self.max_input.text())
#                 if min_amount > max_amount:
#                     QMessageBox.warning(self, 'Error', 'Min amount cannot be greater than max amount.')
#                     return
#                 filtered = self.avl_tree.filter_range(min_amount, max_amount)
#                 self.display_transactions(filtered)
#
#             end_time = time.perf_counter()
#             elapsed_time = end_time - start_time
#             self.time_label.setText(f'⏱️ Running Time: {elapsed_time:.6f}s')
#
#         except ValueError:
#             QMessageBox.warning(self, 'Error', 'Please enter valid numeric values.')
#
#     def display_transactions(self, transactions):
#         self.transaction_table.setRowCount(len(transactions))
#
#         for row, trans in enumerate(transactions):
#             self.transaction_table.setItem(row, 0, QTableWidgetItem(str(trans['id'])))
#             self.transaction_table.setItem(row, 1, QTableWidgetItem(trans['username']))
#
#             trans_type = trans['type'].upper()
#             type_item = QTableWidgetItem(trans_type)
#             if trans_type == 'DEPOSIT':
#                 type_item.setForeground(Qt.GlobalColor.green)
#             else:
#                 type_item.setForeground(Qt.GlobalColor.red)
#             self.transaction_table.setItem(row, 2, type_item)
#
#             self.transaction_table.setItem(row, 3, QTableWidgetItem(f"${trans['amount']:.2f}"))
#             self.transaction_table.setItem(row, 4, QTableWidgetItem(trans['timestamp']))
#
#     def logout(self):
#         self.parent.current_user = None
#         self.parent.show_login_panel()
#
#
# # Main Window
# class BankingSystem(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.db = DatabaseManager()
#         self.current_user = None
#         self.init_ui()
#
#     def init_ui(self):
#         self.setWindowTitle('Banking System')
#         self.setGeometry(100, 100, 1000, 700)
#         self.setStyleSheet(STYLESHEET)
#
#         self.stacked_widget = QStackedWidget()
#         self.setCentralWidget(self.stacked_widget)
#
#         self.login_panel = LoginPanel(self)
#         self.register_panel = RegisterPanel(self)
#         self.user_panel = UserPanel(self)
#         self.admin_panel = AdminPanel(self)
#
#         self.stacked_widget.addWidget(self.login_panel)
#         self.stacked_widget.addWidget(self.register_panel)
#         self.stacked_widget.addWidget(self.user_panel)
#         self.stacked_widget.addWidget(self.admin_panel)
#
#         self.show_login_panel()
#
#     def show_login_panel(self):
#         self.stacked_widget.setCurrentWidget(self.login_panel)
#
#     def show_register_panel(self):
#         self.stacked_widget.setCurrentWidget(self.register_panel)
#
#     def show_user_panel(self):
#         self.user_panel.update_display()
#         self.stacked_widget.setCurrentWidget(self.user_panel)
#
#     def show_admin_panel(self):
#         self.admin_panel.load_transactions()
#         self.stacked_widget.setCurrentWidget(self.admin_panel)
#
#     def closeEvent(self, event):
#         self.db.close()
#         event.accept()
#
#
# def main():
#     app = QApplication(sys.argv)
#     window = BankingSystem()
#     window.show()
#     sys.exit(app.exec())
#
#
# if __name__ == '__main__':
#     main()