from lib.MqttClient import MqttClient
import json
import uuid
import random
import time
import logging

# Configure logging settings
logging.basicConfig(level=logging.DEBUG,  # Set the logging level
                    format='%(asctime)s - %(levelname)s - %(message)s')


def data_generator():
    kwh = random.uniform(2,50)
    cent = kwh * 3
    
    return {
        "session_id": str(uuid.uuid4()),
        "energy_delivered_in_kWh": kwh,
        "duration_in_seconds": random.randint(0, 60),
        "session_cost_in_cents": cent
    }


def main():
    broker_address = "broker.hivemq.com"  # Change this to your broker's address
    mqtt_client = MqttClient(broker_address)
    topic = "nati/topic"
    while True:
        data = data_generator()
        logging.info(data)
        json_data = json.dumps(data)
        mqtt_client.publish(topic, json_data)
        time.sleep(60)
    


if __name__ == "__main__":
    main()
