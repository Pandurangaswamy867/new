from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return "Hello, this is an AWS App Runner Flask App!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=2000)
