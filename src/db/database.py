import sqlite3
import os


# Constants
DB_FILE = os.path.join(os.path.dirname(__file__), "warranty.db")

def get_db_connection() -> sqlite3.Connection:
    """
    Establishes a connection to the SQLite database.
    Returns:
        sqlite3.Connection: A connection object to interact with the database.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        print(f"Connected to the database at {DB_FILE}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        raise

def initialize_database() -> None:
    """
    Initializes the database by creating the required tables.
    """
    create_customers_table = """
    CREATE TABLE IF NOT EXISTS customers (
        rowid INTEGER PRIMARY KEY AUTOINCREMENT, 
        customer_name VARCHAR(50) NOT NULL, 
        city VARCHAR(50) NOT NULL, 
        city_type VARCHAR(1) NOT NULL, 
        contact_person VARCHAR(50) NOT NULL DEFAULT "", 
        phone_number VARCHAR(20) NOT NULL DEFAULT ""
    );
    """

    create_warranty_table = """
    CREATE TABLE IF NOT EXISTS warranty (
        rowid INTEGER PRIMARY KEY AUTOINCREMENT, 
        MSN VARCHAR(20) UNIQUE NOT NULL, 
        customer_id INTEGER NOT NULL, 
        machine_model VARCHAR(10) NOT NULL, 
        installation_date DATE NOT NULL, 
        warranty_duration INTEGER NOT NULL, 
        expiry_date DATE NOT NULL, 
        FOREIGN KEY (customer_id) REFERENCES customers(rowid) ON DELETE CASCADE
    );
    """

    # Connect to the database and execute the schema creation
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(create_customers_table)
        print("Created or verified 'customers' table.")
        cursor.execute(create_warranty_table)
        print("Created or verified 'warranty' table.")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing the database: {e}")
        raise
    finally:
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    # If this script runs directly, initialize the database.
    initialize_database()
    