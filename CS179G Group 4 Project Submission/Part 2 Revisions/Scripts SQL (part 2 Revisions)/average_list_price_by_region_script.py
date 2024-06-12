import csv
import mysql.connector

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
CREATE TABLE IF NOT EXISTS average_list_price_by_region (
    region VARCHAR(255),
    avg_median_list_price DECIMAL(20, 10)
)
"""
cursor.execute(create_table_sql)

# Open the CSV file
with open('/home/cs179g/workspace/data/average_list_price_by_region.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for row in csvreader:
        # Extract values from the row
        state = row[0]
        avg_median_list_price_str = row[1]
        # Skip rows with empty values in the second column
        if avg_median_list_price_str:
            avg_median_list_price = float(avg_median_list_price_str)  # Convert to float
            # Construct the INSERT INTO statement
            sql = "INSERT INTO average_list_price_by_region (region, avg_median_list_price) VALUES (%s, %s)"
            values = (state, avg_median_list_price)
            # Execute the INSERT INTO statement
            cursor.execute(sql, values)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()