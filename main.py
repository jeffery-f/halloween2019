


# states:

import paho.mqtt.client as mqtt
from queue import Queue
import time
import threading

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
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    message = str(msg.payload, 'utf-8')
    if message =='VIDEO_START':
        # play video
        pass

    elif message =='VIDEO_STOP':
        # kill video
        pass



    elif 'TIMER' in message:
        time = int(message.split('_')[-1])
        t = threading.Thread(target=timer_function, args=(time,))
        t.start()

    else:
        q.put(message)

# connect to the MQTT system
client = mqtt.Client(CLIENTNAME) #create new instance
client.connect(ADDRESS, PORT) #connect to broker
client.on_message=on_message
client.subscribe(CHANNEL, 0)
client.loop_start()

def timer_function(length):
    time.sleep(length)
    client.publish(CHANNEL, 'TIME_UP')


while True:

    # if queue has elements
    if q.qsize() > 0:
        msg = q.get()
        print(msg)
    else:
        msg = ""

    if msg == "STOP":
        state = 0
    elif msg == "RESET":
        state = 2



    # Stop Everything - reset everything and wait for play
    if state == 0:
        print('Resetting  | state = 0')
        # reset all objects to base case: wait for start command
        client.publish(CHANNEL, 'SMOKE_OFF' )
        client.publish(CHANNEL, 'PORCH_ON')
        client.publish(CHANNEL, 'INTERIOR_ON')
        client.publish(CHANNEL, 'LED_OFF')
        client.publish(CHANNEL, 'PUMPKIN_IDLE')
        client.publish(CHANNEL, 'VIDEO_STOP')

        # wait for play message
        state = state + 1

    # Waiting for play button
    elif state == 1:
        if msg == "PLAY":
            state = state + 1

    # Reset status - clear everything
    elif state ==2:

        print('Resetting | State = 2')
        client.publish(CHANNEL, 'SMOKE_OFF')
        client.publish(CHANNEL, 'PORCH_ON')
        client.publish(CHANNEL, 'INTERIOR_ON')
        client.publish(CHANNEL, 'LED_OFF')
        client.publish(CHANNEL, 'PUMPKIN_IDLE')
        client.publish(CHANNEL, 'STAIRS_OFF')
        client.publish(CHANNEL, 'VIDEO_STOP')


        state = state + 1

    # wait for motion, on either sensor
    elif state == 3:

        if msg == 'PUMPKIN_MOTION':
            client.publish(CHANNEL, "PUMPKIN_WARNING")
            state = state + 1

        if msg == 'CENTER_MOTION':
            state = state + 2

    # Wait Center Motion
    elif state == 4:
        if msg == 'CENTER_MOTION':
            state = state + 1


    # turn off lights, trigger smoke
    elif state == 5:
        client.publish(CHANNEL, 'PORCH_OFF')
        client.publish(CHANNEL, 'INTERIOR_OFF')
        client.publish(CHANNEL, 'SMOKE_ON')
        client.publish(CHANNEL, 'LED_ORANGE' )
        client.publish(CHANNEL, 'STAIRS_ON')
        client.publish(CHANNEL, 'TIMER_4')
        state = state + 1

    # start video
    elif state == 6:

        if msg == 'TIME_UP':
            client.publish(CHANNEL,'VIDEO_START')
            client.publish(CHANNEL,'LED_LIGHTENING')
            client.publish(CHANNEL, 'TIMER_')

            state = state + 1

    elif state == 7:

            if msg =='TIME_UP':
                client.publish(CHANNEL,'SMOKE_OFF')
                client.publish(CHANNEL, 'TIMER_15')
                state = state + 1




















# 1 waiting for input
    # if pumpkin, go to step 1
    # if main go to step 3

# 2: Pumpkin plays warning
    # if doorbell pressed go to state 10 (reset state

# 3: Wait for main motion sensor


# 4: Porch lights off, LED lights to orange, smoke machine on

# 5: start lightening strikes
