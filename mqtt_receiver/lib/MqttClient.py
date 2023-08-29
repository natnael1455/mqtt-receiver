
import json
import logging
import os
from datetime import datetime

import paho.mqtt.client as mqtt
import pymongo
from dotenv import load_dotenv

from .mongo_db import MongoDBConnection

# Configure logging settings
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Load variables from .env file
load_dotenv()


# a class used to connect to the mqtt server and subscribe to a topic
class MqttClient:
    def __init__(self, broker_address):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            self.client.connect(
                os.getenv("Mqtt_host"), port=int(os.getenv("Mqtt_port"))
            )
        except ConnectionRefusedError:
            logging.error(
                f"Connection is refused by the server at {os.getenv('Mqtt_host')} "
                f"check the port number {os.getenv('Mqtt_port')}"
            )
        except TimeoutError:
            logging.error(
                f" Mqtt server can be found at {os.getenv('Mqtt_host')}  "
            )
        except Exception as e:
            logging.error(f"Unexpected error occurred {e}")

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to broker successfully")
        else:
            logging.error("Connection to the mqtt sever failed")

    def send_to_db(self):
        try:
            mongo_uri = (
                f"mongodb://{os.getenv('DB_host')}:{os.getenv('DB_port')}/"
            )
            db_name = os.getenv("DB_name")
            collection_name = "data"
            connection = MongoDBConnection(mongo_uri, db_name)
            connection.insert_document(collection_name, self.data)
            connection.close_connection()
        except pymongo.errors.ServerSelectionTimeoutError:
            logging.error("Connection to the database failed")

    # The callback for when a message is received from the server.
    def on_message(self, client, userdata, message):
        self.data = json.loads(message.payload.decode())
        self.data["timestamp"] = datetime.now().timestamp()
        self.send_to_db()
        logging.info(
            f"Session ID: {self.data['session_id']}, "
            f"Delivered Energy : {self.data['energy_delivered_in_kWh']} KWh, "
            f"Duration: {self.data['duration_in_seconds']} seconds, "
            f"Cost: {self.data['session_cost_in_cents']} Cents, "
        )

    def subscribe(self, topic):
        self.client.subscribe(topic)
        self.client.loop_forever()

    def disconnect(self):
        self.client.disconnect()
