# Creates Bar Graphs of total bees per cycle in each day for statistical analysis
# Created 8/16/20
# Written by Justin Yu

import csv
from matplotlib import pyplot as plt
import sys
import os

xframe=[]
yR=[]
yL=[]
yLFlat=[]
yRFlat=[]
type=sys.argv[1]

#this argument is used to determine the name of the csv's
name=sys.argv[2]
csvPath = os.path.dirname(os.path.realpath(name))
csvPathL = csvPath + "left.csv"
csvPathR = csvPath + "right.csv"
print(csvPathL)

if type=="left":
    with open(csvPathL) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            yL.append(row)
        for sublist in yL:
            for item in sublist:
                yLFlat.append(item)
        for i in range(len(yLFlat)):
            xframe.append(i/1500)
#        plt.plot(xframe,yLFlat, linewidth=.1)


waterFILE = sys.argv[3]
sugarFILE = sys.argv[4]

water = open(waterFILE, "r")
sugar = open(sugarFILE, "r")

#Get Date and First Log Time
Date = water.readline()[4:6] + '/' + water.readline()[6:8] + '/' + water.readline()[0:4] 
if(int(water.readline()[9:13])<int(sugar.readline()[9:13])):
    Time = water.readline()[9:11] + ":" + water.readline()[11:13]
else:
    Time = sugar.readline()[9:11] + ":" + sugar.readline()[11:13]
    

X=[]
Y=[]



for line in water:
    X.append(int(line[9:13]))
    Y.append(0)

for line in sugar:
    X.append(int(line[9:13]))
    Y.append(1)

X, Y = zip(*sorted(zip(X,Y)))
YPLOT = []

for val in Y:
    for _ in range(1500):
        YPLOT.append(val)


for yIndex in range(len(YPLOT)):
    if(YPLOT[yIndex]!=YPLOT[yIndex+1]):
        print(YPLOT[yIndex])
