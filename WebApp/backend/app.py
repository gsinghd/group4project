from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__, template_folder='/home/cs179g/WebApp/frontend', static_folder='/home/cs179g/WebApp/frontend/static')

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'group4',
    'database': 'group4_db'
}

# Route for fetching data from SQL database
@app.route('/')
def fetch_data():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Execute SQL query
        cursor.execute('SELECT * FROM average_sale_price_by_state')
        data = cursor.fetchall()

        # Close database connection
        cursor.close()
        conn.close()

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
