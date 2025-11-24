"""
Customer Data Access Layer.
Handles all database operations related to customers table.
"""

import sqlite3
from typing import Optional, List, Any


def get_all_customers(connection: sqlite3.Connection,
                      limit: int = 100) -> List[Any]:
    """
    Get all customers from the database.
    
    Args:
        connection: Active SQLite connection
        limit: Maximum number of rows to return
        
    Returns:
        List of customer tuples
    """

    query = '''
    SELECT customerNumber, customerName, contactLastName, contactFirstName, 
           phone, addressLine1, city, country, salesRepEmployeeNumber, creditLimit
    FROM customers
    ORDER BY customerName
    LIMIT ?
    '''
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        cursor.close()
        print(f"Retrieved {len(rows)} customers")
        return rows
    except Exception as err:
        print(f"Failed to query customers: {err}")
        return []


def get_customer_by_number(connection: sqlite3.Connection,
                           customer_number: int) -> Optional[Any]:
    """
    Get a customer by customer number.
    
    Args:
        connection: Active SQLite connection
        customer_number: Customer number
        
    Returns:
        Customer tuple or None if not found
    """
    query = '''
    SELECT customerNumber, customerName, contactLastName, contactFirstName, 
           phone, addressLine1, addressLine2, city, state, postalCode, 
           country, salesRepEmployeeNumber, creditLimit
    FROM customers
    WHERE customerNumber = ?
    '''
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, (customer_number,))
        row = cursor.fetchone()
        cursor.close()
        return row
    except Exception as err:
        print(f"Failed to query customer: {err}")
        return None


def get_customers_by_country(connection: sqlite3.Connection,
                             country: str) -> List[Any]:
    """
    Get customers by country.
    
    Args:
        connection: Active SQLite connection
        country: Country name
        
    Returns:
        List of customer tuples
    """


    query = '''
    SELECT customerNumber, customerName, contactLastName, contactFirstName, 
           phone, city, country
    FROM customers
    WHERE country = ?
    ORDER BY customerName
    '''
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, (country,))
        rows = cursor.fetchall()
        cursor.close()
        print(f"Found {len(rows)} customers in {country}")
        return rows
    except Exception as err:
        print(f"Failed to query customers by country: {err}")
        return []


def get_customers_by_sales_rep(connection: sqlite3.Connection,
                               employee_number: int) -> List[Any]:
    """
    Get customers assigned to a sales representative.
    
    Args:
        connection: Active SQLite connection
        employee_number: Sales rep employee number
        
    Returns:
        List of customer tuples
    """
    query = '''
    SELECT customerNumber, customerName, contactLastName, contactFirstName, 
           phone, city, country, creditLimit
    FROM customers
    WHERE salesRepEmployeeNumber = ?
    ORDER BY customerName
    '''
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, (employee_number,))
        rows = cursor.fetchall()
        cursor.close()
        print(f"Found {len(rows)} customers for sales rep {employee_number}")
        return rows
    except Exception as err:
        print(f"Failed to query customers by sales rep: {err}")
        return []


def insert_customer(connection: sqlite3.Connection,
                   customer_number: int, customer_name: str, contact_last_name: str,
                   contact_first_name: str, phone: str, address_line1: str,
                   city: str, country: str, sales_rep: Optional[int] = None,
                   credit_limit: Optional[float] = None) -> bool:
    """
    Insert a new customer.
    
    Args:
        connection: Active SQLite connection
        customer_number: Unique customer number
        customer_name: Customer company name
        contact_last_name: Contact last name
        contact_first_name: Contact first name
        phone: Phone number
        address_line1: Address line 1
        city: City
        country: Country
        sales_rep: Sales representative employee number (optional)
        credit_limit: Credit limit (optional)
        
    Returns:
        True if successful, False otherwise
    """
    query = '''
    INSERT INTO customers 
    (customerNumber, customerName, contactLastName, contactFirstName, 
     phone, addressLine1, city, country, salesRepEmployeeNumber, creditLimit)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, (customer_number, customer_name, contact_last_name,
                             contact_first_name, phone, address_line1, city,
                             country, sales_rep, credit_limit))
        connection.commit()
        cursor.close()
        print(f"Customer {customer_number} inserted successfully")
        return True
    except Exception as err:
        print(f"Failed to insert customer: {err}")
        connection.rollback()
        return False


def update_customer(connection: sqlite3.Connection,
                   customer_number: int, **kwargs) -> bool:
    """
    Update customer information.
    
    Args:
        connection: Active SQLite connection
        customer_number: Customer number to update
        **kwargs: Fields to update (customerName, phone, creditLimit, etc.)
        
    Returns:
        True if successful, False otherwise
    """
    if not kwargs:
        print("No fields to update")
        return False
    
    set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
    query = f"UPDATE customers SET {set_clause} WHERE customerNumber = ?"
    values = list(kwargs.values()) + [customer_number]
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        if rowcount > 0:
            print(f"Customer {customer_number} updated successfully")
            return True
        else:
            print(f"No customer found with number {customer_number}")
            return False
    except Exception as err:
        print(f"Failed to update customer: {err}")
        connection.rollback()
        return False


def delete_customer(connection: sqlite3.Connection,
                   customer_number: int) -> bool:
    """
    Delete a customer.
    
    Args:
        connection: Active SQLite connection
        customer_number: Customer number to delete
        
    Returns:
        True if successful, False otherwise
    """
    query = "DELETE FROM customers WHERE customerNumber = ?"
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, (customer_number,))
        connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        if rowcount > 0:
            print(f"Customer {customer_number} deleted successfully")
            return True
        else:
            print(f"No customer found with number {customer_number}")
            return False
    except Exception as err:
        print(f"Failed to delete customer: {err}")
        connection.rollback()
        return False
