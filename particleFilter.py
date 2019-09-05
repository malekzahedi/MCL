from constants import NumberOfParticles,TimeStep,WheelRADIUS,randomPerIter,RobotRadius,MaxReading
from random import random,uniform
from action import decideAction,rotate,move,FirstAction
from generalFunctions import getMean,getGaussian
import math
from statistics import median
from time import sleep
from math import pi
#import matplotlib.pyplot as plt

class particleFilter:

    def __init__(self,map,sensorModel,MotionModel,sonarSensors,motors,positionSensors,robot):
        self.robot = robot
        self.map = map
        self.sensorModel = sensorModel
        self.MotionModel = MotionModel
        self.sonarSensors = sonarSensors
        self.motors = motors
        self.positionSensors = positionSensors
        self.iter = 0
        self.FirstMove = True
        self.numOfDeletedParticles = 0 
        self.Mean = 0
        self.Median = 0
        print(self.sensorModel.sensorModelData)

    def run(self):

        if self.FirstMove:
            self.particles = self.map.generateRandom(NumberOfParticles)
            #self.map.showMap(self.iter,self.particles)
            self.map.writeMap2file(self.iter,self.particles)

        self.iter = self.iter +1
        print("Iteration:",self.iter)
        
        kenar = True
        
        #reading encoders initial value
        self.robot.step(TimeStep)
        self.l0 = self.positionSensors["left"].getValue()
        self.r0 = self.positionSensors["right"].getValue()
        print("l0:",self.l0,"r0:",self.r0)
        
        #reading sensors
        self.sonarSensorsValues = self.sonarSensors.readSensors(self.robot) 
        print("Sensor values:",self.sonarSensorsValues)
        self.DistanceValues = self.sensorModel.SensorValuesToDistance(self.sonarSensorsValues)
        print("Sensor distance values:",self.DistanceValues)
        bestSensorIndex = self.DistanceValues.index(min(self.DistanceValues))
        print("Best sensor index:",bestSensorIndex)
        
        if self.DistanceValues[bestSensorIndex] > MaxReading:
            kenar = False
        
        #updating weights based on measurments
        if kenar:
            for i in range(len(self.particles[0])):
                self.particles[4][i] = self.map.getDistanceToNearestWall(self.particles[0][i],self.particles[1][i],self.sonarSensors.sensorPositions[bestSensorIndex] + self.particles[2][i])
                self.sensorModel.DistanceToSensorValue(self.particles[4][i],bestSensorIndex)        
            self.UpdateWeights(self.sensorModel,bestSensorIndex)
        
        self.Mean = getMean(self.particles[3])
        print("Mean of weights:",self.Mean)
        self.Median = median(self.particles[3])
        print("Median of weights:",self.Median)
        
        #showing weights
        '''a = plt.hist(self.particles[3])
        plt.show(a)
        print("weights",self.particles[3])'''
        
        #deleting particles by a cutoff on their weight
        if kenar:
            self.numOfDeletedParticles = self.deleteParticles(self.Median/2)
            print("Num of deletd partciles by cutoff:",self.numOfDeletedParticles)
        else:
            self.numOfDeletedParticles = 0
            
        #making a decision for robot's next move
        if (self.FirstMove == True) :
            decision = FirstAction(self.sensorModel,self.DistanceValues)
            self.FirstMove = False
        else:
            decision = decideAction(self.sensorModel,self.DistanceValues)
        print("Decision:",decision)
        rotation = decision["rotation"]
        linearMove = decision["move"]
                
        #moving robot
        odeometryResult = rotate(rotation,self.l0,self.r0,self.motors["left"],self.motors["right"],self.positionSensors["left"],self.positionSensors["right"],self.robot)
        self.l0 = odeometryResult[0] 
        self.r0 = odeometryResult[1]
        da = odeometryResult[2]
        print("da:",da)
        odeometryResult = move(linearMove,self.l0,self.r0,self.motors["left"],self.motors["right"],self.positionSensors["left"],self.positionSensors["right"],self.robot, self.sonarSensors,self.sensorModel)
        self.l0 = odeometryResult[0] 
        self.r0 = odeometryResult[1]
        dx = odeometryResult[2]
        print("dx:",dx)
        
        #moving particles       
        num = self.MotionModel.moveParticles(self.particles,dx,rotation,self.map) 
        self.numOfDeletedParticles = self.numOfDeletedParticles + num
        
        #printing some data
        print("Num of deleted partciles by move:",num)
        print("Num of deleted particles:",self.numOfDeletedParticles)
        print("Num of paricles after deletions:",len(self.particles[0]))
        
        #generating some random particles
        newParticels1 = self.map.generateRandom(randomPerIter)
        
        #resampling
        if kenar:
            newParticels2 = self.resample(self.Mean,self.map)
            for i in range(len(newParticels1)):
                newParticels1[i].extend(newParticels2[i])
            self.combineOldAndNewParticles(newParticels1)
        else:
            self.combineOldAndNewParticles(newParticels1)
        print("Num of paricles after gen:",len(self.particles[0]))
        
        #visualizing
        #self.map.showMap(self.iter,self.particles)
        self.map.writeMap2file(self.iter,self.particles)
        
        
    def deleteParticles(self,chance):
        """
        delets particles by probability of weight < chance

        returns number of deleted particles
        """
        numOfDeleted = 0
        
        for i in reversed(range(len(self.particles[0]))):
            if self.particles[3][i] <= chance:
                del(self.particles[0][i])
                del(self.particles[1][i])
                del(self.particles[2][i])
                del(self.particles[3][i])
                del(self.particles[4][i])
                numOfDeleted = numOfDeleted +1 
        return numOfDeleted

    def combineOldAndNewParticles(self,newParticles):
        for i in range(len(newParticles[0])):
            self.particles[0].append(newParticles[0][i])
            self.particles[1].append(newParticles[1][i])
            self.particles[2].append(newParticles[2][i])
            self.particles[3].append(newParticles[3][i])
            self.particles[4].append(newParticles[4][i])

    def UpdateWeights(self, sensorModel, MainSensor):
        probability = []
        Sum = 0            
        for i in range(len(self.particles[0])):
            mean = sensorModel.DistanceToSensorValue(self.particles[4][i], MainSensor)
            sigma = sensorModel.CalculateSigma(self.particles[4][i], MainSensor)
            x = sensorModel.DistanceToSensorValue(self.DistanceValues[MainSensor]+RobotRadius,MainSensor) 
            prob = getGaussian(x , mean, sigma)
            probability.append(prob)
            Sum += prob
        
        if Sum==0:
            for i in range(len(self.particles[0])):
                self.particles[3][i] = 1/NumberOfParticles
        else:
            for i in range(len(self.particles[0])):
                self.particles[3][i] = probability[i] / Sum

    def resample(self,weight,map):
        '''
        resamples around particles whose weights are bigger than a specified limit.
        '''
        
        X = []
        Y = []
        theta = []
        W = []
        distance = []
        numOfGoodParticles = 0
        for i in range(len(self.particles[0])):
            if self.particles[3][i] > weight:
                numOfGoodParticles = numOfGoodParticles + 1
        numOfNewParticles =  self.numOfDeletedParticles - randomPerIter
        print("Num of new particles in resampling:",numOfNewParticles)
        if numOfGoodParticles==0:
            return map.generateRandom(NumberOfParticles-randomPerIter)
        ran = random()
        if ran >=0.7:
            ran = 1
        else:
            ran = -1    
        M = int(numOfNewParticles/numOfGoodParticles) + ran
        axis = [0,pi/2,pi,3*pi/2,2*pi]
        print("Num of new particles around good particles:", M )
        for i in range(len(self.particles[0])):
            if self.particles[3][i] > weight:
                distIn4Axis =[]
                for j in range(4):
                    distIn4Axis.append(map.getDistanceToNearestWallTillMax(self.particles[0][i],self.particles[1][i],axis[j],RobotRadius))
                while M:
                    while True:
                        x = self.particles[0][i] + uniform(-max(distIn4Axis[2],RobotRadius) ,max(distIn4Axis[0],RobotRadius))
                        y = self.particles[1][i] + uniform(-max(distIn4Axis[1],RobotRadius) ,max(distIn4Axis[3],RobotRadius))
                        t = self.particles[2][i] + uniform(math.radians(-5),math.radians(5))
                        if not map.isInImpossiblePosition(x,y):
                            X.append(x)
                            Y.append(y)
                            theta.append(t)
                            W.append(0)
                            distance.append(0)
                            break
                    M = M-1
                M = int(numOfNewParticles/numOfGoodParticles) + ran
        return [X,Y,theta,W,distance]
