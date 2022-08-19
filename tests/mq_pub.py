# encoding: utf-8

import paho.mqtt.client as mqtt
import json

# HOST = "192.168.11.249"
HOST = "127.0.0.1"
PORT = 1883


def test():
    client = mqtt.Client()
    client.connect(HOST, PORT, 60)
    # client.publish("fmp/state/ArtStatus/A001","hello Artifact mm",1)
    client.publish("fmp/cmd/ArtOrders/A001", "hello Artifact mm", 1)
    print("ok")


if __name__ == '__main__':
    test()
