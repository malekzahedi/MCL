from numpy.random import normal
import math
from generalFunctions import interpolation

class MotionModel:
    def __init__(self,linearMotionModelData,rotationalMotionModelData):
        self.linearMotionModelData = linearMotionModelData.copy()
        self.rotationalMotionModelData = rotationalMotionModelData.copy()

    def moveParticles(self,particles,target,theta,map):
        """
        move all particles to desired angle and distance.

        angle must be in degrees,target in meter.

        returns num of deleted particles.
        """
        num = len(particles[0])  
        
        if target<0:
            target =0
        
        if theta!=0:
            noiseAngle = normal(self.rotationalMotionModelData[theta]["mean"],self.rotationalMotionModelData[theta]["SD"],num)
        else:
            noiseAngle = []
            for i in range(num):
                 noiseAngle.append(0)

        if target ==0:
            for i in range(len(particles[0])):
                particles[2][i] = particles[2][i] + math.radians(noiseAngle[i]) 
            return 0
        
        target = target * 100
        numOfDeleted = 0
        if target > 2 :
            meanL = interpolation(2,self.linearMotionModelData[2]["mean"],5,self.linearMotionModelData[5]["mean"],target) 
            SDL =   interpolation(2,self.linearMotionModelData[2]["SD"],5,self.linearMotionModelData[5]["SD"],target)              
        if target <= 2:
            meanL = interpolation(0,self.linearMotionModelData[0]["mean"],2,self.linearMotionModelData[2]["mean"],target) 
            SDL =   interpolation(0,self.linearMotionModelData[0]["SD"],2,self.linearMotionModelData[2]["SD"],target)  
            
        print("mean move:",meanL)
        print("SD move:",SDL)

        noiseDistance = normal(meanL,SDL,num)

        step =int(target / map.unit) 
        for j in range(1,step+1):
            for i in  reversed(range(len(particles[0]))):
                particles[0][i] = particles[0][i] + noiseDistance[i]*j/step * math.cos(particles[2][i] + math.radians(noiseAngle[i]))
                particles[1][i] = particles[1][i] + noiseDistance[i]*j/step * math.sin(particles[2][i] + math.radians(noiseAngle[i]))
                particles[2][i] = particles[2][i] + math.radians(noiseAngle[i])
                if map.isInImpossiblePosition(particles[0][i],particles[1][i]):
                    del(particles[0][i])
                    del(particles[1][i])
                    del(particles[2][i])
                    del(particles[3][i])
                    del(particles[4][i])
                    numOfDeleted = numOfDeleted + 1
                    continue
                if not j==step:
                    particles[2][i] = particles[2][i] - math.radians(noiseAngle[i])
                    particles[0][i] = particles[0][i] - noiseDistance[i]*j/step * math.cos(particles[2][i] + math.radians(noiseAngle[i]))
                    particles[1][i] = particles[1][i] - noiseDistance[i]*j/step * math.sin(particles[2][i] + math.radians(noiseAngle[i]))
        return numOfDeleted
