from generalFunctions import getMean, getStandardDeviation,interpolation
from constants import SensorTrueValues

class SensorModel():
    
    def __init__(self,sensorDataDir):
        self.makeSensorModelDictionary(sensorDataDir)

    def readData(self,fileName):
        data = []
        f = open(fileName,'r')
        for x in f:
            data.append(x)
        data = [x.strip() for x in data] 
        data = [float(x) for x in data]
        return data

    def makeSensorModelDictionary(self,sensorDataDir):
        self.sensorModelData = []
        for x in range(0,8):
            dic = {}
            for y in SensorTrueValues:
                data = self.readData(sensorDataDir +"siroosEmtehan{0}_{1}.txt".format(x,y))
                mean = getMean(data)
                #SD = getStandardDeviation(data)
                SD = mean / 7
                dic.update({y:{"mean":mean,"SD":SD}})
            self.sensorModelData.append(dic)
    
    def DistanceToSensorValue(self, distance,MainSensor):        
        if distance <= 2:
            SensorValue = interpolation(1, self.sensorModelData[MainSensor][1]["mean"], 2, self.sensorModelData[MainSensor][2]["mean"], distance)
        elif distance > 2 and distance <= 4:
            SensorValue = interpolation(2, self.sensorModelData[MainSensor][2]["mean"], 4, self.sensorModelData[MainSensor][4]["mean"], distance)
        elif distance > 4:
            SensorValue = interpolation(4, self.sensorModelData[MainSensor][4]["mean"], 7, self.sensorModelData[MainSensor][7]["mean"], distance)
        return SensorValue 

    def SensorValuesToDistance(self, SensorValues):
        Distances = []
        for i in range(len(SensorValues)):
            if SensorValues[i] >= self.sensorModelData[i][2]["mean"]:
                Distances.append(interpolation(self.sensorModelData[i][1]["mean"], 1, self.sensorModelData[i][2]["mean"], 2, SensorValues[i]))
            elif SensorValues[i] < self.sensorModelData[i][2]["mean"] and SensorValues[i] >= self.sensorModelData[i][4]["mean"] :
                Distances.append(interpolation(self.sensorModelData[i][2]["mean"], 2, self.sensorModelData[i][4]["mean"], 4, SensorValues[i]))
            elif SensorValues[i] < self.sensorModelData[i][4]["mean"] :
                Distances.append(interpolation(self.sensorModelData[i][4]["mean"], 4, self.sensorModelData[i][7]["mean"], 7, SensorValues[i]))
        for i in range(len(Distances)):
            if Distances[i]<0:
                Distances[i]=0            
        return Distances

    def CalculateSigma(self, distance, MainSensor):
        if distance <= 2:
            Sigma = interpolation(1, self.sensorModelData[MainSensor][1]["SD"], 2, self.sensorModelData[MainSensor][2]["SD"], distance)
        elif distance > 2 and distance <= 4:
            Sigma = interpolation(2, self.sensorModelData[MainSensor][2]["SD"], 4, self.sensorModelData[MainSensor][4]["SD"], distance)
        elif distance > 4 :
            Sigma = interpolation(4, self.sensorModelData[MainSensor][4]["SD"], 7, self.sensorModelData[MainSensor][7]["SD"], distance)
        return Sigma
