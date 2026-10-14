
from flask import Flask, jsonify, render_template_string
import random
from datetime import datetime

app = Flask(__name__)

# Simulated sensor readings
def read_sensor_data():
    vibration = round(random.uniform(0.10, 0.35), 3)
    temperature = round(random.uniform(28.0, 35.0), 1)

    if vibration > 0.30 or temperature > 34.0:
        status = "UNUSUAL"
    else:
        status = "NORMAL"

    return {
        "vibration": vibration,
        "temperature": temperature,
        "status": status,
        "time": datetime.now().strftime("%H:%M:%S")
    }


HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Medical Equipment Health Monitor</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            color: #1e293b;
            text-align: center;
            padding: 25px;
            margin: 0;
        }

        h1 {
            color: #0f4c81;
            margin-top: 20px;
        }

        .subtitle {
            color: #64748b;
        }

        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            margin: 35px auto;
            max-width: 1000px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 14px;
            width: 260px;
            box-shadow: 0 4px 15px #00000012;
        }

        .card h3 {
            color: #475569;
        }

        .value {
            font-size: 32px;
            font-weight: bold;
            margin: 25px 0;
            color: #0f4c81;
        }

        #status {
            font-size: 25px;
            font-weight: bold;
            margin: 25px 0;
        }

        .note {
            color: #64748b;
            font-size: 13px;
        }
    </style>
</head>

<body>

    <h1>Medical Equipment Health Monitor</h1>
    <p class="subtitle">
        Embedded Systems + IoT Monitoring Prototype
    </p>

    <div class="container">

        <div class="card">
            <h3>Vibration</h3>
            <div class="value" id="vibration">--</div>
            <p>Illustrative units</p>
        </div>

        <div class="card">
            <h3>Temperature</h3>
            <div class="value" id="temperature">--</div>
            <p>Degrees Celsius</p>
        </div>

        <div class="card">
            <h3>Equipment Status</h3>
            <div id="status">Loading...</div>
            <p id="time">Waiting for readings...</p>
        </div>

    </div>

    <p class="note">
        Demo only: readings are simulated, not from real medical equipment.
    </p>

    <script>
        async function updateDashboard() {
            try {
                const response = await fetch("/api/readings");
                const data = await response.json();

                document.getElementById("vibration").textContent =
                    data.vibration;

                document.getElementById("temperature").textContent =
                    data.temperature + " °C";

                const statusElement =
                    document.getElementById("status");

                statusElement.textContent = data.status;

                statusElement.style.color =
                    data.status === "NORMAL" ? "green" : "red";

                document.getElementById("time").textContent =
                    "Updated at " + data.time;

            } catch (error) {
                document.getElementById("status").textContent =
                    "Connection Error";
            }
        }

        updateDashboard();
        setInterval(updateDashboard, 2000);
    </script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/api/readings")
def readings():
    return jsonify(read_sensor_data())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
