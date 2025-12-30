import sys
import os

# Ensure src is in path
sys.path.append(os.getcwd())

from src.db import db

def add_column_if_not_exists(cursor, table, column, definition):
    try:
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' AND COLUMN_NAME = '{column}'")
        if not cursor.fetchone():
            print(f"Adding column {column} to {table}...")
            cursor.execute(f"ALTER TABLE {table} ADD {column} {definition}")
            print(f"Column {column} added.")
        else:
            print(f"Column {column} already exists in {table}.")
    except Exception as e:
        print(f"Error checking/adding column {column}: {e}")

try:
    cursor = db.connection.cursor()
    
    # Corrected list of definitions
    definitions = [
        ('first_name', 'VARCHAR(50) NULL'),
        ('last_name', 'VARCHAR(50) NULL'),
        ('phone', 'VARCHAR(20) NULL'),
        ('email', 'VARCHAR(100) NULL')
    ]
    
    for col, definition in definitions:
        add_column_if_not_exists(cursor, 'Users', col, definition)
        
    db.connection.commit()
    print("Schema update completed.")

except Exception as e:
    print(f"Database error: {e}")
    if db.connection:
        db.connection.rollback()
