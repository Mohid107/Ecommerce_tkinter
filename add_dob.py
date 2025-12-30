import sys
import os

# Ensure src is in path
sys.path.append(os.getcwd())

from src.db import db

def add_column(cursor, table, column, definition):
    try:
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' AND COLUMN_NAME = '{column}'")
        if not cursor.fetchone():
            print(f"Adding column {column} to {table}...")
            cursor.execute(f"ALTER TABLE {table} ADD {column} {definition}")
            print(f"Column {column} added.")
        else:
            print(f"Column {column} already exists.")
    except Exception as e:
        print(f"Error adding {column}: {e}")

try:
    cursor = db.connection.cursor()
    add_column(cursor, 'Users', 'dob', 'VARCHAR(20) NULL')
    db.connection.commit()
    print("Schema update completed.")
except Exception as e:
    print(f"Database error: {e}")
