import csv
import mysql.connector
from decimal import Decimal

def preprocess_numeric_value(value):
    # Replace any non-standard decimal separators with standard '.'
    return value.replace(',', '')

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='group4',
    database='group4_db'
)
cursor = conn.cursor()

# Create MySQL table
create_table_sql = """
CREATE TABLE IF NOT EXISTS avg_price_change_region (
    region VARCHAR(255),
    avg_price_change DECIMAL(20, 10)
)
"""
cursor.execute(create_table_sql)

# Open the CSV file
with open('/home/cs179g/workspace/data/price_deduction/price_change_by_region2.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for row in csvreader:
        # Extract values from the row
        region = row[0]
        avg_price_change_str = row[1]
        avg_price_change_str = preprocess_numeric_value(avg_price_change_str)
        if avg_price_change_str:
            avg_price_change = Decimal(avg_price_change_str)
            # Construct the INSERT INTO statement
            sql = "INSERT INTO avg_price_change_region (region, avg_price_change) VALUES (%s, %s)"
            values = (region, avg_price_change)
            
            # Execute the INSERT INTO statement
            cursor.execute(sql, values)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
