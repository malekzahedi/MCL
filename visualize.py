from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure
from tornado import gen
from functools import partial
from threading import Thread
import time
import os.path
from constants import MapFile,EnvFile,OutputDirectory


class visualizeMap:
    """
    How to use: 

    function writeMap2File from class Map, writes coordinates of particles in a file with name of 

    {iter}.txt after every iteration is done.

    Type "bokeh serve --show visualize.py" in your terminal, opened in the directory of this project,

    and class visualizeMap will read those files and show map in your browser after every iteration.  
    """

    def __init__(self,mapFile,envFile):
        self.readMap(mapFile)
        self.readEnv(envFile)
        self.makeCoordinateMap()


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

    def makeMapReadyToshow(self):
        p = figure(plot_width=self.width*5, plot_height=self.height*5)
        p.square(self.X, self.Y, size=5, color="brown", alpha=1)
        return p

@gen.coroutine
def update(xu, yu):
    source.data = (dict(x=xu, y=yu))

def blocking_task():
    iter = 0
    while True:
        time.sleep(0.5)
        File = OutputDirectory + "{0}.txt".format(iter) 
        if os.path.isfile(File) :
            with open(File,"r") as f:
                x = [line.split() for line in f] 
            X=[]
            Y=[]
            if len(x):
                for i in range(len(x)):
                    X.append(float(x[i][0]))
                    Y.append(float(x[i][1]))
                iter = iter + 1    
                doc.add_next_tick_callback(partial(update, X, Y))

doc = curdoc()
map = visualizeMap(MapFile,EnvFile)
p = map.makeMapReadyToshow()

source = ColumnDataSource(data=dict(x=[0], y=[0]))
        
p.circle(x='x', y='y', source=source)
doc.add_root(p)
thread = Thread(target=blocking_task)
thread.start()
