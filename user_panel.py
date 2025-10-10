from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QHeaderView)
from PyQt6.QtCore import Qt


class UserPanel(QWidget):
    """User dashboard UI."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        header = QHBoxLayout()
        user = self.parent.current_user
        title = QLabel(' Dashboard')
        title.setObjectName('titleLabel')
        header.addWidget(title)
        header.addStretch()

        self.username_label = QLabel()
        self.username_label.setStyleSheet('font-size: 14px; color: #00d4ff;')
        header.addWidget(self.username_label)

        logout_btn = QPushButton('Logout')
        logout_btn.setObjectName('logoutButton')
        logout_btn.clicked.connect(self.logout)
        header.addWidget(logout_btn)
        layout.addLayout(header)

        self.balance_label = QLabel()
        self.balance_label.setObjectName('subtitleLabel')
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.balance_label)

        trans_layout = QHBoxLayout()
        amount_label = QLabel('Amount:')
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('Enter amount')
        trans_layout.addWidget(amount_label)
        trans_layout.addWidget(self.amount_input)

        deposit_btn = QPushButton('Deposit')
        deposit_btn.setObjectName('depositButton')
        deposit_btn.clicked.connect(self.deposit)
        trans_layout.addWidget(deposit_btn)

        withdraw_btn = QPushButton('Withdraw')
        withdraw_btn.setObjectName('withdrawButton')
        withdraw_btn.clicked.connect(self.withdraw)
        trans_layout.addWidget(withdraw_btn)

        layout.addLayout(trans_layout)

        history_label = QLabel('Transaction History:')
        history_label.setObjectName('subtitleLabel')
        layout.addWidget(history_label)

        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(4)
        self.transaction_table.setHorizontalHeaderLabels(['ID', 'Type', 'Amount', 'Timestamp'])
        self.transaction_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.transaction_table.setAlternatingRowColors(True)
        self.transaction_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.transaction_table)

        self.setLayout(layout)

    def update_display(self):
        """Refresh user display with current data."""
        user = self.parent.current_user
        self.username_label.setText(f'😏 {user.username}')
        balance = self.parent.db.get_balance(user.id)
        self.balance_label.setText(f'🤑 Current Balance: ₱{balance:.2f}')

        transactions = self.parent.db.get_user_transactions(user.id)
        self.transaction_table.setRowCount(len(transactions))

        for row, trans in enumerate(transactions):
            self.transaction_table.setItem(row, 0, QTableWidgetItem(str(trans[0])))

            trans_type = trans[1].upper()
            type_item = QTableWidgetItem(trans_type)
            if trans_type == 'DEPOSIT':
                type_item.setForeground(Qt.GlobalColor.green)
            else:
                type_item.setForeground(Qt.GlobalColor.red)
            self.transaction_table.setItem(row, 1, type_item)

            self.transaction_table.setItem(row, 2, QTableWidgetItem(f'₱{trans[2]:.2f}'))
            self.transaction_table.setItem(row, 3, QTableWidgetItem(trans[3]))

    def deposit(self):
        """Handle deposit transaction."""
        try:
            amount = float(self.amount_input.text())
            if amount <= 0:
                QMessageBox.warning(self, 'Error', 'Amount must be positive.')
                return

            user_id = self.parent.current_user.id
            current_balance = self.parent.db.get_balance(user_id)
            new_balance = current_balance + amount

            self.parent.db.update_balance(user_id, new_balance)
            self.parent.db.add_transaction(user_id, 'deposit', amount)

            QMessageBox.information(self, 'Success', f'Deposited ${amount:.2f} successfully!')
            self.amount_input.clear()
            self.update_display()
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Please enter a valid amount.')

    def withdraw(self):
        """Handle withdrawal transaction."""
        try:
            amount = float(self.amount_input.text())
            if amount <= 0:
                QMessageBox.warning(self, 'Error', 'Amount must be positive.')
                return

            user_id = self.parent.current_user.id
            current_balance = self.parent.db.get_balance(user_id)

            if amount > current_balance:
                QMessageBox.warning(self, 'Error', 'Insufficient balance.')
                return

            new_balance = current_balance - amount
            self.parent.db.update_balance(user_id, new_balance)
            self.parent.db.add_transaction(user_id, 'withdraw', amount)

            QMessageBox.information(self, 'Success', f'Withdrew ${amount:.2f} successfully!')
            self.amount_input.clear()
            self.update_display()
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Please enter a valid amount.')

    def logout(self):
        """Logout user."""
        self.parent.set_current_user(None)
        self.parent.show_login_panel()