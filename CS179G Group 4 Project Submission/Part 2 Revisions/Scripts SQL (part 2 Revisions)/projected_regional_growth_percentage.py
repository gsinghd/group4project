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
CREATE TABLE IF NOT EXISTS regional_growth (
    region VARCHAR(255),
    predicted_regional_growth FLOAT
)
"""
cursor.execute(create_table_sql)

# Open the CSV file
with open('/home/cs179g/workspace/spark-3.5.1-bin-hadoop3/gs_ml_analysis/projected_regional_growth_percent.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for row in csvreader:
        # Extract values from the row
        region = row[0]
        predicted_growth = float(row[1])
        
        # Construct the INSERT INTO statement
        sql = "INSERT INTO regional_growth (region, predicted_regional_growth) VALUES (%s, %s)"
        values = (region, predicted_growth)
        
        # Execute the INSERT INTO statement
        cursor.execute(sql, values)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
