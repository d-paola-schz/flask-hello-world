from flask import Flask, request, jsonify, render_template
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
#USER = os.getenv("user")
#PASSWORD = os.getenv("password")
#HOST = os.getenv("host")
#PORT = os.getenv("port")
#DBNAME = os.getenv("dbname")

app = Flask(__name__)

def get_connection():
    connection = psycopg2.connect(CONNECTION_STRING)
    print("Connection successful!")
    return connection

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/sensor')
def sensor():
    # Connect to the database
    try:
        connection = get_connection()
        
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()
        
        # Example query
        #cursor.execute("SELECT NOW();")
        cursor.execute("select * from sensores")
        result = cursor.fetchone()
        print("Current Time:", result)
    
        # Close the cursor and connection
        cursor.close()
        connection.close()
        print("Connection closed.")
        return f"Current Time: {result}"
    except Exception as e:
        return f"Failed to connect: {e}"

@app.route("/pagina")
def pagina():
    return render_template("pagina.html")


@app.route("/sensor/<int:sensor_id>", methods=["POST"])
def insert_sensor_value(sensor_id):
    value = request.args.get("value", type=float)
    if value is None:
        return jsonify({"error": "Missing 'value' query parameter"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Insert into sensors table
        cur.execute(
            "INSERT INTO sensores (sensor_id, value) VALUES (%s, %s)",
            (sensor_id, value)
        )
        conn.commit()

        return jsonify({
            "message": "Sensor value inserted successfully",
            "sensor_id": sensor_id,
            "value": value
        }), 201

    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'conn' in locals():
            conn.close()
