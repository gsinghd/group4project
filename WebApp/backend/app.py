from flask import Flask, jsonify, render_template
import csv
import json
import mysql.connector
import requests
from flask_sqlalchemy import SQLAlchemy
import os
import csv

app = Flask(__name__, template_folder='/home/cs179g/repo/WebApp/frontend', static_folder='/home/cs179g/repo/WebApp/frontend/static')

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'group4',
    'database': 'group4_db'
}

'''
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{db_config['user']}:{db_config['password']}@"
    f"{db_config['host']}/{db_config['database']}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


def get_data_from_db():
    data = {}
    tables = [
        'average_list_price_by_region',
        'average_list_price_by_state',
        'average_sale_price_by_region',
        'average_sale_price_by_state',
        'averages_by_prop_type_state',
        'avg_price_change_by_region',
        'avg_price_change_by_state',
        'days_on_market',
        'housing_trajectory',
        'median_ppsf_by_region',
        'median_ppsf_by_state',
        'price_deduction'
    ]

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    for table in tables:
        cursor.execute(f'SELECT * FROM {table}')
        rows = cursor.fetchall()
        data[table] = rows

    cursor.close()
    conn.close()

    return data

@app.route('/data')
def get_data():
    data = get_data_from_db()
    return jsonify(data)

# Route for fetching data from SQL database
@app.route('/data')
def check_mysql_connection():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        conn.close()
        return jsonify({'status': 'MySQL connection successful'})
    except Exception as e:
        return jsonify({'error': 'Failed to connect to MySQL', 'details': str(e)}), 500


#@app.route('/')
#def index():
 #   return render_template('index.html')

@app.route('/')
def index():
    try:
        api_key = 'a079d9415a5350189aaac490f53e02ab605ae922'  # Replace with your actual API key
        endpoint = f'https://api.census.gov/data/2010/dec/sf1?get=P001001,NAME&for=state:*&key={api_key}'

        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()

            # Extract state names and codes from API response
            states = [{'code': state[1], 'name': state[2]} for state in data[1:]]

            # Render HTML template with state data
            return render_template('index.html', states=states)

        else:
            return 'Error fetching data from Census API'

    except Exception as e:
        return f'An error occurred: {str(e)}'
    
@app.route('/api/datasets', methods=['GET'])
def get_datasets():
    # Fetch datasets from the database
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM datasets")
    datasets = [dataset[0] for dataset in cursor.fetchall()]
    return jsonify(datasets)

@app.route('/api/dataset/<dataset_name>', methods=['GET'])
def get_dataset(dataset_name):
    # Fetch data for the specified dataset
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {average_list_price_by_state}")
    data = cursor.fetchall()
    return jsonify(data)
    
    '''
@app.route('/datasets')
def get_datasets():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch the list of tables (datasets)
        cursor.execute("SHOW TABLES")
        datasets = [row[0] for row in cursor.fetchall()]

        # Close the connection
        cursor.close()
        conn.close()

        return jsonify(datasets)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch datasets', 'details': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/states/<dataset>')
def get_states(dataset):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch the distinct states from the selected dataset
        cursor.execute(f"SELECT DISTINCT state FROM {dataset}")
        states = [row[0] for row in cursor.fetchall()]

        # Close the connection
        cursor.close()
        conn.close()

        return jsonify(states)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch states', 'details': str(e)}), 500

@app.route('/regions/<dataset>')
def get_regions(dataset):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch the distinct regions from the selected dataset
        cursor.execute(f"SELECT DISTINCT region FROM {dataset}")
        regions = [row[0] for row in cursor.fetchall()]

        # Close the connection
        cursor.close()
        conn.close()

        return jsonify(regions)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch regions', 'details': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
