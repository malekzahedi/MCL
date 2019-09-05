'''
A code to extract sensor model of e-puck

Authors : malekzahedi and assari75 (github accounts)
'''

from controller import Robot
from constants import RealMode

import time

TimeStep = 64
robot = Robot()
numOfSensors = 8
numOfReadnig = 50
TrueSensorValues = [1,2,4,7,12]

sonarSensors = []
psNames = [
   'ps0', 'ps1', 'ps2', 'ps3',
   'ps4', 'ps5', 'ps6', 'ps7'
]
for i in range(numOfSensors):
   sonarSensors.append(robot.getDistanceSensor(psNames[i]))
   sonarSensors[i].enable(TimeStep)

#conecting to the real robot
while True:
    robot.step(TimeStep)
    Mode = robot.getMode()
    if Mode == RealMode:
        break

#main loop
while True:    
    for i in range(numOfSensors):
        for d in range(len(TrueSensorValues)):
            f = open("{0}_{1}.txt".format(i,TrueSensorValues[d]),"w")
            for j in range(numOfReadnig):
                robot.step(TimeStep)
                x = sonarSensors[i].getValue() 
                f.write(str(x)+"\n")
                print("sensor ",i," true value ",TrueSensorValues[d]," x ",x)
            f.close()
            print("num of sensor:",i,"range:",TrueSensorValues[d]," finished")
            time.sleep(6)
        time.sleep(12)
    break