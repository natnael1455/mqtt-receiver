import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(self, broker_address):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.connect(broker_address, port=1883)  # Adjust port as needed

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("""Connected to broker
Press Enter to disconnect...""")
        else:
            print("Connection failed")
 
    def publish(self, topic, json_data):
        self.client.publish(topic, payload=json_data, qos=0)

    def disconnect(self):
        self.client.disconnect()