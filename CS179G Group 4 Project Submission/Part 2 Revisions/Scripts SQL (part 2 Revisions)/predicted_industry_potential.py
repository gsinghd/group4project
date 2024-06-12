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

# Ensure the table is already created
create_table_sql = """
CREATE TABLE IF NOT EXISTS industry_potential (
    region VARCHAR(255),
    predicted_industry_potential FLOAT
)
"""
cursor.execute(create_table_sql)

# Open the CSV file
with open('/home/cs179g/workspace/spark-3.5.1-bin-hadoop3/gs_ml_analysis/predicted_industry_potential.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for row in csvreader:
        # Extract only the first (region) and the last (predicted_industry_potential) values
        region = row[0]
        predicted_growth = float(row[-1])  # Access the last element for predicted industry potential
        
        # Construct the INSERT INTO statement
        sql = "INSERT INTO industry_potential (region, predicted_industry_potential) VALUES (%s, %s)"
        values = (region, predicted_growth)
        
        # Execute the INSERT INTO statement
        cursor.execute(sql, values)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
