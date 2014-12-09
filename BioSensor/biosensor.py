from wyliodrin import *
import json, datetime
import paho.mqtt.client as mqtt
from numpy.fft import rfft, fftfreq
from numpy import zeros,abs
from numpy import hanning

sampling_delay_ms = 5 # ms
sampling_rate  =  200 # Hz
fftdim = 200
twopi = 6.28318530

THING_TOKEN = u"9da4531dedd6ebdd4198b71c2fbe08415e5a3214a1e4193303db8f7c5e00c59c"
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

LED_PIN = 8 # enter the pin number where you connected the LED
PD_PIN = 0 # enter the pin number where  you connected the LDR Sensor.

def main():
  #Set client ID
  client = mqtt.Client(USER_TOKEN + '|' + THING_TOKEN)
  client.on_connect = on_connect
  client.on_message = on_message

  #Set client credentials to allow publish
  client.username_pw_set(TOPIC_USER_TOKEN,TOPIC_THING_TOKEN)
  client.connect("mqtt.thethings.io", 1883, 60)
  client.loop_start()
  
  # Setup the pin in output mode (value 1), so that we can write a value on it
  pinMode (LED_PIN, 1)
  digitalWrite (LED_PIN, 1)


  # init an array to hold the LDR sensor readings.
  data = zeros(sampling_rate)
  # Loop forever
  while True:
    thingsIOdict.pop("values",None)
    for ii in range(sampling_rate):
      data[ii] = analogRead(PD_PIN) # read the analog LDR pin and put th value to the data array.
      delay(sampling_delay_ms)
    wham = hanning(sampling_rate)   # create a filter window with the correct size for our buffer length.
    fft_data = rfft(data * wham)    # compute the real fourier transform of the data times the window function.
    f = fftfreq(fftdim)             # generate the frequels
    #remove dc component and other slow frequency components of the spectrum.
    fft_data[0:3] = 0
    tmp_data = abs(fft_data)        
    heartbeat_frequency_index=  tmp_data.argmax()   # get the index of the frequency with the highest contribution to the spectra.
    heart_beat = heartbeat_frequency_index * sampling_rate / (fftdim/2 +1) /2  # convert the index to a physical frequency
    # sendSignal ('signal3',int(heart_beat)) # write the signal to wyliodrin plotter
    # create a timestamp for our datapoint. 
    dtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    thingsIOdict[u"values"] = [{u"key" : "biosensor", u"value" : int(heart_beat), u"unit" : u"Hz", u"type" : u"Frequency", u"datetime" : dtime}]
    userinput =  json.dumps(thingsIOdict)
    client.publish(TOPIC, payload=userinput)
    delay(1000) # read the heartbeat every 1000ms = 1s.

if __name__ == "__main__":
  main()



