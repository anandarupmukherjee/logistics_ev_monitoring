#!/usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import os
import time as t
import json
import re



t.sleep(2)

def insert_val(x,y,z,loc):
    dev="amco"
    # loc="ML_stat"
    # var="curl -i -XPOST 'http://172.18.0.2:8086/write?db=iot' --data '"+dev+" "+loc+"="+mesg+"'"
    var="curl -i -XPOST 'http://172.18.0.2:8086/write?db=ev' --data 'sensor1 x="+str(x)+"',y="+str(y)+"',z="+str(z)+"'"
    os.system(var)


def insert_trig(x,y,z,loc):
    dev="amco"
    # loc="ML_stat"
    # var="curl -i -XPOST 'http://172.18.0.2:8086/write?db=iot' --data '"+dev+" "+loc+"="+mesg+"'"
    print("error here")
    var="curl -i -XPOST 'http://172.18.0.2:8086/write?db=ev' --data 'sensor1 a="+str(x)+"',b="+str(y)+"',c="+str(z)+"'"
    os.system(var)



def on_message_pnp(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # $SYS/broker/bytes/#
    #mqttc.publish("time",payload=t.time())
    #print("Time transmitted to local network....")
    print("entered loop")
    top=msg.topic
    print(top)
    data = "{}".format(str(msg.payload,"utf-8"))
    print(data)
    k=json.dumps(data, separators=(',', ':'))
    x=k.split("ax:")[1].split("\"")[0]
    y=k.split("ay:")[1].split("\"")[0]
    z=k.split("az:")[1].split("\"")[0]
    # print(float(x.replace("\\","")))
    insert_val(float(x.replace("\\","")),float(y.replace("\\","")),float(z.replace("\\","")),top)



def on_message_switch(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # $SYS/broker/bytes/#
    print("entered loop")
    top=msg.topic
    print(top)
    data = "{}".format(str(msg.payload,"utf-8"))
    a=str(data.split(":")[0])
    b=str(data.split(":")[1])
    c=str(data.split(":")[2])
    print(a+":"+b+":"+c)
    insert_trig(a,b,c,top)




def on_message(mosq, obj, msg):
    # This callback will be called for messages that we receive that do not
    # match any patterns defined in topic specific callbacks, i.e. in this case
    # those messages that do not have topics $SYS/broker/messages/# nor
    # $SYS/broker/bytes/#
#    myAWSIoTMQTTClient.publish(msg.topic, msg.payload, 1)
    print("entered loop")
    top=msg.topic
    data = "{}".format(msg.payload)
    message = {"message":data}
#    print("OK......CHECK DONE")
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))



print("Edge handshake initiate...")
mqttc = mqtt.Client()
print("Done. Listening on the local network....")

# Add message callbacks that will only trigger on a specific subscription match.

mqttc.message_callback_add("amco/veh/accx", on_message_pnp)
mqttc.message_callback_add("amco/veh/switch", on_message_switch)
mqttc.on_message = on_message
mqttc.connect("172.18.0.4", 1883, 60)
mqttc.subscribe("amco/#", 0)

#mqttc.publish("time",payload=t.time())
#print("Time transmitted to local network....")
mqttc.loop_forever()
print('Publish End')
