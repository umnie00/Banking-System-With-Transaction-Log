from dataclasses import dataclass


@dataclass
class User:
    """User model."""
    id: int
    username: str
    role: str  # 'admin' or 'user'
    balance: float
    created_at: str

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'balance': self.balance,
            'created_at': self.created_at
        }