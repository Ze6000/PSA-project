import paho.mqtt.client as mqtt
import json


# Script to test mqtt connection

# Define the MQTT broker settings
broker_address = "193.137.172.20"
broker_port = 85
topic = "detecao"  

# Define the variables you want to send
N_Comp = 5  
Leak_Detected = True  
N_fugas = 42  

# Create a dictionary with the variables
payload = {
    "N_Comp": N_Comp,
    "Leak_Detected": Leak_Detected,
    "N_fugas": N_fugas
}

# Convert the dictionary to a JSON string
payload_json = json.dumps(payload)

# Create an MQTT client
client = mqtt.Client()

# Connect to the broker
client.connect(broker_address, broker_port)

# Publish the JSON string to the specified topic
client.publish(topic, payload_json)

# Disconnect from the broker
client.disconnect()
print("All done")
