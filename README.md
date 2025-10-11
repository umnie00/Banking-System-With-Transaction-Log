
Team members’ names and roles:

    JHODENIS M. EDANO - Backend & Data Structures (AVL Tree, filtering logic)
    FAISAL P. SINGCA - Database Design & Management (SQLite, models)
    JOE LANCE M. ODTOHAN - Frontend & UI/UX (PyQt6 interfaces, styling)
    RUMAR BENEDICT S. CIA - Documentation & User Features (User panel, docs)
    AHMADDEDAT J. ISMULA - Documentation & Admin Features (Admin panel, reports)



Project Title: 

      Banking System with Transaction Log

Project Description:

      This Banking System is a full-featured desktop application that provides:

      User Authentication: Secure login and registration system with role-based access (admin/user)
      Account Management: Users can deposit and withdraw funds with real-time balance updates
      Transaction History: Complete logging of all financial transactions
      Admin Dashboard: Advanced filtering and search capabilities for transaction monitoring
      AVL Tree Implementation: Efficient transaction filtering using self-balancing binary search trees
      Modern UI: Sleek, gradient-based interface with custom styling

For Users:

    View current balance
    Make deposits and withdrawals
    View personal transaction history
    Secure password-protected accounts

For Admins:

    View all system transactions
    Filter by transaction type (deposits/withdrawals)
    Filter by amount (greater than, less than, range)
    Search transactions by username
    View detailed account statistics
    Real-time performance metrics

How to Run the Project:


    Python 3.8 or higher
    pip (Python package installer)

Installation Steps:

    Install Required Dependencies

    bash   pip install PyQt6

    Navigate to Project Directory

    bash   cd "PythonProject4_BANKING SYSTEEEEEEEEEEEM"

    Run the Application

    bash   python main.py
    Default Login Credentials
    
Admin Account:

    Username: admin
    Password: admin123

User Account:

    Username: user
    Password: user123

Project Structure:

    PythonProject4_BANKING SYSTEEEEEEEEEEEM/
    │
    ├── main.py                 # Application entry point
    ├── config.py              # Configuration settings
    │
    ├── database/
    │   └── db_manager.py      # Database operations and SQLite management
    │
    ├── models/
    │   ├── user.py            # User data model
    │   └── transaction.py     # Transaction data model
    │
    ├── ui/
    │   ├── main_window.py     # Main application window
    │   ├── login_panel.py     # Login interface
    │   ├── register_panel.py  # Registration interface
    │   ├── user_panel.py      # User dashboard
    │   ├── admin_panel.py     # Admin dashboard with filtering
    │   └── style.py           # UI styling and themes
    │    
    └── data_structure/
    └── avl_tree.py        # AVL tree implementation for filtering

 
 
Usage Guide:
 
    Creating a New Account

    Click the Register button on the login screen
    Enter a username (minimum 3 characters)
    Enter a password (minimum 4 characters)
    Confirm your password
    Optionally set an initial balance
    Click Create Account

    Making Transactions (User)

    Log in with your credentials
    Enter the amount in the input field
    Click Deposit to add funds or Withdraw to remove funds
    View your transaction history in the table below


Admin Features:

    Log in with admin credentials
    Use the filter options to narrow down transactions:

    Transaction Type: Filter by deposits or withdrawals
    Amount Filter: Filter by amount ranges
    Username Search: Find transactions for specific users
    Click Apply Filters to see results
    View performance metrics and transaction statistics


Database:
 
    The application uses SQLite for data persistence. The database file (banking_system.db) is     automatically created on first run and stores:

    User accounts with encrypted passwords
    Transaction history
    Account balances
    Timestamps for all activities

Technical Details:

    Framework: PyQt6 for GUI
    Database: SQLite3
    Data Structure: AVL Tree for efficient transaction filtering
    Architecture: MVC-inspired pattern with separated concerns

Important Notes:

    All monetary values are displayed with 2 decimal precision
    Negative balances are prevented through validation
    Admin accounts can view all transactions but cannot modify them
    The system maintains complete transaction logs for auditing purposes
