import sqlite3
from config import DB_NAME, DEFAULT_USERS, get_timestamp
from models.user import User



class DatabaseManager:
    """Handles all database operations."""

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.init_database()

    def init_database(self):
        """Initialize database tables."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                balance REAL DEFAULT 0.0,
                created_at TEXT DEFAULT ''
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (account_id) REFERENCES accounts (id)
            )
        """)

        self.conn.commit()
        self._seed_default_users()

    def _seed_default_users(self):
        """Add default users if they don't exist."""
        for user in DEFAULT_USERS:
            try:
                self.cursor.execute("""
                    INSERT INTO accounts (username, password, role, balance, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (user['username'], user['password'], user['role'],
                      user['balance'], get_timestamp()))
                self.conn.commit()
            except sqlite3.IntegrityError:
                pass

    def authenticate(self, username, password):
        """Authenticate user and return User object."""
        self.cursor.execute("""
            SELECT id, username, role, balance, created_at FROM accounts
            WHERE username = ? AND password = ?
        """, (username, password))
        result = self.cursor.fetchone()
        return User(*result) if result else None

    def register_user(self, username, password, initial_balance=0.0):
        """Register new user."""
        try:
            self.cursor.execute("""
                INSERT INTO accounts (username, password, role, balance, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (username, password, 'user', initial_balance, get_timestamp()))
            self.conn.commit()
            return True, "Registration successful!"
        except sqlite3.IntegrityError:
            return False, "Username already exists!"

    def get_user(self, user_id):
        """Get user by ID."""
        self.cursor.execute("""
            SELECT id, username, role, balance, created_at FROM accounts WHERE id = ?
        """, (user_id,))
        result = self.cursor.fetchone()
        return User(*result) if result else None

    def get_balance(self, account_id):
        """Get user balance."""
        self.cursor.execute('SELECT balance FROM accounts WHERE id = ?', (account_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0.0

    def update_balance(self, account_id, new_balance):
        """Update user balance."""
        self.cursor.execute(
            'UPDATE accounts SET balance = ? WHERE id = ?',
            (new_balance, account_id)
        )
        self.conn.commit()

    def add_transaction(self, account_id, trans_type, amount):
        """Add new transaction."""
        self.cursor.execute("""
            INSERT INTO transactions (account_id, type, amount, timestamp)
            VALUES (?, ?, ?, ?)
        """, (account_id, trans_type, amount, get_timestamp()))
        self.conn.commit()

    def get_user_transactions(self, account_id):
        """Get transactions for specific user."""
        self.cursor.execute("""
            SELECT transaction_id, type, amount, timestamp
            FROM transactions
            WHERE account_id = ?
            ORDER BY transaction_id DESC
        """, (account_id,))
        return self.cursor.fetchall()

    def get_all_transactions(self):
        """Get all transactions with usernames."""
        self.cursor.execute("""
            SELECT t.transaction_id, a.username, t.type, t.amount, t.timestamp
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            ORDER BY t.transaction_id DESC
        """)
        return self.cursor.fetchall()

    def close(self):
        """Close database connection."""
        self.conn.close()