from math import exp,pi,sqrt

 
def getMean(data):
    '''
    takes a list and returns average
    '''
    sum = 0 
    num = 0
    for x in data:
        sum = x + sum
        num = num + 1
    return sum/num

def getStandardDeviation(data):
    '''
    takes a list and returns standard deviation 

    uses getMean()
    '''
    mean = getMean(data)
    sum = 0
    num = 0
    for x in data:
        sum = (x-mean)**2 + sum
        num = num + 1
    return (sum/num)**0.5   

def getGaussian(x, mean=0.0, sigma=1.0):
    '''
    takes x, mean, and SD and returns gaussian
    '''
    x = float(x - mean) / sigma
    return exp(-x*x/2.0) / sqrt(2.0*pi) / sigma

def interpolation(x1, y1, x2, y2, x3):
    '''
    a linear interpolation. 
    
    line is drawn between given points (x1,y1) and (x2,y2).

    returns y3 corresponds to x3.

    '''
    return y1 + (y2-y1)/(x2-x1)*(x3-x1)

