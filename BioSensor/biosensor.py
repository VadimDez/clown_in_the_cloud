
from wyliodrin import *
import json, datetime
import paho.mqtt.client as mqtt
from sys import stdin
import sys

THING_TOKEN = u"cdbac4cc05fab52d4b607547a185e8604b43c6ee72f2a5911ecb1b7445b47a76"
USER_TOKEN = u"06118234d92b7437749a576b9de5da6fd06fb7d664378c2f016f0a41e5d8a3b2"
thingsIOdict =  {u"values" : None } #{u"thing" : {u"id" : thingToken }, u"user" : {u"id" : userToken}, u"values" : None}

TOPIC_USER_TOKEN = USER_TOKEN
TOPIC_THING_TOKEN = THING_TOKEN
TOPIC_USER_NAME =  'cloudclown'
TOPIC_THING_NAME = 'clown'

TOPIC = 'public/'+TOPIC_USER_NAME+'/'+TOPIC_THING_NAME;

# The callback when the client connects successfully to the server
def on_connect(client, userdata, rc):
  print("Connected with result code "+str(rc))
  client.subscribe(TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	# print(msg.topic+" "+str(msg.payload))
	return None

LED_PIN = 8
PD_PIN = 0

def main():

  def read_pin_and_avg(pin, times):
    '''Read sensor values times times and return the average reading.
    '''
    tmpList = []
    for ii in range(times):
      tmpList.append(analogRead(PD_PIN))
    avg  = sum(tmpList) / float(len(tmpList))
    return avg


  #Set client ID
  client = mqtt.Client(USER_TOKEN + '|' + THING_TOKEN)
  client.on_connect = on_connect
  client.on_message = on_message

  #Set client credentials to allow publish
  client.username_pw_set(TOPIC_USER_TOKEN,TOPIC_THING_TOKEN)
  client.connect("mqtt.thethings.io", 1883, 60)
  client.loop_start()
  
  #print ("Led on pin %s should blink" % LED_PIN)
  # Setup the pin in output mode (value 1), so that we can write a value on it
  pinMode (LED_PIN, 1)
  # init our sensors.
  PD_Value = 0 
  PD_Background = 0
  # print ("Press the Stop button to stop")
  # Loop forever until, we press stop
  while True:
    thingsIOdict.pop("values",None)
    digitalWrite (LED_PIN, 0)    
    delay(100)
    PD_Background = read_pin_and_avg(PD_PIN,5)
    # now start the LED
    digitalWrite (LED_PIN, 1)
    delay(500)
    # and substract the background
    PD_Value = read_pin_and_avg(PD_PIN,5) - PD_Background
    sendSignal ('signal3',PD_Value)
    # datetime 
    dtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    thingsIOdict[u"values"] = [{u"key" : "biosensor", u"value" : PD_Value, u"unit" : "au", u"type" : "", u"datetime" : dtime}]
    userinput =  json.dumps(thingsIOdict)
    client.publish(TOPIC, payload=userinput)

if __name__ == "__main__":
  main()



