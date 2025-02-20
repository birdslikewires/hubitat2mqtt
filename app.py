#!/usr/bin/env python3

## hubitat2mqtt v1.00 (20th February 2025)
##  Takes the POST output from the Maker API and converts it to MQTT.

from flask import Flask, request
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# MQTT settings
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n" % rc)

client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT)

@app.route('/receive', methods=['POST'])
def receive_post():
    data = request.json
    if data and 'content' in data and 'displayName' in data['content']:
        display_name = data['content']['displayName']
        inner_content = data['content']
        json_data = json.dumps(inner_content)
        mqtt_topic = f"hubitat2mqtt/{display_name}"
        client.publish(mqtt_topic, json_data)
        return f"Data received and published to MQTT topic: {mqtt_topic}", 200
    else:
        return "No valid data received", 400

if __name__ == '__main__':
    client.loop_start()
    app.run(host='0.0.0.0', port=5000)
