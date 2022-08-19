# encoding: utf-8


import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("chat")


def on_message(client, userdata, msg):
    print(msg.topic + " " + ":" + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("10.169.96.77", 1883, 60)
client.subscribe(topic="+/vdcs/ogm/T513", qos=1)
client.loop_forever()
