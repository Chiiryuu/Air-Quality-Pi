#Built-in libraries
import sys
import time
import datetime
import math
import requests
import json

#Sensor libraries
from grove.factory import Factory
from grove.adc import ADC
import RPi.GPIO as GPIO

#Lambda function for getting ms from time.time(), which returns seconds
millis = lambda: int(round(time.time() * 1000))


#Keep trying to upload until server responds
def uploadJson(url, data):
    try:
        resp = requests.post(url=url, json=data) # creates the actual request
        f = resp.json()
        return f
    except:
        print("Failed, retrying...")
        return uploadJson(url, data)

def main():
    #Get config file
    configDict = getDictFromFile("config.json")
    configDict['url']

    #Declare pins and variables
    adc = ADC()
    g_sensor = 0
    a_sensor = 0
    d_sensor = 0
    t_sensor = 0
    t_pin = 4
    a_pin = 0
    a5_pin = 2
    d_pin = 4
    d_duration = 0
    d_lpo = 0 # low pulse occupancy
    d_sampletime = 3*configDict['pollingTimeMS'] # milliseconds
    start_t = millis()

    t_sensor = Factory.getTemper("NTC-ADC", t_pin)
    GPIO.setup(d_pin, GPIO.IN)
    GPIO.add_event_detect(d_pin, GPIO.FALLING)
    timer = millis()

    #Declare value list used for upload
    valueList = [ [],[],[],[], [] ]
    data = []

    while True:
        if GPIO.event_detected(d_pin):
            end_t = millis()
            d_duration = end_t - timer
            d_lpo = d_lpo + d_duration
            timer = millis()

            #Repeat data pulling until all sensors have responsed two values
            if (millis()-start_t) > d_sampletime:
                start_t = millis()
                ratio = d_lpo/(d_sampletime)
                d_lpo = 0
                concentration = 1.1*math.pow(ratio,3)-3.8*math.pow(ratio,2)+520*ratio+0.62
                if (len(valueList[1]) < 2):
                    valueList[1].append(concentration)
                    valueList[4].append(time.time()*1000)
                    print('Dust: {} pcs/L\n'.format(valueList[1][-1]))

        g_sensor = adc.read(a5_pin)
        valueList[0].append(g_sensor)
        print('Gas: {}\n'.format(valueList[0][-1]))

        a_sensor = adc.read(a_pin)
        valueList[2].append(a_sensor)
        print('AirQ: {}\n'.format(valueList[2][-1]))

        t_sensor = t_sensor.tempature
        valueList[3].append(temperature)
        print('Temp: {} C\n'.format(valueList[3][-1]))

        td = {
            "timestamp": time.time()*1000,
            "MQ5": g_sensor,
            "airQuality": a_sensor,
            "temp": t_sensor,
            "Dust": d_sensor
        }
        data.appaned(td)

        #Upload two values from each sensor plus timestamps to serber
        if len(data) >= 2:
            payload = {
                "s_time": data[0]['timestamp'],
                "e_time": data[-1]['timestamp'],
                "data": data
            }
            print(uploadJson(configDict['url'], payload))

        time.sleep(configDict['pollingTimeMS']/1000)

    #Won't be reached, but typically you want this here to close the dust sensor.
    GPIO.cleanup()

if __name__ == '__main__':
    main()
