
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS App Runner & Kubernetes</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1e1e2f;
            color: #fff;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        .container {
            margin-top: 10%;
        }
        h1 {
            font-size: 2.5rem;
            color: #ffcc00;
            text-shadow: 2px 2px 5px black;
        }
        .icon {
            font-size: 3rem;
            margin: 20px;
            transition: transform 0.3s ease-in-out;
        }
        .icon:hover {
            transform: scale(1.2);
        }
        .footer {
            margin-top: 30px;
            font-size: 1rem;
            color: #bbb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1><i class="fab fa-aws icon"></i> Welcome to AWS App Runner Flask App! <i class="fas fa-network-wired icon"></i></h1>
        <p>Running on AWS App Runner with Kubernetes Integration!</p>
        <button onclick="animateIcons()">Click to Animate</button>
    </div>
    <div class="footer">
        <p>&copy; 2025 AWS App Runner & Kubernetes Demo</p>
    </div>
    <script>
        function animateIcons() {
            const icons = document.querySelectorAll('.icon');
            icons.forEach(icon => {
                icon.style.transform = "rotate(360deg)";
                setTimeout(() => icon.style.transform = "rotate(0deg)", 500);
            });
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=2000)
