print("AAA")
import numpy as np
import cv2 as cv
import paho.mqtt.client as paho
import pickle

LOCAL_MQTT_HOST = "18.138.14.58"
# AWS EC2:18.138.14.58
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "facedetector_topic"


print("AA")
#create function for callback
def on_publish(client,userdata,result):
    print("data published \n")
    pass

#create mqtt client
mqtt_client = paho.Client()
mqtt_client.on_publish = on_publish
mqtt_client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT)
print("AB")
mqtt_client.publish(LOCAL_MQTT_TOPIC, "test connection", qos=0, retain=False)

#create face detector
facealg = cv.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

#connect to camera
print("A")
cap = cv.VideoCapture(0)
print("B")

while(True):
    print("C")
    #read image in gray scale
    ret, frame = cap.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

    cv.imshow('frame', gray)
    print("D")
    #detect a face
    faces = facealg.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        
        #cut the face from the frame
        roi_gray = gray[y:y+h, x:x+w]
    
        #encode and public message
        rc,png = cv.imencode('.png', roi_gray)
        msg = pickle.dumps(png)
        mqtt_client.publish(LOCAL_MQTT_TOPIC, msg, qos=0, retain=False)
        print("E")

    #quit capturing
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

