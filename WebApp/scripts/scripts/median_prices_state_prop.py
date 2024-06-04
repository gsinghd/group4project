import csv
import mysql.connector
from decimal import Decimal

# Function to preprocess numeric values
def preprocess_numeric_value(value):
    return value.replace(',', '')

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='group4',
    database='group4_db'
)
cursor = conn.cursor()

# Create MySQL table if not exists
create_table_sql = """
CREATE TABLE IF NOT EXISTS median_prices_state_prop (
    state VARCHAR(255),
    property_type VARCHAR(255),
    avg_median_sale_price DECIMAL(20, 10),
    avg_median_list_price DECIMAL(20, 10),
    avg_median_ppsf DECIMAL(20, 10)
)
"""
cursor.execute(create_table_sql)

# Open the CSV file and insert data into MySQL
with open('/home/cs179g/workspace/data/average_by_prop_type_state.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for row in csvreader:
        # Extract values from the row
        state = row[0]
        property_type = row[1]
        avg_median_sale_price_str = preprocess_numeric_value(row[2])
        avg_median_list_price_str = preprocess_numeric_value(row[3])
        avg_median_ppsf_str = preprocess_numeric_value(row[4])

        # Check for empty strings or non-numeric values
        if avg_median_sale_price_str.strip() and avg_median_sale_price_str.replace('.', '').isdigit():
            avg_median_sale_price = Decimal(avg_median_sale_price_str)
        else:
            avg_median_sale_price = None

        # Check for empty strings or non-numeric values
        if avg_median_list_price_str.strip() and avg_median_list_price_str.replace('.', '').isdigit():
            avg_median_list_price = Decimal(avg_median_list_price_str)
        else:
            avg_median_list_price = None

        # Check for empty strings or non-numeric values
        if avg_median_ppsf_str.strip() and avg_median_ppsf_str.replace('.', '').isdigit():
            avg_median_ppsf = Decimal(avg_median_ppsf_str)
        else:
            avg_median_ppsf = None

        # Construct the INSERT INTO statement
        sql = "INSERT INTO median_prices_state_prop (state, property_type, avg_median_sale_price, avg_median_list_price, avg_median_ppsf) VALUES (%s, %s, %s, %s, %s)"
        values = (state, property_type, avg_median_sale_price, avg_median_list_price, avg_median_ppsf)

        # Execute the INSERT INTO statement
        cursor.execute(sql, values)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
