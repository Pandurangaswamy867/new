from flask import Flask, request, jsonify, render_template_string
import mysql.connector
import os
import boto3
import json
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

app = Flask(__name__)

# Enable AWS X-Ray
xray_recorder.configure(service='MyFlaskApp')
XRayMiddleware(app, xray_recorder)

# Fetch database credentials from AWS Secrets Manager
def get_db_credentials():
    secret_name = "AppRunnerHotelDBSecret"  # Replace with your actual secret name
    region_name = "us-east-1"  # Replace with your AWS region

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response['SecretString'])
        return {
            "host": secret["host"],
            "user": secret["username"],
            "password": secret["password"],
            "database": secret["dbname"],
            "port": int(secret.get("port", 3306)),
        }
    except Exception as e:
        print(f"Error fetching secrets: {e}")
        return None

DB_CONFIG = get_db_credentials()

def get_db_connection():
    if not DB_CONFIG:
        print("Database credentials not available.")
        return None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None

def create_tables():
    connection = get_db_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                capacity INT NOT NULL
            )
        """)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Table Creation Error: {err}")
    finally:
        cursor.close()
        connection.close()

create_tables()

@app.route("/")
def home():
    return render_template_string("""
    <h1>Welcome to the Hotel App</h1>
    <a href='/add'>Add Room</a> | <a href='/room-list'>Room List</a>
    """)

@app.route("/add")
def add():
    return render_template_string("""
    <h1>Add a New Room</h1>
    <form action='/create' method='POST'>
        <label>Room Name:</label>
        <input type='text' name='name' required>
        <label>Capacity:</label>
        <input type='number' name='capacity' required>
        <button type='submit'>Add Room</button>
    </form>
    """)

@app.route("/create", methods=["POST"])
def create():
    name = request.form.get("name")
    capacity = request.form.get("capacity")
    connection = get_db_connection()
    if connection is None:
        return render_template_string("""
        <h1>Error</h1>
        <p>Could not connect to the database.</p>
        """)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO rooms (name, capacity) VALUES (%s, %s)", (name, capacity))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Insert Error: {err}")
    finally:
        cursor.close()
        connection.close()
    return render_template_string("""
    <h1>Room Successfully Created</h1>
    <a href='/'>Go Back</a>
    """)

@app.route("/error")
def error():
    return render_template_string("""
    <h1>An Error Occurred</h1>
    <p>Something went wrong. Please try again later.</p>
    <a href='/'>Go Back</a>
    """)

@app.route("/param-list")
def param_list():
    return render_template_string("""
    <h1>Application Parameters</h1>
    <p>Database Host: {{ db_host }}</p>
    <p>Database Name: {{ db_name }}</p>
    """, db_host=DB_CONFIG["host"], db_name=DB_CONFIG["database"])

@app.route("/room-list")
def room_list():
    connection = get_db_connection()
    if connection is None:
        return render_template_string("""
        <h1>Error</h1>
        <p>Could not connect to the database.</p>
        """)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name, capacity FROM rooms")
    rooms = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template_string("""
    <h1>List of Rooms</h1>
    <ul>
        {% for room in rooms %}
            <li>{{ room.name }} - Capacity: {{ room.capacity }}</li>
        {% endfor %}
    </ul>
    <a href='/'>Go Back</a>
    """, rooms=rooms)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=2000)
