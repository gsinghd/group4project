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
CREATE TABLE IF NOT EXISTS average_sale_price_by_state (
    state VARCHAR(255),
    avg_median_sale_price DECIMAL(20, 10)
)
"""
cursor.execute(create_table_sql)

# Open the CSV file
with open('/home/cs179g/workspace/data/average_list_price_by_state.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for row in csvreader:
        # Extract values from the row
        state = row[0]
        avg_median_sale_price_str = row[1]
        avg_median_sale_price_str = preprocess_numeric_value(avg_median_sale_price_str)
        # Skip rows with empty values in the second column
        if avg_median_sale_price_str:
            avg_median_sale_price = Decimal(avg_median_sale_price_str)  # Convert to float
            # Construct the INSERT INTO statement
            sql = "INSERT INTO average_sale_price_by_state (state, avg_median_sale_price) VALUES (%s, %s)"
            values = (state, avg_median_sale_price)
            # Execute the INSERT INTO statement
            cursor.execute(sql, values)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()