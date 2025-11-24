"""
Database initialization script for ClassicModels SQLite database.
Creates all necessary tables with proper schema and constraints.
"""

import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv('DB_PATH', 'classicmodels.db')


def create_database():
    """Create the ClassicModels database schema."""
    
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    # Enable foreign key constraints
    cursor.execute('PRAGMA foreign_keys = ON')
    
    print("Creating ClassicModels database schema...")
    
    # Create offices table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS offices (
        officeCode VARCHAR(10) PRIMARY KEY,
        city VARCHAR(50) NOT NULL,
        phone VARCHAR(50) NOT NULL,
        addressLine1 VARCHAR(50) NOT NULL,
        addressLine2 VARCHAR(50),
        state VARCHAR(50),
        country VARCHAR(50) NOT NULL,
        postalCode VARCHAR(15) NOT NULL,
        territory VARCHAR(10) NOT NULL
    )
    ''')
    
    # Create employees table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employeeNumber INTEGER PRIMARY KEY,
        lastName VARCHAR(50) NOT NULL,
        firstName VARCHAR(50) NOT NULL,
        extension VARCHAR(10) NOT NULL,
        email VARCHAR(100) NOT NULL,
        officeCode VARCHAR(10) NOT NULL,
        reportsTo INTEGER,
        jobTitle VARCHAR(50) NOT NULL,
        FOREIGN KEY (reportsTo) REFERENCES employees(employeeNumber),
        FOREIGN KEY (officeCode) REFERENCES offices(officeCode)
    )
    ''')
    
    # Create customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customerNumber INTEGER PRIMARY KEY,
        customerName VARCHAR(50) NOT NULL,
        contactLastName VARCHAR(50) NOT NULL,
        contactFirstName VARCHAR(50) NOT NULL,
        phone VARCHAR(50) NOT NULL,
        addressLine1 VARCHAR(50) NOT NULL,
        addressLine2 VARCHAR(50),
        city VARCHAR(50) NOT NULL,
        state VARCHAR(50),
        postalCode VARCHAR(15),
        country VARCHAR(50) NOT NULL,
        salesRepEmployeeNumber INTEGER,
        creditLimit REAL,
        FOREIGN KEY (salesRepEmployeeNumber) REFERENCES employees(employeeNumber)
    )
    ''')
    
    # Create productlines table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productlines (
        productLine VARCHAR(50) PRIMARY KEY,
        textDescription TEXT,
        htmlDescription TEXT,
        image BLOB
    )
    ''')
    
    # Create products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        productCode VARCHAR(15) PRIMARY KEY,
        productName VARCHAR(70) NOT NULL,
        productLine VARCHAR(50) NOT NULL,
        productScale VARCHAR(10) NOT NULL,
        productVendor VARCHAR(50) NOT NULL,
        productDescription TEXT NOT NULL,
        quantityInStock INTEGER NOT NULL,
        buyPrice REAL NOT NULL,
        MSRP REAL NOT NULL,
        FOREIGN KEY (productLine) REFERENCES productlines(productLine)
    )
    ''')
    
    # Create orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        orderNumber INTEGER PRIMARY KEY,
        orderDate DATE NOT NULL,
        requiredDate DATE NOT NULL,
        shippedDate DATE,
        status VARCHAR(15) NOT NULL,
        comments TEXT,
        customerNumber INTEGER NOT NULL,
        FOREIGN KEY (customerNumber) REFERENCES customers(customerNumber)
    )
    ''')
    
    # Create orderdetails table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orderdetails (
        orderNumber INTEGER NOT NULL,
        productCode VARCHAR(15) NOT NULL,
        quantityOrdered INTEGER NOT NULL,
        priceEach REAL NOT NULL,
        orderLineNumber INTEGER NOT NULL,
        PRIMARY KEY (orderNumber, productCode),
        FOREIGN KEY (orderNumber) REFERENCES orders(orderNumber),
        FOREIGN KEY (productCode) REFERENCES products(productCode)
    )
    ''')
    
    # Create payments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        customerNumber INTEGER NOT NULL,
        checkNumber VARCHAR(50) NOT NULL,
        paymentDate DATE NOT NULL,
        amount REAL NOT NULL,
        PRIMARY KEY (customerNumber, checkNumber),
        FOREIGN KEY (customerNumber) REFERENCES customers(customerNumber)
    )
    ''')
    
    connection.commit()
    print(f"Database schema created successfully at: {DB_PATH}")
    
    # Create indexes for performance
    print("Creating indexes...")
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_customers_country ON customers(country)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_customers_salesrep ON customers(salesRepEmployeeNumber)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customerNumber)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(orderDate)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_orderdetails_product ON orderdetails(productCode)')
    
    connection.commit()
    print("Indexes created successfully")
    
    cursor.close()
    connection.close()
    
    print(f"\n✓ Database initialization complete!")
    print(f"  Database location: {os.path.abspath(DB_PATH)}")
    print(f"\n  You can now populate this database with your ClassicModels data.")


def insert_sample_data():
    """Insert sample data for testing (optional)."""
    
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    print("\nInserting sample data...")
    
    # Sample customers
    sample_customers = [
        (103, 'Atelier graphique', 'Schmitt', 'Carine', '40.32.2555', '54, rue Royale', None, 'Nantes', None, '44000', 'France', 1370, 21000.00),
        (112, 'Signal Gift Stores', 'King', 'Jean', '7025551838', '8489 Strong St.', None, 'Las Vegas', 'NV', '83030', 'USA', 1166, 71800.00),
        (114, 'Australian Collectors, Co.', 'Ferguson', 'Peter', '03 9520 4555', '636 St Kilda Road', 'Level 3', 'Melbourne', 'Victoria', '3004', 'Australia', 1611, 117300.00),
    ]
    
    try:
        cursor.executemany('''
            INSERT OR IGNORE INTO customers 
            (customerNumber, customerName, contactLastName, contactFirstName, phone, 
             addressLine1, addressLine2, city, state, postalCode, country, 
             salesRepEmployeeNumber, creditLimit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_customers)
        
        # Sample orders
        sample_orders = [
            (10100, '2023-01-06', '2023-01-13', '2023-01-10', 'Shipped', None, 103),
            (10101, '2023-01-09', '2023-01-18', '2023-01-11', 'Shipped', 'Check on availability.', 112),
            (10102, '2023-01-10', '2023-01-18', '2023-01-14', 'Shipped', None, 114),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO orders 
            (orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_orders)
        
        connection.commit()
        print(f"Sample data inserted: {len(sample_customers)} customers, {len(sample_orders)} orders")
        
    except sqlite3.Error as e:
        print(f"Error inserting sample data: {e}")
        connection.rollback()
    
    cursor.close()
    connection.close()


if __name__ == "__main__":
    print("=" * 60)
    print("ClassicModels SQLite Database Initialization")
    print("=" * 60)
    
    # Check if database already exists
    if os.path.exists(DB_PATH):
        response = input(f"\nDatabase '{DB_PATH}' already exists. Recreate it? (y/n): ")
        if response.lower() != 'y':
            print("Initialization cancelled.")
            exit()
        else:
            os.remove(DB_PATH)
            print(f"Removed existing database: {DB_PATH}")
    
    create_database()
    
    # Ask if user wants sample data
    response = input("\nWould you like to insert sample data? (y/n): ")
    if response.lower() == 'y':
        insert_sample_data()
    
    print("\n" + "=" * 60)
    print("Initialization complete!")
    print("=" * 60)
