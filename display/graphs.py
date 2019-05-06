#built-in libraries
import time
import math
#graphics.py
from graphics import *

#   Documentation for graphics
#   https://mcsp.wartburg.edu/zelle/python/graphics/graphics.pdf

#class definition
class Graph():

    #graph constuctor
    def __init__(self, displayIn, center, width, height, midVal, range, maxPoints=10, title = "Graph", color = "Red", units=""):
        
        #initializers
        
        self.display = displayIn
        self.graphCenter = center
        
        self.title = title
        self.units = units
        
        self.padding = 20
        
        self.color = color
        
        self.mean = 0
        self.nMean = 0
        
        
        self.points = []
        
        self.graphWidth = width
        self.graphHeight = height
        
        self.midVal =midVal
        self.range = range
        
        self.maxPoints = maxPoints
        
        self.pointSpace = self.graphWidth//(self.maxPoints-1)
        
        
        #Draw graph object
        
        self.graphBack = Rectangle(Point(self.graphCenter.getX() - self.graphWidth//2 - 3*self.padding, self.graphCenter.getY() - self.graphHeight//2 - 2*self.padding), Point(self.graphCenter.getX() + self.graphWidth//2 + 3*self.padding, self.graphCenter.getY() + self.graphHeight//2 + 2.7*self.padding))
        self.graphBack.setFill("White")
        self.graphBack.setWidth(3)
        self.graphBack.draw(self.display)
        
        self.titleLine = Line(Point(self.graphCenter.getX() - self.graphWidth//2 - self.padding, self.graphCenter.getY() - self.graphHeight//2 - 10), Point(self.graphCenter.getX() + self.graphWidth//2 + self.padding, self.graphCenter.getY() - self.graphHeight//2 - 10))
        self.titleLine.setWidth(3)
        self.titleLine.draw(self.display)
        
        self.meanSeparator = Line(Point(self.graphCenter.getX() - self.graphWidth//2 - self.padding, self.graphCenter.getY() + self.graphHeight//2 + 20), Point(self.graphCenter.getX() + self.graphWidth//2 + self.padding, self.graphCenter.getY() + self.graphHeight//2 + 20))
        self.meanSeparator.setWidth(3)
        self.meanSeparator.draw(self.display)
        
        self.rightLine = Line(Point(self.graphCenter.getX() - self.graphWidth//2 - self.padding,self.graphCenter.getY() - self.graphHeight//2 - 10), Point(self.graphCenter.getX() - self.graphWidth//2 - self.padding,self.graphCenter.getY() + self.graphHeight//2 + 20),  )
        self.rightLine.setWidth(3)
        self.rightLine.draw(self.display)
        
        self.leftLine = Line(Point(self.graphCenter.getX() + self.graphWidth//2 + self.padding, self.graphCenter.getY() - self.graphHeight//2 - 10), Point(self.graphCenter.getX() + self.graphWidth//2 + self.padding, self.graphCenter.getY() + self.graphHeight//2 + 20),  )
        self.leftLine.setWidth(3)
        self.leftLine.draw(self.display)
        
        self.counter = 0
        
        self.titleSize = len(title) * 5
        
        self.lineList = []
        
        self.lineList.append((Line(Point(self.graphCenter.getX() - self.graphWidth//2 - 18, self.graphCenter.getY() + (self.graphHeight//2 * -1  )), Point(self.graphCenter.getX() + self.graphWidth//2 + 18, self.graphCenter.getY() + (self.graphHeight//2 * -1  ))),
        Text(Point(self.graphCenter.getX()- self.graphWidth//2 - 40 , self.graphCenter.getY() + (self.graphHeight//2 * -1  )),f"{self.midVal+self.range}"))
        )
        
        self.lineList.append((Line(Point(self.graphCenter.getX() - self.graphWidth//2 - 18, self.graphCenter.getY() + (self.graphHeight//2 * -0.5  )), Point(self.graphCenter.getX() + self.graphWidth//2 + 18, self.graphCenter.getY() + (self.graphHeight//2 * -0.5  ))),
        Text(Point(self.graphCenter.getX()- self.graphWidth//2 - 40 , (self.graphCenter.getY() + (self.graphHeight//2 * -0.5  ))),f"{self.midVal+(self.range//2)}"))
        )
        
        self.lineList.append((Line(Point(self.graphCenter.getX() - self.graphWidth//2 - 18, self.graphCenter.getY()), Point(self.graphCenter.getX() + self.graphWidth//2 + 18, self.graphCenter.getY())),
        Text(Point(self.graphCenter.getX()- self.graphWidth//2 - 40 , (self.graphCenter.getY() )),f"{self.midVal}"))
        )
        
        self.lineList.append((Line(Point(self.graphCenter.getX() - self.graphWidth//2 - 18, self.graphCenter.getY() + (self.graphHeight//2 * 0.5  )), Point(self.graphCenter.getX() + self.graphWidth//2 + 18, self.graphCenter.getY() + (self.graphHeight//2 * 0.5  ))),
        Text(Point(self.graphCenter.getX()- self.graphWidth//2 - 40 , (self.graphCenter.getY() + (self.graphHeight//2 * 0.5  ))),f"{self.midVal-(self.range//2)}"))
        )
        
        self.lineList.append((Line(Point(self.graphCenter.getX() - self.graphWidth//2 - 18, self.graphCenter.getY() + (self.graphHeight//2 * 1  )), Point(self.graphCenter.getX() + self.graphWidth//2 + 18, self.graphCenter.getY() + (self.graphHeight//2 * 1  ))),
        Text(Point(self.graphCenter.getX()- self.graphWidth//2 - 40 , (self.graphCenter.getY() + (self.graphHeight//2 * 1  ))),f"{self.midVal-self.range}"))
        )
    
        
        for line in self.lineList:
            line[0].setWidth(1)
            line[0].setFill("Gray")
            line[0].draw(self.display)
            line[1].setFace("helvetica")
            line[1].setSize(10)
            line[1].draw(self.display)
        
        
        
       # self.textBack = Rectangle(Point(self.graphCenter.getX() - self.titleSize, self.graphCenter.getY() - self.graphHeight//2 - self.padding - 20), Point(self.graphCenter.getX() + self.titleSize, self.graphCenter.getY() - self.graphHeight//2 - self.padding))
       # self.textBack.setFill("White")
       # self.textBack.setWidth(3)
       # self.textBack.draw(self.display)
       
        self.meanLine = Line(Point(self.graphCenter.getX() - self.graphWidth//2 - 5, (self.graphCenter.getY())), Point(self.graphCenter.getX() + self.graphWidth//2 + 5, (self.graphCenter.getY())))
        self.meanLine.setWidth(2)
        self.meanLine.setFill("Black")
        self.meanLine.draw(self.display)
        
        self.nmeanLine = Line(Point(self.graphCenter.getX() - self.graphWidth//2 - 5, (self.graphCenter.getY())), Point(self.graphCenter.getX() + self.graphWidth//2 + 5, (self.graphCenter.getY())))
        self.nmeanLine.setWidth(2)
        self.nmeanLine.setFill(self.color)
        self.nmeanLine.draw(self.display)

        self.titleText = Text(Point(self.graphCenter.getX(), self.graphCenter.getY() - self.graphHeight//2 - 25),self.title+f" ({self.units})")
        self.titleText.setFace("helvetica")
        self.titleText.setSize(12)
        self.titleText.setTextColor(self.color)
        self.titleText.draw(self.display)
        
        self.lastMean = Text(Point(self.graphCenter.getX(), self.graphCenter.getY() + self.graphHeight//2 + 30),f"Running Mean: {self.mean}{self.units}")
        self.lastMean.setFace("helvetica")
        self.lastMean.setSize(10)
        self.lastMean.setTextColor("Black")
        self.lastMean.draw(self.display)
        
        self.lastnMean = Text(Point(self.graphCenter.getX(), self.graphCenter.getY() + self.graphHeight//2 + 45),f"Current Mean: {self.mean}{self.units}")
        self.lastnMean.setFace("helvetica")
        self.lastnMean.setSize(10)
        self.lastnMean.setTextColor(self.color)
        self.lastnMean.draw(self.display)
        

        #Add a point, given a y value

    def addPoint(self, y):
        if (len(self.points) == self.maxPoints):
            oldPoint = self.points.pop(0)
            for element in oldPoint:
                if (element != None and type(element)!=int):
                    element.undraw()
            self.points[0][1].undraw()
            self.points[0] = (self.points[0][0], None, self.points[0][2], self.points[0][3], self.points[0][4])
            for point in self.points:
                for element in point:
                    if (element != None and type(element)!=int):
                        element.move(-self.pointSpace,0)
                                      
        self.newPoint = Point(self.graphCenter.getX() + (len(self.points)*self.pointSpace) - self.graphWidth//2 , (self.graphCenter.getY() + (self.graphHeight//2 * (self.midVal-y)//(self.range)  )))
        self.circle = Circle( self.newPoint ,  3)
        #circle.setWidth(2)
        self.circle.setFill(self.color)
        self.line = None
        if (len(self.points)>0):
            self.line = Line(self.points[len(self.points)-1][0], self.newPoint)
        
        self.pointText = Text(Point(self.newPoint.getX(), (self.graphCenter.getY() + self.graphHeight//2) +10 ),str(y))
        self.pointText.setFace("helvetica")
        self.pointText.setSize(10)
        self.pointText.setTextColor("Black")
            
        
        self.pointGroup = (self.newPoint, self.line, self.circle ,self.pointText, y) 
        self.points.append( self.pointGroup   )
        self.counter = self.counter + 1
        if (len(self.points) == 1):
            self.mean = y
        else:
            self.mean = ((self.mean)*(self.counter-1) + y) / self.counter
        self.lastMean.setText(f"Running Mean: {round(self.mean,1)}{self.units}")
        self.meanLine.move(0,    (self.graphCenter.getY() + (self.graphHeight//2 * (self.midVal-self.mean)//(self.range)  )) - self.meanLine.getP1().getY())
        for element in self.pointGroup:
            if (element != None and type(element)!=int):
                element.draw(self.display)
        if (len(self.points)>1):
            self.points[len(self.points)-2][2].undraw()
            self.points[len(self.points)-2][2].draw(self.display)
            self.points[len(self.points)-2][3].undraw()
            self.points[len(self.points)-2][3].draw(self.display)
        self.nMean = 0    
        for point in self.points:
                self.nMean = self.nMean + point[4]
        self.nMean = self.nMean / len(self.points)
        self.lastnMean.setText(f"Current Mean: {round(self.nMean,1)}{self.units}")
        self.nmeanLine.move(0,    (self.graphCenter.getY() + (self.graphHeight//2 * (self.midVal-self.nMean)//(self.range)  )) - self.nmeanLine.getP1().getY())
