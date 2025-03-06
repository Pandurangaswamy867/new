from flask import Flask, render_template_string, request, jsonify
import mysql.connector
import os
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.mysql import MySQLInstrumentor

# Enable OpenTelemetry Tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True))
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
MySQLInstrumentor().instrument()

logging.basicConfig(level=logging.INFO)

# MySQL Database Configuration from Environment Variables
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
}

def get_db_connection():
    """Establish a connection to the MySQL database."""
    with tracer.start_as_current_span("get_db_connection"):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as err:
            logging.error(f"Database Connection Error: {err}")
            return None

# Ensure the 'users' table exists
def init_db():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE
                )
            """)
            conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            logging.error(f"Database Initialization Error: {err}")
        finally:
            conn.close()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 AWS App Runner & X-Ray</title>
    <style>
        body { font-family: Arial, sans-serif; background: #1e1e2f; color: white; text-align: center; }
        .container { margin-top: 5%; }
        h1 { color: #ffcc00; }
        input, button { margin: 10px; padding: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 AWS App Runner & X-Ray Tracing</h1>
        <p>Enter details to store in MySQL database:</p>
        <input type="text" id="name" placeholder="Name">
        <input type="email" id="email" placeholder="Email">
        <button onclick="submitData()">Submit</button>
        <h2>Users List</h2>
        <ul id="userList"></ul>
    </div>
    <script>
        function submitData() {
            let name = document.getElementById("name").value;
            let email = document.getElementById("email").value;
            fetch("/add_data", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: name, email: email })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message || data.error);
                fetchUsers();
            });
        }
        function fetchUsers() {
            fetch("/get_users")
            .then(response => response.json())
            .then(users => {
                let userList = document.getElementById("userList");
                userList.innerHTML = "";
                users.forEach(user => {
                    let li = document.createElement("li");
                    li.textContent = `${user.name} - ${user.email}`;
                    userList.appendChild(li);
                });
            });
        }
        window.onload = fetchUsers;
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/add_data", methods=["POST"])
def add_data():
    """API to add user data to MySQL database."""
    with tracer.start_as_current_span("add_user"):
        try:
            data = request.json
            name = data.get("name")
            email = data.get("email")
            conn = get_db_connection()
            if not conn:
                return jsonify({"error": "Database connection failed"}), 500
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"message": "Data added successfully!"}), 201
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500

@app.route("/get_users", methods=["GET"])
def get_users():
    """API to fetch users from MySQL database."""
    with tracer.start_as_current_span("get_users"):
        try:
            conn = get_db_connection()
            if not conn:
                return jsonify({"error": "Database connection failed"}), 500
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(users)
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500

@app.route("/debug_env", methods=["GET"])
def debug_env():
    """Debug route to check environment variables for database connection."""
    masked_config = DB_CONFIG.copy()
    masked_config["password"] = "********"  # Mask password for security
    return jsonify(masked_config)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=2000)
