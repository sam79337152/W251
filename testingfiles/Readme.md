### MQTT Topics
In the local broker in Jetson the topic name was named ```facedetector_topic``` while in the remote server in the cloud the topic was named ```facedetector_topic_remote```. The QoS used was ```0``` all over the MQTT pipeline.

### Sample Images
Sample face images that were capture by the camera with Jetson TX2, cut from the frame, sent over the pipeline and saved in the bucket can be found in  ```saved_images```. The http link of the location of the object storage was sent in ISVC.

### Facedetector

The docker image used for the face detector container can be found in ```dockerfiles/facedetector``` and the python code in ```python/facedetector.py```.
```
xhost +

sudo docker run --name face_detector --network hw03 -it --rm --runtime nvidia -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix -v /data/hw3/dockerdata:/root --device=/dev/video1 csancini/hw3

cd ~
python3 facedetector.py
```

### Local Broker


The docker image used for the local broker container  can be found in ```dockerfiles/mosquitto```. The service was start and monitored in the shell terminal only.
```
sudo docker run --name mosquitto --network hw03 -p 1883:1883 -ti --rm -v /data/hw3/dockerdata:/root csancini/hw3-mosquitto sh
/usr/sbin/mosquitto
```

### Local Forwarder

The docker image used for the forwarder container  can be found in ```dockerfiles/mosquitto```and the python code in ```python/forwarder.py```
```
sudo docker run --name forwarder --network hw03 -dti --rm -v /data/hw3/dockerdata:/root csancini/hw3-mosquitto sh
sudo docker network connect bridge forwarder
sudo docker attach forwarder

cd ~
python3 forwarder.py
```

### Remote Broker

The docker image used for the remote broker container  can be found in ```dockerfiles/mosquitto```. The service was start and monitored in the shell terminal only.

```
sudo docker run --name remote-broker --network hw03 -p 1883:1883 -dti --rm -v /root/dockerdata:/root csancini/hw3-mosquitto sh
sudo docker network connect bridge remote-broker
sudo docker exec -it remote-broker /usr/sbin/mosquitto
```

### Image Processor

The docker image used for image processor container  can be found in ```dockerfiles/image-processor```and the python code in ```python/image-processor.py```

```
sudo docker run --name image-processor --network hw03 -ti --rm -v /root/dockerdata:/root -v /mnt/mybucket:/mnt/mybucket csancini/hw3-image-processor sh

cd ~
python3 image-processor.py
```

