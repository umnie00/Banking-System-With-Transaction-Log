from dataclasses import dataclass


@dataclass
class Transaction:
    """Transaction model."""
    id: int
    username: str
    type: str  # 'deposit' or 'withdraw'
    amount: float
    timestamp: str

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'type': self.type,
            'amount': self.amount,
            'timestamp': self.timestamp
        }