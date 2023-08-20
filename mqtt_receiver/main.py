from lib.MqttClient import MqttClient


def main():
    broker_address = "localhost"  # Change this to your broker's address
    mqtt_client = MqttClient(broker_address)
    
    topic = "nati/topic"
    mqtt_client.subscribe(topic)
    


if __name__ == "__main__":
    main()
