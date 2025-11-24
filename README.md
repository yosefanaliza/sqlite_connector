# ClassicModels SQLite Connector

A Python application demonstrating SQLite database operations with the ClassicModels database schema. Features a clean Data Access Layer (DAL) architecture with simplified connection management.

## Features

- ✅ **Zero configuration** - No database server required
- ✅ **File-based database** - Single SQLite file
- ✅ **Built-in Python support** - Uses sqlite3 standard library
- ✅ **Data Access Layer (DAL)** for clean separation of concerns
- ✅ **Parameterized queries** for SQL injection prevention
- ✅ **Environment configuration** using python-dotenv
- ✅ **Database initialization** script with sample data
- ✅ **Foreign key constraints** enforced
- ✅ **Performance indexes** on common queries

## Project Structure

```
sql-connector/
├── db/
│   ├── __init__.py           # Database package exports
│   └── connection.py         # SQLite connection management
├── dal/                       # Data Access Layer
│   ├── __init__.py           # DAL package exports
│   ├── customer_dal.py       # Customer CRUD operations
│   └── order_dal.py          # Order & OrderDetails operations
├── main.py                    # Demo application
├── init_db.py                 # Database initialization script
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (gitignored)
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Quick Start

### 1. Install Dependencies

```powershell
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Initialize Database

```powershell
python init_db.py
```

This creates the ClassicModels database with:
- All necessary tables (customers, orders, orderdetails, products, etc.)
- Foreign key constraints
- Performance indexes
- Optional sample data for testing

### 3. Configure Environment (Optional)

Create a `.env` file to customize the database location:

```env
DB_PATH=classicmodels.db
```

If not set, defaults to `classicmodels.db` in the project root.

### 4. Run the Application

```powershell
python main.py
```

## Usage

### Basic Connection

```python
from db import get_connection

# Get a connection
connection = get_connection()

if connection:
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM customers LIMIT 5")
        results = cursor.fetchall()
        
        for row in results:
            print(row)
        
        cursor.close()
    finally:
        connection.close()
```

### Using the Data Access Layer

```python
from db import get_connection
from dal import (
    get_customers_by_country,
    get_all_orders,
    get_order_details
)

connection = get_connection()

if connection:
    try:
        # Get customers from USA
        usa_customers = get_customers_by_country(connection, "USA")
        for customer in usa_customers:
            print(f"Customer: {customer[1]}, City: {customer[5]}")
        
        # Get recent orders
        orders = get_all_orders(connection, limit=10)
        for order in orders:
            print(f"Order #{order[0]}, Status: {order[4]}")
        
        # Get order details
        details = get_order_details(connection, 10100)
        for detail in details:
            print(f"Product: {detail[2]}, Qty: {detail[3]}")
    
    finally:
        connection.close()
```

## Data Access Layer (DAL)

### Customer Operations

```python
from dal import (
    get_all_customers,
    get_customer_by_number,
    get_customers_by_country,
    get_customers_by_sales_rep,
    insert_customer,
    update_customer,
    delete_customer
)

# Query operations
customers = get_all_customers(connection, limit=100)
customer = get_customer_by_number(connection, 103)
usa_customers = get_customers_by_country(connection, "USA")

# Insert new customer
insert_customer(
    connection,
    customer_number=999,
    customer_name="New Company",
    contact_last_name="Doe",
    contact_first_name="John",
    phone="555-1234",
    address_line1="123 Main St",
    city="New York",
    country="USA"
)

# Update customer
update_customer(connection, 999, creditLimit=50000.00, phone="555-5678")

# Delete customer
delete_customer(connection, 999)
```

### Order Operations

```python
from dal import (
    get_all_orders,
    get_order_by_number,
    get_orders_by_customer,
    get_orders_by_status,
    get_order_details,
    insert_order,
    update_order_status
)

# Query operations
orders = get_all_orders(connection, limit=50)
order = get_order_by_number(connection, 10100)
customer_orders = get_orders_by_customer(connection, 103)
shipped_orders = get_orders_by_status(connection, "Shipped")
details = get_order_details(connection, 10100)

# Insert new order
from datetime import date
insert_order(
    connection,
    order_number=10500,
    order_date=date(2023, 11, 1),
    required_date=date(2023, 11, 10),
    customer_number=103,
    status="In Process"
)

# Update order status
update_order_status(connection, 10500, "Shipped", shipped_date=date(2023, 11, 5))
```

## Database Schema

### Main Tables

| Table | Description |
|-------|-------------|
| **customers** | Customer information, contacts, and credit limits |
| **orders** | Order headers with dates and status |
| **orderdetails** | Line items for each order (products, quantities, prices) |
| **products** | Product catalog with pricing |
| **productlines** | Product categories |
| **employees** | Sales representatives and staff |
| **offices** | Company office locations |
| **payments** | Customer payment records |

### Key Features

- **Foreign Key Constraints**: Referential integrity enforced
- **Indexes**: Optimized for common queries (country, customer, status, dates)
- **Proper Data Types**: INTEGER, REAL, TEXT, DATE
- **Cascading**: Proper CASCADE rules on foreign keys

## Architecture

### Connection Management

The `db/connection.py` module provides:
- Simple `get_connection()` function
- Automatic foreign key constraint enabling
- Error handling with informative messages
- Environment-based database path configuration

```python
def get_connection():
    """Create and return a SQLite database connection."""
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute('PRAGMA foreign_keys = ON')
        return connection
    except sqlite3.Error as err:
        print(f"Error connecting to database: {err}")
        return None
```

### Data Access Layer Pattern

Benefits:
- **Separation of concerns**: Database logic isolated from business logic
- **Reusable functions**: Common operations encapsulated
- **Type safety**: Proper type hints for all parameters
- **Error handling**: Consistent error messages and rollback logic
- **Parameterized queries**: Protection against SQL injection using `?` placeholders

### SQLite Advantages

- **No Server**: SQLite is serverless, no installation or setup required
- **Zero Configuration**: Works out of the box with Python
- **Single File**: Entire database in one `.db` file
- **Portable**: Easy to backup, move, or version control
- **Fast**: Excellent performance for read-heavy workloads
- **Reliable**: ACID-compliant, battle-tested in production

## Database Initialization

The `init_db.py` script creates the complete ClassicModels schema:

```powershell
python init_db.py
```

**Features:**
- Creates all tables with proper constraints
- Sets up foreign key relationships
- Creates performance indexes
- Optionally inserts sample data
- Checks for existing database and prompts before overwriting

## Security Best Practices

- ✅ **Environment variables**: Database path configurable via `.env`
- ✅ **Parameterized queries**: All SQL uses `?` placeholders
- ✅ **No hardcoded paths**: Configuration separated from code
- ✅ **Foreign key enforcement**: Data integrity maintained
- ✅ **Error handling**: No sensitive data in error messages
- ✅ **Transaction support**: Proper commit/rollback on errors

## Requirements

- Python 3.7+
- python-dotenv (for environment variables)

**That's it!** SQLite is included with Python, no database server needed.

## Dependencies

```
python-dotenv==1.2.1
```

SQLite3 is part of the Python standard library.

## Performance Tips

1. **Use Indexes**: Already created for common queries
2. **Batch Inserts**: Use `executemany()` for multiple inserts
3. **Transactions**: Wrap multiple operations in transactions
4. **Connection Reuse**: Reuse connections instead of creating new ones
5. **PRAGMA Optimization**: Consider `PRAGMA journal_mode=WAL` for concurrent reads

## Limitations

SQLite is excellent for:
- ✅ Development and testing
- ✅ Small to medium datasets (< 100GB)
- ✅ Read-heavy workloads
- ✅ Single-user or low-concurrency applications
- ✅ Embedded applications

Consider MySQL/PostgreSQL for:
- ❌ High concurrency (many simultaneous writes)
- ❌ Very large datasets (> 100GB)
- ❌ Distributed systems
- ❌ Multiple concurrent writers

## Troubleshooting

**Database not found:**
```powershell
python init_db.py
```

**Foreign key constraint errors:**
Ensure referenced records exist before inserting dependent records.

**Empty query results:**
Initialize with sample data using `init_db.py` and select "y" when prompted.

**Permission errors:**
Check write permissions in the directory where the database is created.

## License

This is a demonstration project for educational purposes.

## Contributing

Feel free to submit issues or pull requests to improve this project.

## Repository

GitHub: [https://github.com/yosefanaliza/sqlite_connector](https://github.com/yosefanaliza/sqlite_connector)
