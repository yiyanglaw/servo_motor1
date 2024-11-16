import paho.mqtt.publish as publish
from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)))  # Use current directory for templates

# MQTT settings
MQTT_BROKER = "broker.hivemq.com"  # HiveMQ broker
MQTT_PORT = 1883
MQTT_TOPIC = "raspberrypi/servo/position"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get direction and degree from the form
        direction = request.form["direction"]
        degree = request.form["degree"]

        # Validate degree input (0-90)
        if not degree.isdigit() or not (0 <= int(degree) <= 90):
            return render_template("index.html", message="Invalid degree. Must be between 0 and 90.")
        
        # Send data to MQTT broker
        try:
            payload = f"{direction} {degree}"
            publish.single(MQTT_TOPIC, payload, hostname=MQTT_BROKER)
            return render_template("index.html", message=f"Sent {payload} to Raspberry Pi.")
        except Exception as e:
            return render_template("index.html", message=f"Error: {str(e)}")

    return render_template("index.html", message="")

if __name__ == "__main__":
    app.run(debug=True)
