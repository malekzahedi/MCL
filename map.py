from bokeh.plotting import figure, output_file, show
from functools import partial
from random import random
from math import pi,floor,cos,sin
 
class Map:
    
    ''' 
    takes mapFile address, envFile adddress, and OutputDirectory to make the map
    '''

    def __init__(self,mapFile,envFile,OutputDirectory):
        self.readMap(mapFile)
        self.readEnv(envFile)
        self.makeCoordinateMap()
        self.OutputDirectory = OutputDirectory

    def readMap(self,fileAddress):
        with open(fileAddress) as f:
            self.mapArray = [line.split() for line in f] 
            self.numOflines = len(self.mapArray)
            self.numOfColoumns = len(self.mapArray[0])
            #self.mapArray.reverse()
            for i in range(self.numOflines):
                self.mapArray[i].reverse()

    def readEnv(self,fileAddress):
        with open(fileAddress) as f:
            env = [line.split() for line in f] 
        self.height = int(env[0][0])
        self.width = int(env[0][1])
        self.scale = int(env[0][2])
        self.unit = 1/ self.scale
        self.realHeight = self.height / self.scale
        self.realWidth = self.width / self.scale

    def makeCoordinateMap(self):
        self.X = []
        self.Y = []
        for y in range(self.numOflines):
            for x in range(self.numOfColoumns):
                if self.mapArray[y][x] == '1':
                    self.X.append(x/self.scale)
                    self.Y.append(y/self.scale)

    def showMap(self,iter,particle):
        File = self.OutputDirectory + "mapAtIteration{0}.html".format(iter)
        output_file(File)
        p = figure(plot_width=int(self.width*5), plot_height=int(self.height*5))
        p.square(self.X, self.Y, size=2.5, color="brown", alpha=1)
        p.circle(particle[0],particle[1])
        show(p)

    def writeMap2file(self,iter,particles):
        File = self.OutputDirectory + "{0}.txt".format(iter)
        f = open(File,"w")
        for i in range(len(particles[0])):
            f.write(str(particles[0][i])+" "+str(particles[1][i])+"\n")
        f.close()

    def generateRandom(self,M):
        X = []
        Y = []
        Theta = []
        W = []
        distance = []
        while M:
            while True:
                x = random()* (self.realWidth-1)
                y = random() * (self.realHeight-1)
                t = random()*2*pi
                if not self.isInImpossiblePosition(x,y):  
                    X.append(x)
                    Y.append(y)
                    Theta.append(t)
                    W.append(1/M)
                    distance.append(0)
                    break
            M=M-1
        return [X,Y,Theta,W,distance]

    def continuous2discret(self,x,y):
        disX = floor(x* self.scale)
        disY = floor(y* self.scale)
        return [disX,disY]

    def isInImpossiblePosition(self,x,y):
        disX,disY = self.continuous2discret(x,y)
        if disX >=self.width or disY>=self.height or disX<0 or disY<0:
            return True
        if self.mapArray[disY][disX]=='1':
            return True
        return False

    def isOnWall(self,x,y):
        disx,disy = self.continuous2discret(x,y)
        if self.mapArray[disy][disx]=='1':
            return True
        return False

    def isOutOfMap(self,x,y):       
        disX,disY = self.continuous2discret(x,y)
        if disX >=self.width or disY>=self.height or disX<0 or disY<0:
            return True
        return False

    def getDistanceToNearestWall(self,x,y,theta):
        """
        theta in radians
        """
        newX = x
        newY = y
        step = self.unit /2
        i = 0
        while True:
            dist = i * step
            newX = newX + cos(theta) * step
            newY = newY + sin(theta) * step
            if self.isOnWall(newX,newY):
                return dist
            if self.isOutOfMap(newX,newY):
                return dist - step
            i = i + 1

    def getDistanceToNearestWallTillMax(self,x,y,theta,Max):
        """
        theta in radians
        """
        newX = x
        newY = y
        step = self.unit /2
        i = 0
        while True:
            dist = i * step
            if dist > Max:
                return dist
            newX = newX + cos(theta) * step
            newY = newY + sin(theta) * step
            if self.isOnWall(newX,newY):
                return dist
            if self.isOutOfMap(newX,newY):
                return dist - step
            i = i + 1

