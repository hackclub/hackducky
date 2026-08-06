import os
import shutil
import sqlite3
import json

import pyuac

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
    else:
        os.system("Icacls 'c:\\Users\\khale\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies' /t /e /g everyone:F")

def get_table_data(conn):
    cursor = conn.cursor()

    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Store table data
    data = {}
    for table in tables:
        table_name = table[0].decode()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Convert rows to list of dictionaries
        table_data = []
        for row in rows:
            row_dict = {}
            for idx, column in enumerate(cursor.description):
                try:
                    dec = row[idx].decode('latin1')
                except:
                    dec = row[idx]

                row_dict[column[0]] = dec
            table_data.append(row_dict)

        data[table_name] = table_data

    cursor.close()
    return data

def get_db_connection(db_path):
    print(os.path.isfile(db_path))
    file_name = os.path.basename(db_path)
    shutil.copy2(db_path, file_name) 
    return file_name, sqlite3.connect(file_name)

# Connect to the SQLite database (replace 'your_database.db' with your database file)
n, conn = get_db_connection('c:\\Users\\khale\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies')
conn.text_factory = bytes

# Retrieve table data
table_data = get_table_data(conn)

# Close the connection
conn.close()

# Convert data to JSON format
json_data = json.dumps(table_data, indent=2)  # 'indent' for pretty formatting (optional)

# Save JSON data to a file or do whatever you need with it
with open('lab_res.json', 'w') as json_file:
    json_file.write(json_data)
