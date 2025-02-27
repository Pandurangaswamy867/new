from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 AWS App Runner & Kubernetes</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #1e1e2f;
            color: #fff;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        .container {
            margin-top: 5%;
            padding: 20px;
        }
        h1 {
            font-size: 2.5rem;
            color: #ffcc00;
            text-shadow: 2px 2px 5px black;
        }
        .icon {
            font-size: 3rem;
            margin: 15px;
            transition: transform 0.3s ease-in-out;
        }
        .icon:hover {
            transform: scale(1.2);
        }
        .flowchart {
            text-align: left;
            font-size: 1.2rem;
            margin: 30px auto;
            max-width: 600px;
            background-color: #29293d;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 3px 3px 10px rgba(255, 255, 255, 0.2);
        }
        .step {
            margin: 15px 0;
            padding: 10px;
            background-color: #3a3a5a;
            border-radius: 5px;
            box-shadow: 2px 2px 8px rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            transition: background 0.3s ease;
        }
        .step i {
            font-size: 1.5rem;
            margin-right: 10px;
        }
        .step:hover {
            background-color: #50507a;
        }
        button {
            padding: 10px 20px;
            font-size: 1.2rem;
            background-color: #ffcc00;
            color: black;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
            margin-top: 20px;
        }
        button:hover {
            background-color: #e6b800;
        }
        .progress-container {
            width: 60%;
            margin: 20px auto;
            background-color: #3a3a5a;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.2);
        }
        .progress-bar {
            width: 0%;
            height: 20px;
            background-color: #ffcc00;
            transition: width 0.5s ease;
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
        <h1><i class="fab fa-aws icon"></i> Welcome to AWS App Runner Demo! <i class="fas fa-network-wired icon"></i></h1>
        <p>🚀 Deploying applications on AWS App Runner with Kubernetes & Cloud Services!</p>
        
        <div class="flowchart">
            <h2>📌 Deployment Flowchart:</h2>
            <div class="step" onclick="updateProgress(16.6)"><i class="fab fa-github"></i> Step 1: Code from GitHub Repo</div>
            <div class="step" onclick="updateProgress(33.2)"><i class="fas fa-server"></i> Step 2: AWS App Runner Deploys App</div>
            <div class="step" onclick="updateProgress(49.8)"><i class="fas fa-shield-alt"></i> Step 3: Protected by AWS WAF</div>
            <div class="step" onclick="updateProgress(66.4)"><i class="fas fa-sitemap"></i> Step 4: Routing via Route 53</div>
            <div class="step" onclick="updateProgress(83.0)"><i class="fas fa-chart-line"></i> Step 5: Observability with CloudWatch</div>
            <div class="step" onclick="updateProgress(100)"><i class="fas fa-check-circle"></i> Step 6: Scalable & Running 🚀</div>
        </div>
        
        <div class="progress-container">
            <div class="progress-bar" id="progressBar"></div>
        </div>

        <button onclick="animateIcons()">Click to Animate</button>
    </div>

    <div class="footer">
        <p>&copy; 2025 AWS App Runner & Kubernetes Demo | 🌍 Built for Cloud Enthusiasts!</p>
    </div>

    <script>
        function animateIcons() {
            const icons = document.querySelectorAll('.icon');
            icons.forEach(icon => {
                icon.style.transform = "rotate(360deg)";
                setTimeout(() => icon.style.transform = "rotate(0deg)", 500);
            });
        }
        
        function updateProgress(value) {
            document.getElementById("progressBar").style.width = value + "%";
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
