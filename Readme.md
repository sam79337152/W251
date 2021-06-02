# W251 Deep Learning in the Cloud and at the Edge
## Homework 3
Sam Shih
###### 

### MQTT, Qos And Overall Structure
The facedetecor container pushes the topics once it recognizes a face from the camera. The forwarder container subscribes the topic from MQTT broker, receives messages from facedetector and submit it to AWS EC2``` image_processor```. In the local broker in Jetson, the topic name is named``` facedetector_topic```. In the remote server in the cloud, the topic is named```facedetector_topic_remote```. I use QoS 0 all over the MQTT pipeline. Besides, I simplify the procedure which facedetector will directly store face images in Jetson rather than relying on a standalone logger docker.

### Commands - Kubernetes on Jetsons
```kubectl apply -f mosquitto_deployment.yaml
kubectl get deployments
kubectl apply -f mosquittoService.yaml
kubectl get services```

### Commands - Kubernetes on AWS EC2
```kubectl apply -f mosquitto_deployment_remote.yaml
kubectl get deployments
kubectl apply -f mosquittoService_remote.yaml
kubectl get services
```



I have applied K8s to run the docker in both local Jetson and remote EC2 which makes the whole process simple. Alternatively, we can use the following command to run the docker container.


### Commands - Run Docker Facedetector
The docker image used for the face detector container can be found in``` dockerfiles/facedetectortest``` and the python code in``` python/facedetectortest.py.```

```
xhost +

sudo docker run --name facedetectortest --network hw03 -it --rm --runtime nvidia -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix -v /data/hw3/dockerdata:/root

cd ~
python3 facedetectortest.py
```

### Commands - Run Docker Forward
The docker image used for the forwarder container can be found in``` dockerfiles/forwarder``` and the python code in``` python/forwarder.py```

```
sudo docker run --name forwarder --network hw03 -dti --rm -v /data/hw3/dockerdata:/root
sudo docker network connect bridge forwarder
sudo docker attach forwarder

cd ~
python3 forwarder.py
```

### Commands - Run Docker Image Processor
The docker image used for image processor container can be found in``` dockerfiles/image-processor``` and the python code in``` python/image-processor.py```

```
sudo docker run --name image-processor --network hw03 -ti --rm -v /root/dockerdata:/root -v /mnt/mybucket:/mnt/mybucket

cd ~
python3 image-processor.py
```

### Commands - SSH To AWS
```ssh -i "W251AWSNew.pem" ubuntu@ec2-18-138-14-58.ap-southeast-1.compute.amazonaws.com```

### SampleImages
Images that were captured by the camera , cut from the frame, sent over the pipeline and saved in the bucket can be found in```saved_images.```
The link of my face images:
https://berkeleysambucket.s3-ap-southeast-1.amazonaws.com/faceImages/frame-1622378866-508316.png
https://berkeleysambucket.s3-ap-southeast-1.amazonaws.com/faceImages/frame-1622378866-667324.png

