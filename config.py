from datetime import datetime

# Database
DB_NAME = 'banking_system.db'

# Default Users
DEFAULT_USERS = [
    {'username': 'admin', 'password': 'admin123', 'role': 'admin', 'balance': 0.0},
    {'username': 'user', 'password': 'user123', 'role': 'user', 'balance': 1000.0}
]

# Validation
MIN_USERNAME_LENGTH = 3
MIN_PASSWORD_LENGTH = 4

# Utility
def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')