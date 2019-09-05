from constants import TimeStep,sensorPositions
from generalFunctions import getMean

class Sense:
    '''
    initialize sonar sensros and read them
    '''
    
    def __init__(self,robot):
        self.initializeSonarSensors(robot)

    def initializeSonarSensors(self,robot):
        self.ps = []
        psNames = [
            'ps0', 'ps1', 'ps2', 'ps3',
            'ps4', 'ps5', 'ps6', 'ps7'
        ]
        for i in range(8):
            self.ps.append(robot.getDistanceSensor(psNames[i]))
            self.ps[i].enable(TimeStep)
        self.sensorPositions = sensorPositions
        
    def readSensors(self,robot):
        '''
        read each sensor five times. delete highest and lowest value of each sensor.
        
        returns mean of remained values in a list.
        '''
        numOfReadings = 5
        numOfSensors = 8
        psValues = [[0 for y in range(numOfReadings)] for x in range(numOfSensors) ] 
        for i in range(numOfSensors):
            for j in range(numOfReadings):
                robot.step(TimeStep)
                psValues[i][j] = self.ps[i].getValue()         
        for i in range(numOfSensors):
            del(psValues[i][psValues[i].index(min(psValues[i]))])
            del(psValues[i][psValues[i].index(max(psValues[i]))])
        values=[]
        for i in range(numOfSensors):
            values.append(getMean(psValues[i])) 
        return values

    def readOneSensor(self,i,robot):
        return self.ps[i].getValue()