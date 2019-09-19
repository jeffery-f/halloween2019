



import paho.mqtt.client as mqtt


def on_message(mosq, obj, msg):
    # This callback will be called for messages that we receive that do not
    # match any patterns defined in topic specific callbacks, i.e. in this case
    # those messages that do not have topics $SYS/broker/messages/# nor
    # $SYS/broker/bytes/#
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

ADDRESS = "test.mosquitto.org"
PORT = 1883
CHANNEL = "jrfhalloween/trigger"
CLIENTNAME = "COMPUTER"


client = mqtt.Client("COMPUTER") #create new instance
client.connect(ADDRESS, PORT) #connect to broker
client.subscribe(CHANNEL)
client.on_message = on_message
client.loop_start()

while True:
    command = input('press enter to send: \n PLAY \n STOP \n RESET \n PUMPKIN_MOTION \n CENTER_MOTION \n TIME_UP')
    client.publish("jrfhalloween/trigger", command)


