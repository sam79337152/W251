import paho.mqtt.client as mqtt
import cv2 as cv
import time
import pickle
from datetime import datetime



#remote info
REMOTE_MQTT_HOST = "18.138.14.58"
# 18.138.14.58
REMOTE_MQTT_PORT = 1883
REMOTE_MQTT_TOPIC = "facedetector_topic_remote"
PATH = "/mnt/mybucket/"


#remote callback function
def on_publish_remote(client,userdata,result):
    print("data published to remote server \n")
    pass

#create remote mqtt client
remote_mqtt_client = mqtt.Client()
remote_mqtt_client.on_publish = on_publish_remote
remote_mqtt_client.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT)
#remote_mqtt_client.publish(REMOTE_MQTT_TOPIC, "test remote connection")

#local info
LOCAL_MQTT_HOST = "localhost"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "facedetector_topic"

#local callback function
def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)


def on_message(client,userdata, msg):
 # try:
    print("\nforwarding message received")	
    remote_mqtt_client.publish(REMOTE_MQTT_TOPIC, payload=msg.payload, qos=0, retain=False)
   
   
    print("\nimage to process received")
    print("client: ",client)
    print("userdata: ",userdata)
    print("msg: ",msg)
    print("msg payload:",msg.payload)
    print("msg type",type(msg))


    #img = pickle.loads(msg.payload,encoding='bytes')
    img = pickle.loads(msg.payload)
    png = cv.imdecode(img, 0)

    ts = str(datetime.timestamp(datetime.now())).replace('.','-', 1)
    filename = PATH + 'frame-' + ts + '.png'
    print("Saving", filename)
    cv.imwrite(filename, png)
  
  
 # except:
   # print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()

