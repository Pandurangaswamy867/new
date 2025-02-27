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
    <script src="https://cdn.jsdelivr.net/npm/particles.js"></script>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(120deg, #1e1e2f, #252550);
            color: #fff;
            text-align: center;
            margin: 0;
            padding: 0;
            transition: background 0.5s ease;
        }
        .container {
            margin-top: 5%;
            padding: 20px;
            position: relative;
            z-index: 1;
        }
        h1 {
            font-size: 3rem;
            color: #ffcc00;
            text-shadow: 4px 4px 10px rgba(255, 255, 0, 0.7);
        }
        .icon {
            font-size: 3rem;
            margin: 15px;
            transition: transform 0.3s ease-in-out;
        }
        .icon:hover {
            transform: scale(1.3);
        }
        .flowchart {
            text-align: left;
            font-size: 1.2rem;
            margin: 30px auto;
            max-width: 650px;
            background: linear-gradient(145deg, #2b2b40, #303055);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 4px 4px 12px rgba(255, 255, 255, 0.2);
        }
        .step {
            margin: 15px 0;
            padding: 10px;
            background: #3a3a5a;
            border-radius: 5px;
            box-shadow: 3px 3px 10px rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            transition: all 0.3s ease;
        }
        .step i {
            font-size: 1.5rem;
            margin-right: 10px;
        }
        .step:hover {
            background: #55557a;
            transform: translateX(5px);
        }
        button {
            padding: 12px 24px;
            font-size: 1.3rem;
            background: linear-gradient(45deg, #ffcc00, #ffa500);
            color: black;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s, transform 0.3s;
            margin-top: 20px;
        }
        button:hover {
            background: linear-gradient(45deg, #e6b800, #ff8c00);
            transform: scale(1.05);
        }
        .progress-container {
            width: 70%;
            margin: 20px auto;
            background: #3a3a5a;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 3px 3px 12px rgba(255, 255, 255, 0.2);
        }
        .progress-bar {
            width: 0%;
            height: 20px;
            background: linear-gradient(90deg, #ffcc00, #ff6600);
            transition: width 0.5s ease;
        }
        .footer {
            margin-top: 30px;
            font-size: 1rem;
            color: #bbb;
        }
        /* Dark Mode Toggle */
        .dark-mode {
            background: linear-gradient(120deg, #000, #1a1a2e);
            color: #fff;
        }
        .toggle-container {
            position: fixed;
            top: 20px;
            right: 20px;
            cursor: pointer;
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 10px;
            transition: background 0.3s;
        }
        .toggle-container:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            background: transparent;
            z-index: 0;
        }
    </style>
</head>
<body>
    <div id="particles-js"></div>
    <div class="toggle-container" onclick="toggleDarkMode()">
        <i class="fas fa-moon"></i> Dark Mode
    </div>
    <div class="container">
        <h1><i class="fab fa-aws icon"></i> AWS App Runner & Kubernetes <i class="fas fa-network-wired icon"></i></h1>
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
            document.querySelectorAll('.icon').forEach(icon => {
                icon.style.transform = "rotate(360deg)";
                setTimeout(() => icon.style.transform = "rotate(0deg)", 500);
            });
        }
        function updateProgress(value) {
            document.getElementById("progressBar").style.width = value + "%";
        }
        function toggleDarkMode() {
            document.body.classList.toggle("dark-mode");
        }
        particlesJS.load('particles-js', 'https://cdn.jsdelivr.net/particles.js/2.0.0/particles.json', function() {});
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=2000)
