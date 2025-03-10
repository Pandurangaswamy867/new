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
    secret_arn = os.getenv("DB_SECRET")  # ARN of the secret
    region_name = "us-east-1"  # Set your AWS region
    
    if not secret_arn:
        print("Error: DB_SECRET environment variable not set.")
        return None
    
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    
    try:
        response = client.get_secret_value(SecretId=secret_arn)
        secret = json.loads(response['SecretString'])
        return {
            "host": secret.get("host"),
            "user": secret.get("username"),
            "password": secret.get("password"),
            "database": secret.get("dbname", "hotel_db"),
            "port": int(secret.get("port", 3306)),
        }
    except client.exceptions.ResourceNotFoundException:
        print(f"Error: Secret {secret_arn} not found.")
    except client.exceptions.AccessDeniedException:
        print("Error: Access to Secrets Manager denied.")
    except Exception as e:
        print(f"Error fetching secrets: {e}")
    
    return None

DB_CONFIG = get_db_credentials()

def get_db_connection():
    if not DB_CONFIG:
        print("Error: Database credentials not available.")
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
        print("Error: Skipping table creation due to database connection failure.")
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
        print("Database table `rooms` ensured.")
    except mysql.connector.Error as err:
        print(f"Table Creation Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Initialize the database
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

    if not name or not capacity:
        return jsonify({"error": "Missing room name or capacity"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO rooms (name, capacity) VALUES (%s, %s)", (name, capacity))
        connection.commit()
        return jsonify({"message": "Room added successfully"})
    except mysql.connector.Error as err:
        print(f"Insert Error: {err}")
        return jsonify({"error": "Failed to add room"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route("/room-list")
def room_list():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, capacity FROM rooms")
        rooms = cursor.fetchall()
        return jsonify(rooms)
    except mysql.connector.Error as err:
        print(f"Query Error: {err}")
        return jsonify({"error": "Failed to fetch room list"}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=2000)
