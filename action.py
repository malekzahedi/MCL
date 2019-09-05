from constants import Speed,AxleLENGTH,WheelRADIUS,TimeStep
from math import radians
from random import random


def decideAction(sensorModel,DistanceValues):
    '''
    takes sensorModel and distanceValues to decide action

    returns dictionary of rotation and move
    '''
    move = 1
    rotation = 0
    ran = random()
    if  (DistanceValues[0] + DistanceValues[7])/2 < 7  :
        if  DistanceValues[0] > 2 and DistanceValues[7] >  2  :
            move = 2
        else:
            if DistanceValues[1]<3 and DistanceValues[0]<3:
                rotation = 45
            elif DistanceValues[6]<3 and DistanceValues[7]<3:
                rotation = -45
            elif DistanceValues[0] < 3 and DistanceValues[7] <  3  :
                if ran >= 0.5:
                    rotation = 90
                else:
                    rotation = -90
            else: 
                rotation = 90
    elif (DistanceValues[0] + DistanceValues[7])/2 >= 7:
        move = 5
    
    return {"rotation":rotation,"move":move}

def FirstAction(sensorModel,DistanceValues):
    '''
    takes sensorModel and distanceValues to decide action for the first time

    robot tries to approach to the nearest wall

    returns dictionary of rotation and move
    '''

    minValue = min(DistanceValues)
    minValueIndex = DistanceValues.index(minValue)
    if minValueIndex == 7 or minValueIndex == 0 :
        rotation = 0
    if minValueIndex == 3 or minValueIndex == 4 :
        rotation = 180
    if minValueIndex == 2 :
        rotation = -90
    if minValueIndex == 5 :
        rotation = 90
    if minValueIndex == 1 :
        rotation = -45
    if minValueIndex == 6 :
        rotation = 45
    
    if minValue > 2 and  minValue < 7:
        move = 2
    elif minValue >= 7:
        move = 5
    else:
        move = 0
    return {"rotation":rotation,"move":move}

def rotate(goal,l0,r0,leftMotor,rightMotor,leftPosiotionSensor,rightPosiotionSensor,robot):
    '''
    rotates the robot in radians
    '''
    if goal ==0:
        return [l0,r0,0]
    if goal < 0:
        goal = radians(goal+5)
    else:
        goal = radians(goal-5)
    if leftMotor.getVelocity() == 0.0:
        leftMotor.setVelocity(-goal/abs(goal)*Speed)
        rightMotor.setVelocity(goal/abs(goal)*Speed)
    while robot.step(TimeStep)!=-1:    
        l = leftPosiotionSensor.getValue()
        r = rightPosiotionSensor.getValue()
        dl = (l - l0) * WheelRADIUS 
        dr = (r - r0) * WheelRADIUS 
        da = (dr-dl) / AxleLENGTH
        if abs(da) >= abs(goal):
            robot.step(TimeStep)
            leftMotor.setVelocity(0.0)
            rightMotor.setVelocity(0.0)
            break
    robot.step(TimeStep)
    return [l,r,da]

def move(goal,l0,r0,leftMotor,rightMotor,leftPosiotionSensor,rightPosiotionSensor,robot,sonarSensors,sensorModel):
    '''
    moves the robot in centimeter
    '''
    if goal == 0:
        return [l0,r0,0]
        
    goal = goal / 100
    if leftMotor.getVelocity() == 0.0:
        leftMotor.setVelocity(Speed)
        rightMotor.setVelocity(Speed)
    while robot.step(TimeStep)!=-1:    
        l = leftPosiotionSensor.getValue()
        r = rightPosiotionSensor.getValue()
        dl = (l - l0) * WheelRADIUS
        dr = (r - r0) * WheelRADIUS
        dx = (dl+dr)/2

        #collision avoidance and target reaching , mastmalli
        sensor0 = sonarSensors.readOneSensor(0,robot)
        sensor7 = sonarSensors.readOneSensor(7,robot)
        sensor1 = sonarSensors.readOneSensor(1,robot)
        sensor6 = sonarSensors.readOneSensor(6,robot)
        sensor0 = sensorModel.SensorValuesToDistance([sensor0])
        sensor7 = sensorModel.SensorValuesToDistance([sensor7])
        sensor1 = sensorModel.SensorValuesToDistance([sensor1])
        sensor6 = sensorModel.SensorValuesToDistance([sensor6])
        if  dx >= goal or (sensor0[0] < 1 and sensor1[0] <1) or (sensor0[0] < 1 and sensor7[0] <1 ) or (sensor7[0] <1 and sensor6[0] <1):
            robot.step(TimeStep)
            leftMotor.setVelocity(0.0)
            rightMotor.setVelocity(0.0)
            break
    robot.step(TimeStep)
    return [l,r,dx]
