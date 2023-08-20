import paho.mqtt.client as mqtt
import json
import tkinter as tk
from datetime import datetime
import time


# MQTT setup for subscriber
def setup():
    brokers = ["broker.hivemq.com"]
    broker_address = brokers[0]
    client = mqtt.Client("SmartCleanRoomSubscriber_IOT_FinalProject")
    print("Connecting to broker ", broker_address)
    port = 1883
    client.connect(broker_address, port)
    sub_topic = "IOT/FinalProject/SmartCleanRoom"
    client.subscribe(sub_topic)
    return client


def create_gui():
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Clean Rooms Monitor")
    listbox = tk.Listbox(root)
    listbox.config(width=100, height=100, font=("Courier 11", 13), fg="black", bg="white")
    current_date = datetime.today().strftime('%B %d, %Y')
    listbox.insert(tk.END, "Air-conditioning in Clean Rooms on " + current_date + " - Stay Alert for Temperature and Humidity data")
    listbox.insert(tk.END, "")
    listbox.pack()
    return root, listbox


# Callback function for incoming messages of all rooms
def on_message_for_rooms(client, userdata, message, listbox):
    data = json.loads(message.payload.decode())
    for id, content in data.items():
        temp = content[0]
        hum = content[1]
        sample_time = content[2]
        if temp > 25 or temp < 15 or hum < 35 or hum > 45:
            listbox.insert(tk.END,
                           "Clean room " + str(id) + ": Temperature data: " + str(temp) + "°C | Humidity data: " + str(hum) + "% | on time: " + sample_time)
            # Create alert by changing the color
            listbox.itemconfig(listbox.size() - 1, {'bg': 'red'})
        else:
            listbox.insert(tk.END,
                           "Clean room " + str(id) + ": Temperature data: " + str(temp) + "°C | Humidity data: " + str(hum) + "% | on time: " + sample_time)
            listbox.itemconfig(listbox.size() - 1, {'bg': 'white'})
        time.sleep(2)


# Callback function for incoming messages of specific room
def on_message_for_specific_room(client, userdata, message, client_id, listbox):
    data = json.loads(message.payload.decode())
    for id, content in data.items():
        temp = content[0]
        hum = content[1]
        sample_time = content[2]
        if id == str(client_id):
            if temp > 25 or temp < 15 or hum < 35 or hum > 45:
                listbox.insert(tk.END,
                               "Clean room " + str(id) + ": Temperature data: " + str(temp) + "°C | Humidity data: " + str(hum) + "% | on time: " + sample_time)
                # Create alert by changing the color
                listbox.itemconfig(listbox.size() - 1, {'bg': 'red'})
            else:
                listbox.insert(tk.END,
                               "Clean room " + str(id) + ": Temperature data: " + str(temp) + "°C | Humidity data: " + str(hum) + "% | on time: " + sample_time)
                listbox.itemconfig(listbox.size() - 1, {'bg': 'white'})
        time.sleep(2)


# Continuously listen for incoming data
def subscribe(client_id):
    client = setup()
    root, listbox = create_gui()
    print("Starts displaying the heart rate dashboard")
    if client_id == 0:
        client.on_message = lambda c, u, m: on_message_for_rooms(c, u, m, listbox)
    else:
        listbox.insert(tk.END,
                       "Dashboard of Clean room " + str(client_id), "")
        client.on_message = lambda c, u, m: on_message_for_specific_room(c, u, m, client_id, listbox)
    client.loop_start()
    root.mainloop()

