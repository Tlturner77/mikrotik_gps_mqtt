from datetime import datetime as dt
import paho.mqtt.client as mqtt
import ssl
import sqlite3
import json
from paho.mqtt.client import connack_string as ack

class mqtt_sql:
    
    def insert(db_values):
        # Define the SQLite database filename
        db_filename = "sensor_data.db"  

        # Create a connection to the SQLite database
        conn = sqlite3.connect(db_filename)

        # Create a table to store the sensor data if it doesn't already exist
        conn.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            timestamp TEXT,
            latitude REAL,
            longitude REAL,
            altitude REAL,
            speed REAL,
            destination_bearing REAL,
            true_bearing REAL,
            magnetic_bearing REAL,
            satellites INTEGER,
            fix_quality INTEGER
        )
        """)

        # Insert the data into the SQLite database
        conn.execute("INSERT INTO sensor_data (timestamp, latitude, longitude, altitude, speed, destination_bearing, true_bearing, magnetic_bearing, satellites, fix_quality) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (db_values))
        conn.commit()

class mqtt_callback:
    mqtt_topic = "sensor/gps"

    def on_connect(client, userdata, flags, rc, v5config=None):
        print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Connection returned result: "+ack(rc))
        client.subscribe(mqtt_topic, qos=0)

    def on_message(client, userdata, message,tmp=None):
        print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Received message " + str(message.payload) + " on topic '"
        + message.topic + "' with QoS " + str(message.qos))

        payload = json.loads(message.payload)

        # Define the payload values and data types   
        timestamp = dt.strptime((payload["timestamp"]), "%b/%d/%Y %H:%M:%S")  
        latitude = float(payload["latitude"]) 
        longitude = float(payload["longitude"])
        altitude = float(payload["altitude"])
        speed = float(payload["speed"])
        destination_bearing = float(payload["destination-bearing"])
        true_bearing = float(payload["true-bearing"])
        magnetic_bearing = float(payload["magnetic-bearing"])
        satellites = int(payload["satellites"])
        fix_quality = int(payload["fix-quality"])
       # horizontal_dilution = int(payload["horizontal-dilution"])


        db_payload = timestamp, latitude, longitude,altitude,speed,destination_bearing,true_bearing,magnetic_bearing,satellites,fix_quality
        mqtt_sql.insert(db_payload)

    def on_publish(client, userdata, mid,tmp=None):
        print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Published message id: "+str(mid))
        
    def on_subscribe(client, userdata, mid, qos,tmp=None):
        if isinstance(qos, list):
            qos_msg = str(qos[0])
        else:
            qos_msg = f"and granted QoS {qos[0]}"
        print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Subscribed " + qos_msg) 

# Define the AWS IoT broker and topic to subscribe to
mqtt_broker = "AWS_IoT_endpoint"
mqtt_iot_port = 8883
mqtt_topic = "sensor/gps"
mqtt_client_id = "GPSmqttSub"

# Define the path to the AWS IoT root CA certificate
ca_path = "root-CA.crt"

# Define the path to the certificate and private key for your IoT Thing
cert_path = "gps.cert.pem"
key_path = "gps.private.key"

# Define the mqtt client settings, for AWS use version 5
mqtt_client = mqtt.Client(client_id=mqtt_client_id, protocol=mqtt.MQTTv5)

# Define the tls client settings
mqtt_client.tls_set(ca_path, 
                certfile=cert_path, 
                keyfile=key_path,  
                tls_version=2);


# Define callback functions

mqtt_client.on_connect = mqtt_callback.on_connect;
mqtt_client.on_message = mqtt_callback.on_message;
mqtt_client.on_publish = mqtt_callback.on_publish;
mqtt_client.on_subscribe = mqtt_callback.on_subscribe;


# Define the connection to the AWS broker
mqtt_client.connect(mqtt_broker, port=mqtt_iot_port, keepalive=60);

# Deifne the mqtt loop
mqtt_client.loop_forever();