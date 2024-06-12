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

# Create MySQL table if not exists
create_table_sql = """
CREATE TABLE IF NOT EXISTS statesAndRegions (
    state VARCHAR(255),
    region VARCHAR(255)
)
"""
cursor.execute(create_table_sql)

# Open the CSV file and insert data into the MySQL table
with open('/home/cs179g/workspace/data/average_list_price_by_state.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for row in csvreader:
        # Extract values from the row
        state = row[0]
        region = row[1]
        
        # SQL statement to insert values into the table
        sql = "INSERT INTO statesAndRegions (state, region) VALUES (%s, %s)"
        values = (state, region)
        
        # Execute the SQL statement
        cursor.execute(sql, values)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully.")
