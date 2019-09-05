'''
Authors : malekzahedi and assari75 (github accounts)
'''

from map import Map
from sensorModel import SensorModel
from constants import RealMode,MaxIter,SensorModelDir,MapFile,EnvFile,OutputDirectory,linearMotionModelData,rotationalMotionModelData,TimeStep
from motionModel import MotionModel
from controller import Robot,Motor
from particleFilter import particleFilter
from sense import Sense
from action import rotate
import time

robot = Robot()

#load sensor model, motion model and map.
s = SensorModel(SensorModelDir)
m = Map(MapFile,EnvFile,OutputDirectory)
l = MotionModel(linearMotionModelData,rotationalMotionModelData)

#initialize sensors
sonarSensors = Sense(robot)

#initialize motors
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
rightMotor.setPosition(float('inf'))
leftMotor.setPosition(float('inf'))
rightMotor.setVelocity(0.0)
leftMotor.setVelocity(0.0)
motors = {"left":leftMotor,"right":rightMotor}

#initialize encoders
leftPosiotionSensor = robot.getPositionSensor("left wheel sensor")
rightPosiotionSensor = robot.getPositionSensor("right wheel sensor")
leftPosiotionSensor.enable(TimeStep)
rightPosiotionSensor.enable(TimeStep) 
positionSensors = {"left":leftPosiotionSensor,"right":rightPosiotionSensor}

#initialize particleFilter class
p = particleFilter(m,s,l,sonarSensors,motors,positionSensors,robot)

#conecting to the real robot
while True:
    robot.step(TimeStep)
    Mode = robot.getMode()
    if Mode == RealMode:
        break

#main loop
while p.iter<MaxIter:
   p.run()
