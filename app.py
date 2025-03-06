from flask import Flask, render_template_string, request, jsonify
import mysql.connector
import os
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

app = Flask(__name__)

# Enable AWS X-Ray
xray_recorder.configure(service='MyFlaskApp')
XRayMiddleware(app, xray_recorder)

# MySQL Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
}

def get_db_connection():
    """Establish a connection to MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AWS X-Ray Enabled Flask App Running!"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=2000)
