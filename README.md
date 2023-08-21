# mqtt-receiver
The mqtt-receiver project even though it's name idicate as MQTT message revice it include three subprojects inside it. and they are as follows.
1. MQTT message receiver project that connects to mqtt broker and receive the message and store it in a momogDB that deloyed locally with it but can work also with by changing the DB_host and DB_port in the docker composer yml in the root directory of this project.

2. the REST api sub project it prpose to to serve or show the data that is save in the monogDB database by the mqtt-receiver it has one api that listens to get method of the port 8000 the it can be modified by changing the host port number for the matter of convince or incase port confilicte.

3. The last one is MQTT publisher project (opsional) that connect to the mqtt broker and publish the message to the broker. it can be used to test the mqtt-receiver project. if you are palning to use your own mqtt publisher. then you to know the following things.
      1. the mqtt-receiver project is listening to the topic "nati/topic" 

      2. use same Mqqtt host and port in my case are "broker.hivemq.com"and 1883 respectively.

      3. the message should be in json format and should have the following keys 
      ```json
      "session_id", "energy_delivered_in_kWh", "duration_in_seconds", "session_cost_in_cents" and the values should be in the following format "session_id": "df624335-1107-4999-8833-e8d721e83739", "energy_delivered_in_kWh": 26.444530841066246, "duration_in_seconds": 16, "session_cost_in_cents": 79.33359252319875.  
      ```

both  the MQTT reveiver and publisher use paho.mqtt.client to connect as wel as send and receive the message from the broker.
and the REST api and MQTT receiver use pymongo to connect to monogDB database. and the REST api use FastAPI to serve the data.

# Setup 
to to Deploy this prject conatairs to a machine you need a machine which has docker and docker-compose installed in it. as well git to clone the project to the machine.

## step 1
clone the project to the machine by using the following command.
```bash
git clone https://github.com/natnael1455/mqtt-receiver.git
```
## step 2
go to the project directory by using the following command.
```bash
cd mqtt-receiver
```
## step 3
run the following command to build the docker images and run the containers.
```bash
docker-compose up -d
```
and run the following command
```bash
docker-compose ps    
```
and you should see something like this.
```bash
   NAME                              IMAGE                          COMMAND                  SERVICE             CREATED             STATUS              PORTS

mqtt-receiver-mqtt-publisher-1    mqtt-receiver-mqtt-publisher   "python main.py"         mqtt-publisher      55 minutes ago      Up 55 minutes       
mqtt-receiver-mqtt-receiver-1     mqtt-receiver-mqtt-receiver    "python main.py"         mqtt-receiver       55 minutes ago      Up 55 minutes       1883/tcp
mqtt-receiver-mqttdb-server-1     mongo:latest                   "docker-entrypoint.s…"   mqttdb-server       55 minutes ago      Up 55 minutes       0.0.0.0:27017->27017/tcp
mqtt-receiver-rest-api-1          mqtt-receiver-rest-api         "uvicorn main:app --…"   rest-api            55 minutes ago      Up 55 minutes       0.0.0.0:8000->8000/tcp 
```
at this point you should see 4 containers running in the machine the forth being the monogDB server.

## optional step mqtt broker
if you diced to use to use other mqtt brokers hosts other than the public one "broker.hivemq.com" set a host with simple host with no credentails for TLS encryption. After setting the mqtt broker change following environment variable in the docker-compose.yml file in the root directory of the project. in both mqtt publisher and receiver.
```docker-compose
      - Mqtt_host=host-address 
      - Mqtt_port=port-number
``````

# Usage
## MQTT publisher
As it has to mimic the real world iot divice that publish auto generated  message to the broker every 1 minute. it does not need to run maunally but you can use the following comand to see the logs of the data it generates.

```bash
docker logs -f mqtt-receiver-mqtt-publisher-1
```
the "mqtt-receiver-mqtt-publisher-1" is the name of the container. you should check the previous command to see the name of the container in your machine. and you should see something as follows in the logs. and new log adding every minute 
```bash
2023-08-20 22:03:12,926 - INFO - {'session_id': 'bb66300e-fc1a-4407-beba-24f6054bc933', 'energy_delivered_in_kWh': 34.64792504159193, 'duration_in_seconds': 55, 'session_cost_in_cents': 103.9437751247758}
2023-08-20 22:04:12,937 - INFO - {'session_id': 'cd2996c9-dbfc-42e4-9a22-e009fc0bf01e', 'energy_delivered_in_kWh': 13.348745806260666, 'duration_in_seconds': 3, 'session_cost_in_cents': 40.046237418782}
2023-08-20 22:05:12,990 - INFO - {'session_id': 'df624335-1107-4999-8833-e8d721e83739', 'energy_delivered_in_kWh': 26.444530841066246, 'duration_in_seconds': 16, 'session_cost_in_cents': 79.33359252319875}
2023-08-20 22:06:13,055 - INFO - {'session_id': 'a0b14be6-775f-4173-9f78-024c21f05429', 'energy_delivered_in_kWh': 25.19380014838053, 'duration_in_seconds': 5, 'session_cost_in_cents': 75.58140044514158}
```

## MQTT receiver
As it listen to the MQTT broker it logs messages and save the in the DATABASE. you can see the logs by using the following command.
```bash
docker logs -f mqtt-receiver-mqtt-receiver-1 
```
and you should see something like this. the mqtt-receiver-mqtt-receiver-1 is the name of the container. you should check the previous command to see the name of the container in your machine. and you should see something as follows in the logs. and new log adding every minute 
```bash
2023-08-20 22:03:13,459 - INFO - Connected to broker Press Enter to disconnect...
2023-08-20 22:04:12,983 - INFO - Session ID: cd2996c9-dbfc-42e4-9a22-e009fc0bf01e, Delivered Energy : 13.348745806260666 KWh, Duration: 3 seconds, Cost: 40.046237418782 Cents, 
2023-08-20 22:05:13,047 - INFO - Session ID: df624335-1107-4999-8833-e8d721e83739, Delivered Energy : 26.444530841066246 KWh, Duration: 16 seconds, Cost: 79.33359252319875 Cents, 
2023-08-20 22:06:13,135 - INFO - Session ID: a0b14be6-775f-4173-9f78-024c21f05429, Delivered Energy : 25.19380014838053 KWh, Duration: 5 seconds, Cost: 75.58140044514158 Cents, 
2023-08-20 22:07:13,202 - INFO - Session ID: 0e0b6b0a-0b0a-4b0a-8b0a-0b0a0b0a0b0a, Delivered Energy : 34.64792504159193 KWh, Duration: 55 seconds, Cost: 103.9437751247758 Cents,
```
## REST api
the finally use to see the data that is saved in the monogDB using web api 
by running the next line in you web browser or postman. you will get all the data that was saved since that moment in json format.
```web
http://localhost:8000/
```
or you can use the following command to get the data in the terminal.
```bash
curl http://localhost:8000/
```
or use this url in you browser to examine the full api with OpenApi 

```web
http://localhost:8000/docs
```
