import csv
import mysql.connector
from decimal import Decimal

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
CREATE TABLE IF NOT EXISTS median_dom_state_by_type (
    state VARCHAR(255),
    property_type VARCHAR(255),
    median_dom DECIMAL(10, 1)
)
"""
cursor.execute(create_table_sql)

# Open the CSV file
with open('/home/cs179g/workspace/data/days_on_market/median_dom_by_type.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for row in csvreader:
        # Extract values from the row
        state = row[0]
        property_type = row[1]
        median_dom_str = row[2]
        
        # Convert median_dom to Decimal
        median_dom = Decimal(median_dom_str)
        
        # Construct the INSERT INTO statement
        sql = "INSERT INTO median_dom_state_by_type (state, property_type, median_dom) VALUES (%s, %s, %s)"
        values = (state, property_type, median_dom)
        
        # Execute the INSERT INTO statement
        cursor.execute(sql, values)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
