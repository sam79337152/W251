import paho.mqtt.client as mqtt
import cv2 as cv
import time
import pickle
from datetime import datetime

#local info
LOCAL_MQTT_HOST = "localhost"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "facedetector_topic_remote"
PATH = "/mystorage"

#local callback function
def on_connect_local(client, userdata, flags, rc):
        print("image processor connected to local messsage logger: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)


def on_message(client,userdata, msg):
#   try:
    print("\nimage to process received")

    img = pickle.loads(msg.payload)
    png = cv.imdecode(img, 0)

    ts = str(datetime.timestamp(datetime.now())).replace('.','-', 1)
    filename = PATH + 'frame-' + ts + '.png'
    print("Saving", filename)
    cv.imwrite(filename, png)

#   except:
#     print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()
