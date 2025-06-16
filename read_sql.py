import sqlite3
from tabulate import tabulate  # Optional for table formatting

# Connect to the database file
conn = sqlite3.connect('models/employees.db')  # Replace with your actual .db file
cursor = conn.cursor()

# Get table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table_name in tables:
    table = table_name[0]
    print(f"\n=== Table: {table} ===")

    # Fetch column names
    cursor.execute(f"PRAGMA table_info({table});")
    col_info = cursor.fetchall()
    col_names = [col[1] for col in col_info]

    # Fetch all rows
    cursor.execute(f"SELECT * FROM {table};")
    rows = cursor.fetchall()

    # Print using tabulate or plain print
    if rows:
        print(tabulate(rows, headers=col_names, tablefmt='grid'))  # Pretty table
    else:
        print("Table is empty.")

# Close connection
conn.close()
