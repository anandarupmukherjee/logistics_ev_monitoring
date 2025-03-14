FROM arm32v7/python:3-jessie
ADD mqtt_driver.py /

RUN pip install --upgrade pip
RUN pip3 install paho-mqtt
RUN pip install jsonlib-python3
RUN pip3 install regex

#RUN pip3 install os
#RUN pip3 install time
CMD [ "python3", "./mqtt_driver.py"]
 