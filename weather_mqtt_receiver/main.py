import paho.mqtt.client as mqtt

# MQTT broker details
BROKER = "localhost"
PORT = 1883
TOPICS = [("wind/sensor/speed", 0), ("wind/sensor/data", 0)]  # List of (topic, QoS)

# Callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker at {BROKER}:{PORT}")
        for topic, qos in TOPICS:
            client.subscribe(topic, qos)
            print(f"Subscribed to topic: {topic}")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback for when a message is received
def on_message(client, userdata, msg):
    if msg.topic == "wind/sensor/speed":
        print(f"Speed Message: {msg.payload.decode()}")  # Process speed-specific data
    elif msg.topic == "wind/sensor/data":
        print(f"Direction Message: {msg.payload.decode()}")  # Process direction-specific data
    else:
        print(f"Unknown topic {msg.topic}: {msg.payload.decode()}")

# Create MQTT client instance
client = mqtt.Client()

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(BROKER, PORT, 60)

# Start the loop to process network traffic and dispatch callbacks
try:
    print("Listening for messages...")
    client.loop_forever()
except KeyboardInterrupt:
    print("\nDisconnected from the broker.")
    client.disconnect()


