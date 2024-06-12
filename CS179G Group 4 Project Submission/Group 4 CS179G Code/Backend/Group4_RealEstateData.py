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

@app.route('/types/<dataset>')
def get_types(dataset):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch the distinct states from the selected dataset
        cursor.execute(f"SELECT DISTINCT property_type FROM {dataset}")
        states = [row[0] for row in cursor.fetchall()]

        # Close the connection
        cursor.close()
        conn.close()

        return jsonify(states)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch states', 'details': str(e)}), 500

@app.route('/state_data/<dataset>/<state>')
def get_state_data(dataset, state):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Query
        query = f"SELECT * FROM {dataset} WHERE state = \"{state}\""

        # Fetch the distinct states from the selected dataset
        cursor.execute(query)
        data = [row[1] for row in cursor.fetchall()]

        # Close the connection
        cursor.close()
        conn.close()

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch states', 'details': str(e)}), 500

@app.route('/state_location/<state>')
def get_location(state):
    states = {
    "Alabama": {"latitude": 32.806671, "longitude": -86.79113},
    "Alaska": {"latitude": 61.370716, "longitude": -152.404419},
    "Arizona": {"latitude": 33.729759, "longitude": -111.431221},
    "Arkansas": {"latitude": 34.969704, "longitude": -92.373123},
    "California": {"latitude": 36.116203, "longitude": -119.681564},
    "Columbia": {"latitude": 39.2037, "longitude": -76.8610},
    "Colorado": {"latitude": 39.059811, "longitude": -105.311104},
    "Connecticut": {"latitude": 41.597782, "longitude": -72.755371},
    "Delaware": {"latitude": 39.318523, "longitude": -75.507141},
    "Florida": {"latitude": 27.766279, "longitude": -81.686783},
    "Georgia": {"latitude": 33.040619, "longitude": -83.643074},
    "Hawaii": {"latitude": 21.094318, "longitude": -157.498337},
    "Idaho": {"latitude": 44.240459, "longitude": -114.478828},
    "Illinois": {"latitude": 40.349457, "longitude": -88.986137},
    "Indiana": {"latitude": 39.849426, "longitude": -86.258278},
    "Iowa": {"latitude": 42.011539, "longitude": -93.210526},
    "Kansas": {"latitude": 38.5266, "longitude": -96.726486},
    "Kentucky": {"latitude": 37.66814, "longitude": -84.670067},
    "Louisiana": {"latitude": 31.169546, "longitude": -91.867805},
    "Maine": {"latitude": 44.693947, "longitude": -69.381927},
    "Maryland": {"latitude": 39.063946, "longitude": -76.802101},
    "Massachusetts": {"latitude": 42.230171, "longitude": -71.530106},
    "Michigan": {"latitude": 43.326618, "longitude": -84.536095},
    "Minnesota": {"latitude": 45.694454, "longitude": -93.900192},
    "Mississippi": {"latitude": 32.741646, "longitude": -89.678696},
    "Missouri": {"latitude": 38.456085, "longitude": -92.288368},
    "Montana": {"latitude": 46.921925, "longitude": -110.454353},
    "Nebraska": {"latitude": 41.12537, "longitude": -98.268082},
    "Nevada": {"latitude": 38.313515, "longitude": -117.055374},
    "New Hampshire": {"latitude": 43.452492, "longitude": -71.563896},
    "New Jersey": {"latitude": 40.298904, "longitude": -74.521011},
    "New Mexico": {"latitude": 34.840515, "longitude": -106.248482},
    "New York": {"latitude": 42.165726, "longitude": -74.948051},
    "North Carolina": {"latitude": 35.630066, "longitude": -79.806419},
    "North Dakota": {"latitude": 47.528912, "longitude": -99.784012},
    "Ohio": {"latitude": 40.388783, "longitude": -82.764915},
    "Oklahoma": {"latitude": 35.565342, "longitude": -96.928917},
    "Oregon": {"latitude": 44.572021, "longitude": -122.070938},
    "Pennsylvania": {"latitude": 40.590752, "longitude": -77.209755},
    "Rhode Island": {"latitude": 41.680893, "longitude": -71.51178},
    "South Carolina": {"latitude": 33.856892, "longitude": -80.945007},
    "South Dakota": {"latitude": 44.299782, "longitude": -99.438828},
    "Tennessee": {"latitude": 35.747845, "longitude": -86.692345},
    "Texas": {"latitude": 31.054487, "longitude": -97.563461},
    "Utah": {"latitude": 40.150032, "longitude": -111.862434},
    "Vermont": {"latitude": 44.045876, "longitude": -72.710686},
    "Virginia": {"latitude": 37.769337, "longitude": -78.169968},
    "Washington": {"latitude": 47.400902, "longitude": -121.490494},
    "West Virginia": {"latitude": 38.491226, "longitude": -80.954063},
    "Wisconsin": {"latitude": 44.268543, "longitude": -89.616508},
    "Wyoming": {"latitude": 42.755966, "longitude": -107.30249}
    }
    return states[state]

@app.route('/region_location/<region>')
def get_location_region(region):
    url = f"https://www.zipcodeapi.com/rest/NaDX1tra76uTOKSFRouI6yktLSEw9vmadeiY0n5G7xMrZliaNCjxMgzSaHkRnhDk/info.json/{region}/degrees"
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        # Construct response with CORS headers
        response = jsonify(data)
        response.headers.add('Access-Control-Allow-Origin', '*')  # Allow all origins, restrict based on your needs
        
        return response
    else:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code

@app.route('/type_data/<dataset>/<state>/<prop_type>')
def get_type_data(dataset, state, prop_type):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Query
        query = f"SELECT * FROM {dataset} WHERE state = \"{state}\" AND property_type = \"{prop_type}\""

        # Fetch the distinct states from the selected dataset
        cursor.execute(query)
        data = [row[2] for row in cursor.fetchall()]

        # Close the connection
        cursor.close()
        conn.close()

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch states', 'details': str(e)}), 500


@app.route('/region_data/<dataset>/<region>')
def get_region_data(dataset, region):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Query
        query = f"SELECT * FROM {dataset} WHERE region = \"{region}\""

        # Fetch the distinct states from the selected dataset
        cursor.execute(query)
        data = [row[1] for row in cursor.fetchall()]

        # Close the connection
        cursor.close()
        conn.close()

        return jsonify(data)
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
    
@app.route('/us-map')
def us_map():
    return render_template('us_map.html')


@app.route('/growth-data')
def growth_data():
    growth_by_state = {
    "California": 2.5,
    "Texas": -1.5,
    "New York": 0.5,
    "Florida": 0.8,
    "Illinois": -0.4,
    # Include all necessary states
}
    return jsonify(growth_by_state)

@app.route('/industry-growth-data')
def industry_growth_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT region, predicted_industry_potential FROM industry_potential_by_region"
        cursor.execute(query)
        rows = cursor.fetchall()
        # Transform data into a dictionary keyed by region
        growth_data = {row['region']: row['predicted_industry_potential'] for row in rows}
        return jsonify(growth_data)
    except Exception as e:
        return jsonify({'error': 'Database query failed', 'details': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/state-industry-growth-data')
def state_industry_growth_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT SUBSTRING_INDEX(region, ',', -1) AS state, AVG(predicted_industry_potential) AS avg_growth
            FROM industry_potential_by_region
            GROUP BY SUBSTRING_INDEX(region, ',', -1)
        """)
        rows = cursor.fetchall()
        # Normalize state names if necessary, and round averages for simplicity
        growth_data = {row['state'].strip(): round(row['avg_growth'], 2) for row in rows}
        return jsonify(growth_data)  # Ensure the variable name matches what's being returned
    except Exception as e:
        # Ensure the error message is helpful and the variable names are correct
        return jsonify({'error': 'Database query failed', 'details': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/state-regional-growth-data')
def state_regional_growth_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT SUBSTRING_INDEX(region, ',', -1) AS state, AVG(predicted_regional_growth) AS avg_growth
            FROM regional_growth_by_region
            GROUP BY SUBSTRING_INDEX(region, ',', -1)
        """)
        rows = cursor.fetchall()
        growth_data = {row['state'].strip(): round(row['avg_growth'], 4) for row in rows}
        return jsonify(growth_data)
    except Exception as e:
        return jsonify({'error': 'Database query failed', 'details': str(e)}), 500
    finally:
        cursor.close()
        conn.close()



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
