from flask import Flask, request, jsonify, render_template
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
            "database": secret.get("dbname", "hotel_db"),
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
    return render_template("index.html")

@app.route("/add")
def add():
    return render_template("add_room.html")

@app.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    name = data.get("name")
    capacity = data.get("capacity")
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO rooms (name, capacity) VALUES (%s, %s)", (name, capacity))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Insert Error: {err}")
    finally:
        cursor.close()
        connection.close()
    return jsonify({"message": "Room added successfully"})

@app.route("/room-list")
def room_list():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name, capacity FROM rooms")
    rooms = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(rooms)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=2000)
