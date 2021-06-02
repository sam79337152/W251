FROM ubuntu:latest
MAINTAINER fnndsc "dev@babymri.org"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

ENTRYPOINT ["python3"]


#FROM w251/cuda:dev-tx2-4.3_b132
FROM ubuntu:18.04
#FROM python:3
#WORKDIR /usr/src/app


#RUN apt-get -y install python3-pip
##RUN sudo apt-get install python3

#RUN sudo apt-get -y update && sudo apt-get -y upgrade 
##RUN apt-get update && apt-get install -y python-pip


##RUN apt-get install -y python3-numpy
##RUN apt-get install -y python3-opencv

#RUN sudo python2 get-pip.py
#RUN sudo apt install python3-pip

RUN apt install python3-opencv
RUN pip3 install --upgrade pip

RUN apt install -y mosquitto-clients
RUN pip3 install paho-mqtt
RUN pip3 install numpy
RUN pip3 install opencv-python
RUN pip3 install decorator==4.4.2
RUN pip3 install setuptools
RUN pip3 install pickle4


RUN mkdir /app
WORKDIR /app
COPY facedetectortest.py /app
COPY testpython.py /app

RUN export DISPLAY=:0
#RUN sudo xhost +

#CMD ["python3","facedetectortest.py"]
CMD ["python3","testpython.py"]
