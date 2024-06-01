from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__, template_folder='/home/cs179g/repo/WebApp/frontend', static_folder='/home/cs179g/repo/WebApp/frontend/static')

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'group4',
    'database': 'group4_db'
}

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

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
