import paho.mqtt.client as mqtt
import cv2 as cv
import time
import pickle
from datetime import datetime
import boto3

#local info
LOCAL_MQTT_HOST = "18.138.14.58"
# External facing ip: 18.138.14.58
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "facedetector_topic_remote"
PATH = "/mnt/mybucket/"

#local callback function
def on_connect_local(client, userdata, flags, rc)client_loop: send disconnect: Connection reset
        print("image processor connected to remote broker with rc: " + str(rc))


def on_message(client,userdata, msg):
 try:
    print("\nimage to process received")
    print("client: ",client)
    print("userdata: ",userdata)
    print("msg: ",msg)
    print("msg payload:",msg.payload)
    print("msg type",type(msg))


    img = pickle.loads(msg.payload,encoding='bytes')
    png = cv.imdecode(img, 0)

    ts = str(datetime.timestamp(datetime.now())).replace('.','-', 1)
    filename = PATH + 'frame-' + ts + '.png'
    print("Saving", filename)
    cv.imwrite(filename, png)

    s3 = boto3.resource('s3',aws_access_key_id='AKIATI3BQVWKXSWVGUQO',aws_secret_access_key='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')
    s3.meta.client.upload_file(filename, 'berkeleysambucket', 'faceImages/'+'frame-' + ts + '.png')


  except:
    print("Unexpected error:", sys.exc_info()[0])
    print("Unexpected error:")

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()

