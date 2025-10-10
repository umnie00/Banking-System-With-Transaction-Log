class AVLNode:
    """Node for AVL Tree."""

    def __init__(self, transaction_data):
        self.data = transaction_data
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """Self-balancing binary search tree for transaction filtering."""

    def __init__(self):
        self.root = None

    def get_height(self, node):
        return 0 if not node else node.height

    def get_balance(self, node):
        return 0 if not node else self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, node, transaction_data):
        if not node:
            return AVLNode(transaction_data)

        if transaction_data['amount'] < node.data['amount']:
            node.left = self.insert(node.left, transaction_data)
        else:
            node.right = self.insert(node.right, transaction_data)

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Left-Left case
        if balance > 1 and transaction_data['amount'] < node.left.data['amount']:
            return self.right_rotate(node)

        # Right-Right case
        if balance < -1 and transaction_data['amount'] >= node.right.data['amount']:
            return self.left_rotate(node)

        # Left-Right case
        if balance > 1 and transaction_data['amount'] >= node.left.data['amount']:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right-Left case
        if balance < -1 and transaction_data['amount'] < node.right.data['amount']:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def add_transaction(self, transaction_data):
        """Add transaction to tree."""
        self.root = self.insert(self.root, transaction_data)

    def inorder_traversal(self, node, result_list):
        if node:
            self.inorder_traversal(node.left, result_list)
            result_list.append(node.data)
            self.inorder_traversal(node.right, result_list)

    def search_greater_than(self, node, min_amount, result_list):
        if not node:
            return
        if node.data['amount'] > min_amount:
            self.search_greater_than(node.left, min_amount, result_list)
            result_list.append(node.data)
        self.search_greater_than(node.right, min_amount, result_list)

    def search_less_than(self, node, max_amount, result_list):
        if not node:
            return
        self.search_less_than(node.left, max_amount, result_list)
        if node.data['amount'] < max_amount:
            result_list.append(node.data)
        self.search_less_than(node.right, max_amount, result_list)

    def search_range(self, node, min_amount, max_amount, result_list):
        if not node:
            return
        if node.data['amount'] > min_amount:
            self.search_range(node.left, min_amount, max_amount, result_list)
        if min_amount <= node.data['amount'] <= max_amount:
            result_list.append(node.data)
        if node.data['amount'] < max_amount:
            self.search_range(node.right, min_amount, max_amount, result_list)

    def get_all_sorted(self):
        result = []
        self.inorder_traversal(self.root, result)
        return result

    def filter_greater_than(self, min_amount):
        result = []
        self.search_greater_than(self.root, min_amount, result)
        return result

    def filter_less_than(self, max_amount):
        result = []
        self.search_less_than(self.root, max_amount, result)
        return result

    def filter_range(self, min_amount, max_amount):
        result = []
        self.search_range(self.root, min_amount, max_amount, result)
        return result