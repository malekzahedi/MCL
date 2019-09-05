from math import pi

SensorTrueValues = [1,2,4,7]

MapFile = "D:\\Majid\\UT\\Class\\Advanced Robotics\\Project\\MapSakht\\map.txt"
EnvFile = "D:\\Majid\\UT\\Class\\Advanced Robotics\\Project\\MapSakht\\env.txt"
SensorModelDir = "D:\\Majid\\UT\\Class\\Advanced Robotics\\Project\\Test\\SampleEnvironment\\Emtehan\\"
OutputDirectory = ""

WheelRADIUS = 0.02
AxleLENGTH = 0.052
NumberOfParticles = 10000
randomPerIter = 1000
TimeStep = 16
Speed = 1.0
MaxIter =50
RobotRadius = 7.1/2
RealMode = 2
MaxReading = 10

linearMotionModelData = {12:{"mean":12,"SD":0.5551/100},
                        5:{"mean":5,"SD":0.2400/100},
                        2:{"mean":2,"SD":0.1183/100},
                        0:{"mean":0,"SD":0}}

rotationalMotionModelData ={180:{"mean":180,"SD":3.4871/10},
                        -180:{"mean":-180,"SD":6.8235/10},
                         90:{"mean":90,"SD":5.7131/10},
                        -90:{"mean":-90,"SD":3.6878/10},
                        0:{"mean":0,"SD":0},
                        45:{"mean":45,"SD":2.85655/10},
                        -45:{"mean":-45,"SD":1.8439/10}}

sensorPositions = [1.27 - pi/2 ,0.77 - pi/2,0 - pi/2,5.21 - pi/2,4.21 - pi/2,3.14 - pi/2,2.37 - pi/2,1.87 - pi/2]
