#built-in libraries
import time
import datetime
import math
import json
import requests
#graphics.py
from graphics import *
#Custom-built python files
import graphs


#   Documentation for graphics
#   https://mcsp.wartburg.edu/zelle/python/graphics/graphics.pdf





#Functions

#strftime is built for time.time(), not s_time() used on the server
def epochToString(time):
    time = time/1000
    return datetime.datetime.fromtimestamp(time).strftime('%H:%M:%S %m/%d/%Y')

#Used to get data blocks from server
    #Keep trying until server responds
    
def getDictFromURL(url, s_time, e_time):
    try:
        blob = {
            's_time': s_time,
            'e_time': e_time
        }
        
        resp = requests.get(url=url, json=blob) # creates the actual request
        f = resp.json()
        return f
    except:
        print("Reconnecting...")
        errorBack.undraw()
        errorText.undraw()
        errorText.setText("Attempting to connect to Sensor...")
        try:
            errorBack.draw(display) 
            errorText.draw(display)
        except:
            print("Window closed! Killing program...")
            exit()
        #return getStringFromURL(url)

#These two are used only to read config file    
def getDictFromString(s):
    try:
        return json.loads(s)
    except:
        return None
       
def getDictFromFile(file):
    try:
        config = open(file, encoding='utf_8')
        return json.load(config)
    except:
        return None
        
#def getDictFromURL(url, s_time, e_time):
#    return getDictFromString(getStringFromURL(url, s_time, e_time))


#Setup Stuff (and evil global variables... so we can easily display errors)        
configDict = getDictFromFile("config.json")

displaySize = configDict['displaySize']
pollingTime = configDict['pollingTimeMS']
display = GraphWin(configDict['WindowTitle'],displaySize[0],displaySize[1])
display.setBackground(color_rgb(9,9,9))
background = Image(Point(displaySize[0]/2, displaySize[1]/2), configDict['background']) 
background.draw(display)
t0 = time.time()*1000
deltaT = pollingTime

errorText = Text(Point(displaySize[0]/2, 10),"Setting up...")
errorText.setFace("helvetica")
errorText.setSize(12)
errorText.setTextColor("Black")


errorBack = Rectangle(Point(displaySize[0]/4, -2), Point(displaySize[0]/4 * 3, 25))
errorBack.setFill("White")
errorBack.setWidth(3)

timeBack = Rectangle(Point(2*configDict['padding'], displaySize[1]-2), Point(displaySize[0] - 2*configDict['padding'], displaySize[1]-40))
timeBack.setFill("White")
timeBack.setWidth(3)

timeLine = Line(Point(displaySize[0]/2, displaySize[1]-2), Point(displaySize[0]/2, displaySize[1]-40))
timeLine.setWidth(3)

curTimeText = Text(Point(displaySize[0]/4, displaySize[1]-19),f"Current Time: {epochToString(t0)}")
curTimeText.setFace("helvetica")
curTimeText.setSize(12)
curTimeText.setTextColor("Black")

lastUpdateText = Text(Point(3*displaySize[0]/4, displaySize[1]-19),"Last Sensor Update: None")
lastUpdateText.setFace("helvetica")
lastUpdateText.setSize(12)
lastUpdateText.setTextColor("Black")

#After global variables settled, main begins

def main():
    #Draw the display
    print("Starting up...")
    errorBack.draw(display)
    errorText.draw(display)
    timeBack.draw(display)
    timeLine.draw(display)
    curTimeText.draw(display)
    lastUpdateText.draw(display)
    
    global t0
    global deltaT
    

    graphList = []

    graphX = 0
    graphY = 0

    previousTimestamp = t0 #- 86400 * 1000 #One day
    if (configDict['GrabLastDay']):
        previousTimestamp = previousTimestamp - 86400 * 1000 #One day previous

    #Create graph objects
    graphIndex = 0
    for graph in configDict['graphs']:
        if (graphIndex==0):
            graphX = displaySize[0]//4
            graphY = displaySize[1]//4 + configDict['padding']
        if (graphIndex==1):
            graphX = 3*displaySize[0]//4
            graphY = displaySize[1]//4 + configDict['padding']
        elif(graphIndex==2):
            graphX = displaySize[0]//4
            graphY = 3*displaySize[1]//4 - 3.5*configDict['padding']
        elif(graphIndex==3):
            graphX = 3*displaySize[0]//4
            graphY = 3*displaySize[1]//4 - 3.5*configDict['padding']
    
        graphList.append(
            graphs.Graph(display, Point(graphX ,graphY - configDict['padding'] ), configDict['graphs'][graph]['size'][0], configDict['graphs'][graph]['size'][1], configDict['graphs'][graph]['midpoint'], configDict['graphs'][graph]['range'], configDict['graphs'][graph]['dataPoints'], configDict['graphs'][graph]['title'],configDict['graphs'][graph]['color'],configDict['graphs'][graph]['units'])
            )
        graphIndex = graphIndex + 1
        
    #Observation loop, repeat for eternity, looking for new data
    print("Entering main loop...")
    #print(previousTimestamp)
    while (True):
        curTimeText.setText(f"Current Time: {epochToString(time.time()*1000)}")
    
        #Only check if it's time to check, as specified in the config
        if (deltaT>= pollingTime):
            t0 = round(time.time()*1000)
            
            dataDicts = getDictFromURL(configDict['url'], (previousTimestamp+1), t0)
            #print(dataDicts)
            
            
            #Check to see if we got a good response
            if (dataDicts != None and len(dataDicts) > 0 and dataDicts != {'result': 'failure'}):
                #print(dataDicts)
                print("Requested data from server...")
                for dataDict in dataDicts:
                    if (previousTimestamp < dataDict['e_time']):
                        previousTimestamp = dataDict['e_time']
                    #Retrieve data from each data block (Each one holds 2 pieves of data)
                    for datum in dataDict['data']:
                        
                        #Actually read in data
                        
                        previousTimestamp = datum['timestamp']
                        errorBack.undraw()
                        errorText.undraw()
                        graphList[0].addPoint(  round(datum['temp']) )
                        graphList[1].addPoint(  round(datum['Dust']) )
                        graphList[2].addPoint(   round(datum['airQuality'])  )
                        graphList[3].addPoint(  round(datum['MQ5']) )
                            #print(epochToString(dataDict['timestamp']//100))
                            #if (previousTimestamp == datum['timestamp']):
                #print(previousTimestamp)    
                lastUpdateText.setText(f"Last Sensor Update: {epochToString(previousTimestamp)}")
                
            #If we didn't retrieve any data, notify user
            elif(dataDicts != None and len(dataDicts) == 0):  
                print("No new data to get!")
                errorBack.undraw()
                errorText.undraw()
                errorText.setText("Awaiting new data from Sensor...")
                #Check if window was closed
                try:
                    errorBack.draw(display) 
                    errorText.draw(display)
                except:
                    print("Window closed! Killing program...")
                    exit()
        deltaT = round((time.time()*1000 - t0))
        

        
    
if __name__ == '__main__':
    main()

