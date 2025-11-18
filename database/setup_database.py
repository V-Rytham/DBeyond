import sqlite3
import os

def setup_database():
    """Create and populate sample database for quantum SQL optimizer"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'sample.db')
    
    # Remove existing database to start fresh
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Create connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Creating tables...")
    
    # Create customers table
    cursor.execute('''
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        country TEXT
    )
    ''')
    
    # Create orders table
    cursor.execute('''
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        order_date TEXT,
        total_amount REAL,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
    ''')
    
    # Create products table
    cursor.execute('''
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_name TEXT,
        price REAL,
        quantity INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders(id)
    )
    ''')
    
    print("Inserting sample data...")
    
    # Insert sample customers
    customers = [
        (1, 'Alice Johnson', 'alice@example.com', 'USA'),
        (2, 'Bob Smith', 'bob@example.com', 'UK'),
        (3, 'Charlie Brown', 'charlie@example.com', 'USA'),
        (4, 'Diana Prince', 'diana@example.com', 'Canada'),
        (5, 'Eve Wilson', 'eve@example.com', 'Australia'),
    ]
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?)', customers)
    
    # Insert sample orders
    orders = [
        (1, 1, '2024-01-15', 150.00),
        (2, 1, '2024-02-20', 200.00),
        (3, 2, '2024-01-25', 75.50),
        (4, 3, '2024-02-10', 300.00),
        (5, 3, '2024-03-05', 125.00),
    ]
    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?)', orders)
    
    # Insert sample products
    products = [
        (1, 1, 'Laptop', 800.00, 1),
        (2, 1, 'Mouse', 25.00, 2),
        (3, 2, 'Keyboard', 100.00, 1),
        (4, 3, 'Monitor', 300.00, 1),
        (5, 4, 'Headphones', 120.00, 2),
        (6, 5, 'USB Cable', 15.00, 5),
    ]
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?)', products)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"✓ Database setup complete!")
    print(f"  Location: {db_path}")
    print(f"  Tables: customers (5 rows), orders (5 rows), products (6 rows)")

if __name__ == "__main__":
    setup_database()
