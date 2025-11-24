"""SQLite database connection module."""

import sqlite3

DB_PATH = 'classicmodels.db'

def get_connection():
    """Create and return a SQLite database connection."""
    try:
        connection = sqlite3.connect(DB_PATH)
        # Enable foreign key constraints
        connection.execute('PRAGMA foreign_keys = ON')
        print(f"Successfully connected to database: {DB_PATH}")
        return connection
    except sqlite3.Error as err:
        print(f"Error connecting to database: {err}")
        return None