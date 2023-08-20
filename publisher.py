import paho.mqtt.client as mqtt
import random
import json
from datetime import datetime
import time


# MQTT setup for publisher
def setup():
    brokers = ["broker.hivemq.com"]
    broker_address = brokers[0]
    client = mqtt.Client("SmartCleanRoom_IOT_FinalProject")
    port = 1883
    print("Starts publishing data to broker ", broker_address)
    client.connect(broker_address, port)
    return client


# Generate random temperature and humidity data
def generate_Air_conditioning_rate(id):
    data = {}
    time.sleep(30)
    current_time = datetime.today().strftime('%H:%M')
    if id == 0:
        id = random.randint(1, 5)
    temp = random.randint(14, 26) + random.randint(1,10)/10
    hum = random.randint(34, 46) + random.randint(1,10)/10
    data[id] = [temp, hum, current_time]
    return data


# Send data dictionary via MQTT
def send_data(topic, data, client):
    json_data = json.dumps(data)
    client.publish(topic, json_data)


def generate_Air_conditioning_rate_and_publish(client_id):
    client = setup()
    # Continuously generate and send data
    while True:
        sub_topic = "IOT/FinalProject/SmartCleanRoom"
        data = generate_Air_conditioning_rate(client_id)
        send_data(sub_topic, data, client)

