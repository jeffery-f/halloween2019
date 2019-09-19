
# states:

import paho.mqtt.client as mqtt
from queue import Queue
import time

ADDRESS = "test.mosquitto.org"
PORT = 1883
CHANNEL = "jrfhalloween/trigger"
CLIENTNAME = "MAIN"

q = Queue()
state = 0


def on_message(mosq, obj, msg):
    # This callback will be called for messages that we receive that do not
    # match any patterns defined in topic specific callbacks, i.e. in this case
    # those messages that do not have topics $SYS/broker/messages/# nor
    # $SYS/broker/bytes/#
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    if msg.payload =='SMOKE_ON':
        # play video
        pass

    elif msg.payload =='SMOKE_OFF':
        # kill video
        pass

    else:
        q.put(msg.payload)

# connect to the MQTT system
client = mqtt.Client(CLIENTNAME) #create new instance
client.connect(ADDRESS, PORT) #connect to broker
client.on_message=on_message
client.subscribe(CHANNEL, 0)
client.loop_start()


