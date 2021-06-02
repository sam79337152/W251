import paho.mqtt.client as mqtt

#remote info
REMOTE_MQTT_HOST = "18.138.14.58"
# 18.138.14.58
LOCAL_LOGGER_HOST = "localhost"

REMOTE_MQTT_PORT = 1883
LOCAL_MQTT_PORT = 1883

REMOTE_MQTT_TOPIC = "facedetector_topic_remote"
LOCAL_MQTT_TOPIC = "facedetector_topic_remote"

#remote callback function
def on_publish_remote(client,userdata,result):
    print("data published to remote server \n")
    pass

#create remote mqtt client
remote_mqtt_client = mqtt.Client()
remote_mqtt_client.on_publish = on_publish_remote
remote_mqtt_client.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT)
#remote_mqtt_client.publish(REMOTE_MQTT_TOPIC, "test remote connection")



#local message broker callback function
def on_publish_logger(client,userdata,result):
    print("data published to message logger \n")
    pass

#create local message broker client
local_mqtt_client = mqtt.Client()
local_mqtt_client.on_publish = on_publish_logger
local_mqtt_client.connect(LOCAL_LOGGER_HOST, LOCAL_MQTT_PORT)


#local received message info
LOCAL_MQTT_HOST = "localhost"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "facedetector_topic"

#local received message callback function
def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)


def on_message(client,userdata, msg):
  try:
    print("\nforwarding message to remote")
    remote_mqtt_client.publish(REMOTE_MQTT_TOPIC, payload=msg.payload, qos=0, retain=False)
    print("\nforwarding message to message logger")
    local_mqtt_client.publish(LOCAL_MQTT_TOPIC, payload=msg.payload, qos=0, retain=False)    
  except:
    print("Unexpected error:", sys.exc_info()[0])

#Received message setup    
local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()
