import time
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QComboBox, QHeaderView, QGroupBox, QFrame)
from PyQt6.QtCore import Qt
from data_structure.avl_tree import AVLTree


class AdminPanel(QWidget):
    """Admin dashboard UI with enhanced filtering and search."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.avl_tree = AVLTree()
        self.all_transactions = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header Section
        header = QHBoxLayout()
        title = QLabel('🔐 Admin Dashboard')
        title.setObjectName('titleLabel')
        header.addWidget(title)
        header.addStretch()

        self.stats_label = QLabel('📊 Total Transactions: 0')
        self.stats_label.setStyleSheet('''
            font-size: 14px; 
            color: #00d4ff; 
            background-color: #2e3f5e;
            padding: 8px 16px;
            border-radius: 8px;
            border: 2px solid #00d4ff;
        ''')
        header.addWidget(self.stats_label)

        logout_btn = QPushButton('🚪 Logout')
        logout_btn.setObjectName('logoutButton')
        logout_btn.clicked.connect(self.logout)
        header.addWidget(logout_btn)
        layout.addLayout(header)

        # Filters Group Box
        filter_group = QGroupBox('🔍 Filter & Search Options')
        filter_group.setStyleSheet('''
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #00d4ff;
                border: 2px solid #4a5f8c;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        ''')
        filter_layout = QVBoxLayout(filter_group)

        # Row 1: Transaction Type and Amount Filter
        row1 = QHBoxLayout()

        type_label = QLabel('📝 Transaction Type:')
        type_label.setStyleSheet('font-size: 13px; font-weight: bold;')
        row1.addWidget(type_label)

        self.type_combo = QComboBox()
        self.type_combo.addItems(['All Types', 'Deposits Only', 'Withdrawals Only'])
        self.type_combo.currentTextChanged.connect(self.on_filter_change)
        row1.addWidget(self.type_combo)

        row1.addWidget(self.create_separator())

        filter_label = QLabel('💰 Amount Filter:')
        filter_label.setStyleSheet('font-size: 13px; font-weight: bold;')
        row1.addWidget(filter_label)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['All Transactions', 'Greater Than', 'Less Than', 'Range'])
        self.filter_combo.currentTextChanged.connect(self.toggle_filter_inputs)
        row1.addWidget(self.filter_combo)

        self.min_input = QLineEdit()
        self.min_input.setPlaceholderText('Min Amount')
        self.min_input.setMaximumWidth(150)
        self.min_input.hide()
        row1.addWidget(self.min_input)

        self.max_input = QLineEdit()
        self.max_input.setPlaceholderText('Max Amount')
        self.max_input.setMaximumWidth(150)
        self.max_input.hide()
        row1.addWidget(self.max_input)

        row1.addStretch()
        filter_layout.addLayout(row1)

        # Row 2: Search and Action Buttons
        row2 = QHBoxLayout()

        search_label = QLabel('🔎 Search Username:')
        search_label.setStyleSheet('font-size: 13px; font-weight: bold;')
        row2.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Enter username to search...')
        self.search_input.setMaximumWidth(250)
        self.search_input.returnPressed.connect(self.apply_filter)
        row2.addWidget(self.search_input)

        search_btn = QPushButton('🔍 Search')
        search_btn.setObjectName('searchButton')
        search_btn.setMaximumWidth(120)
        search_btn.clicked.connect(self.apply_filter)
        row2.addWidget(search_btn)

        clear_btn = QPushButton('🔄 Clear')
        clear_btn.setObjectName('clearButton')
        clear_btn.setMaximumWidth(120)
        clear_btn.clicked.connect(self.clear_filters)
        row2.addWidget(clear_btn)

        row2.addWidget(self.create_separator())

        apply_btn = QPushButton('✅ Apply Filters')
        apply_btn.setMaximumWidth(150)
        apply_btn.clicked.connect(self.apply_filter)
        row2.addWidget(apply_btn)

        refresh_btn = QPushButton('🔄 Refresh Data')
        refresh_btn.setMaximumWidth(150)
        refresh_btn.clicked.connect(self.load_transactions)
        row2.addWidget(refresh_btn)

        self.time_label = QLabel('⏱️ Running Time: 0.0000s')
        self.time_label.setObjectName('timeLabel')
        row2.addWidget(self.time_label)

        row2.addStretch()
        filter_layout.addLayout(row2)

        layout.addWidget(filter_group)

        # Table Section
        table_header = QHBoxLayout()
        table_label = QLabel('📋 Transaction Records')
        table_label.setObjectName('subtitleLabel')
        table_header.addWidget(table_label)

        self.result_count_label = QLabel('Showing: 0 transactions')
        self.result_count_label.setStyleSheet('font-size: 13px; color: #2ecc71;')
        table_header.addWidget(self.result_count_label)
        table_header.addStretch()
        layout.addLayout(table_header)

        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(5)
        self.transaction_table.setHorizontalHeaderLabels(['ID', 'Username', 'Type', 'Amount', 'Timestamp'])
        self.transaction_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.transaction_table.setAlternatingRowColors(True)
        self.transaction_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.transaction_table.setStyleSheet('''
            QTableWidget {
                background-color: #2e3f5e;
                alternate-background-color: #364a6d;
                border: 2px solid #4a5f8c;
                border-radius: 10px;
                gridline-color: #4a5f8c;
            }
        ''')
        layout.addWidget(self.transaction_table)

        # Account Info Section (appears below table)
        self.account_info_group = QGroupBox('👤 Account Information')
        self.account_info_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #2ecc71;
                border: 2px solid #2ecc71;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #2e3f5e;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        ''')
        account_layout = QHBoxLayout(self.account_info_group)

        self.account_details = QLabel('Search for a username to view account details...')
        self.account_details.setStyleSheet('font-size: 13px; color: #ffffff; padding: 10px;')
        self.account_details.setWordWrap(True)
        account_layout.addWidget(self.account_details)

        self.account_info_group.hide()
        layout.addWidget(self.account_info_group)

        self.setLayout(layout)

    def create_separator(self):
        """Create a vertical separator line."""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet('color: #4a5f8c;')
        return separator

    def toggle_filter_inputs(self, filter_type):
        """Show/hide filter inputs based on selection."""
        self.min_input.hide()
        self.max_input.hide()

        if filter_type == 'Greater Than':
            self.min_input.show()
            self.min_input.setPlaceholderText('Min Amount')
        elif filter_type == 'Less Than':
            self.min_input.show()
            self.min_input.setPlaceholderText('Max Amount')
        elif filter_type == 'Range':
            self.min_input.show()
            self.max_input.show()

    def on_filter_change(self):
        """Auto-apply filter when transaction type changes."""
        if self.avl_tree.root:
            self.apply_filter()

    def clear_filters(self):
        """Clear all filters and search."""
        self.type_combo.setCurrentIndex(0)
        self.filter_combo.setCurrentIndex(0)
        self.search_input.clear()
        self.min_input.clear()
        self.max_input.clear()
        self.account_info_group.hide()
        if self.avl_tree.root:
            self.display_transactions(self.all_transactions)

    def load_transactions(self):
        """Load all transactions into AVL tree and display."""
        start_time = time.perf_counter()

        self.avl_tree = AVLTree()
        transactions = self.parent.db.get_all_transactions()

        self.all_transactions = []
        for trans in transactions:
            trans_data = {
                'id': trans[0],
                'username': trans[1],
                'type': trans[2],
                'amount': trans[3],
                'timestamp': trans[4]
            }
            self.avl_tree.add_transaction(trans_data)
            self.all_transactions.append(trans_data)

        self.display_transactions(self.all_transactions)
        self.stats_label.setText(f'📊 Total Transactions: {len(self.all_transactions)}')

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        self.time_label.setText(f'⏱️ Running Time: {elapsed_time:.6f}s')

    def search_account_info(self, username):
        """Search and display account information."""
        # Get user transactions
        user_transactions = [t for t in self.all_transactions if t['username'].lower() == username.lower()]

        if not user_transactions:
            self.account_info_group.hide()
            return

        # Calculate statistics
        total_deposits = sum(t['amount'] for t in user_transactions if t['type'].lower() == 'deposit')
        total_withdrawals = sum(t['amount'] for t in user_transactions if t['type'].lower() == 'withdraw')
        transaction_count = len(user_transactions)

        # Get current balance from database
        self.parent.db.cursor.execute(
            'SELECT balance, role, created_at FROM accounts WHERE username = ?',
            (username,)
        )
        result = self.parent.db.cursor.fetchone()

        if result:
            current_balance, role, created_at = result
            info_text = f'''
            <b>Username:</b> {username} | <b>Role:</b> {role.upper()} | <b>Member Since:</b> {created_at}<br>
            <b>Current Balance:</b> <span style="color: #2ecc71;">${current_balance:.2f}</span> | 
            <b>Total Transactions:</b> {transaction_count}<br>
            <b>Total Deposits:</b> <span style="color: #2ecc71;">${total_deposits:.2f}</span> | 
            <b>Total Withdrawals:</b> <span style="color: #e74c3c;">${total_withdrawals:.2f}</span>
            '''
            self.account_details.setText(info_text)
            self.account_info_group.show()

    def apply_filter(self):
        """Apply selected filters to transactions."""
        filter_type = self.filter_combo.currentText()
        trans_type = self.type_combo.currentText()
        search_text = self.search_input.text().strip()
        start_time = time.perf_counter()

        try:
            # First, get transactions based on amount filter
            if filter_type == 'All Transactions':
                filtered = self.avl_tree.get_all_sorted()
            elif filter_type == 'Greater Than':
                min_amount = float(self.min_input.text())
                filtered = self.avl_tree.filter_greater_than(min_amount)
            elif filter_type == 'Less Than':
                max_amount = float(self.min_input.text())
                filtered = self.avl_tree.filter_less_than(max_amount)
            elif filter_type == 'Range':
                min_amount = float(self.min_input.text())
                max_amount = float(self.max_input.text())
                if min_amount > max_amount:
                    QMessageBox.warning(self, 'Error', 'Min amount cannot be greater than max amount.')
                    return
                filtered = self.avl_tree.filter_range(min_amount, max_amount)

            # Apply transaction type filter
            if trans_type == 'Deposits Only':
                filtered = [t for t in filtered if t['type'].lower() == 'deposit']
            elif trans_type == 'Withdrawals Only':
                filtered = [t for t in filtered if t['type'].lower() == 'withdraw']

            # Apply username search filter
            if search_text:
                filtered = [t for t in filtered if search_text.lower() in t['username'].lower()]
                # Show account info if searching
                if filtered:
                    self.search_account_info(filtered[0]['username'])
                else:
                    self.account_info_group.hide()
                    QMessageBox.information(self, 'Search Result', f'No transactions found for username: {search_text}')
            else:
                self.account_info_group.hide()

            self.display_transactions(filtered)

            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            self.time_label.setText(f'⏱️ Running Time: {elapsed_time:.6f}s')

        except ValueError:
            QMessageBox.warning(self, 'Error', 'Please enter valid numeric values.')

    def display_transactions(self, transactions):
        """Populate table with transaction data."""
        self.transaction_table.setRowCount(len(transactions))
        self.result_count_label.setText(f'Showing: {len(transactions)} transactions')

        for row, trans in enumerate(transactions):
            self.transaction_table.setItem(row, 0, QTableWidgetItem(str(trans['id'])))
            self.transaction_table.setItem(row, 1, QTableWidgetItem(trans['username']))

            trans_type = trans['type'].upper()
            type_item = QTableWidgetItem(trans_type)
            if trans_type == 'DEPOSIT':
                type_item.setForeground(Qt.GlobalColor.green)
            else:
                type_item.setForeground(Qt.GlobalColor.red)
            self.transaction_table.setItem(row, 2, type_item)

            self.transaction_table.setItem(row, 3, QTableWidgetItem(f"${trans['amount']:.2f}"))
            self.transaction_table.setItem(row, 4, QTableWidgetItem(trans['timestamp']))

    def logout(self):
        """Logout admin."""
        self.parent.set_current_user(None)
        self.parent.show_login_panel()