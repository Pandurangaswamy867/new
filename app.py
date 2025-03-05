from flask import Flask, render_template_string, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# MySQL Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "app_db"),
    "port": int(os.getenv("DB_PORT", 3306)),
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Ensure the users table exists
def init_db():
    try:
        conn = get_db_connection()
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
        conn.close()
    except Exception as e:
        print(f"Database Initialization Error: {e}")

# HTML Template (Your existing HTML and CSS)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 AWS App Runner & Kubernetes</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/particles.js"></script>
    <style>
        body { font-family: 'Arial', sans-serif; background: linear-gradient(120deg, #1e1e2f, #252550); color: #fff; text-align: center; }
        .container { margin-top: 5%; padding: 20px; }
        h1 { font-size: 3rem; color: #ffcc00; }
        .form-container { background: #2b2b40; padding: 20px; border-radius: 10px; margin-top: 20px; }
        input, button { margin: 10px; padding: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 AWS App Runner & Kubernetes</h1>
        <p>Enter your details to store in the database:</p>
        <div class="form-container">
            <input type="text" id="name" placeholder="Name" required>
            <input type="email" id="email" placeholder="Email" required>
            <button onclick="submitData()">Submit</button>
        </div>
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
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Data added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_users", methods=["GET"])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=2000)
