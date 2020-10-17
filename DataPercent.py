# Creates Bar Graphs of total bees per cycle in each day for statistical analysis
# Created 8/16/20
# Written by Justin Yu

import csv
from matplotlib import pyplot as plt
import sys
import os
plt.rcParams.update({'font.size':13})
xframe=[]
yR=[]
yL=[]
yLFlat=[]
yRFlat=[]
type=sys.argv[1]
fig,ax = plt.subplots()
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
    
#reset Date and time for previous few lines
water = open(waterFILE, "r")
sugar = open(sugarFILE, "r")

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


WaterTotal=0
SugarTotal=0
WATERCYCLES=[]
SUGARCYCLES=[]

Cycles = []

for index in range(len(YPLOT)):
    try:
        if(YPLOT[index]!=YPLOT[index+1]):
            Cycles.append(YPLOT[index])
    except:
        Cycles.append(YPLOT[index])


for index in range(len(YPLOT)):
    if(YPLOT[index]==0):
        try:
            WaterTotal=WaterTotal+yLFlat[index]
        except:
            pass
        try:
            if(YPLOT[index]!=YPLOT[index+1]):
                WATERCYCLES.append(WaterTotal)
                print(str(WaterTotal) + "water")
                WaterTotal=0
        except:
            WATERCYCLES.append(WaterTotal)
            print(str(WaterTotal) + "water")
            WaterTotal=0
    elif(YPLOT[index]==1):
        try:
            SugarTotal=SugarTotal+yLFlat[index]
        except:
            pass
        try:
            if(YPLOT[index]!=YPLOT[index+1]):
                SUGARCYCLES.append(SugarTotal)
                print(str(SugarTotal) + "Sugar")
                SugarTotal=0
        except:
            SUGARCYCLES.append(SugarTotal)
            print(str(SugarTotal) + "Sugar")
            SugarTotal=0


Labels = []
Bars = []
TotalBee=0
countSugar=1
countWater=1
for val in Cycles:
    if(val==0):
        TotalBee=TotalBee+WATERCYCLES[countWater-1]
        countWater=countWater+1
    elif(val==1):
        TotalBee=TotalBee+SUGARCYCLES[countSugar-1]
        countSugar=countSugar+1
countSugar=1
countWater=1
for val in Cycles:
    if(val==0):
        Labels.append("Punish " + str(countWater))
        Bars.append(WATERCYCLES[countWater-1])
        countWater=countWater+1
    elif(val==1):
        Labels.append("Reward " + str(countSugar))
        Bars.append(SUGARCYCLES[countSugar-1])
        countSugar=countSugar+1

for val in Labels:
    print(val[0]+"labels")
for i in range(len(Bars)):
    Bars[i]=round(Bars[i]/TotalBee*100,2)
    
bar_plot= plt.bar(Labels,Bars)
#for index, value in enumerate(Bars):
#   #answer=str(round(value/TotalBee*100,2))
#    plt.text(value, index, value)

for i in range(len(bar_plot)):
    if(Labels[i][0]=='R'):
        bar_plot[i].set_color('#00FF00')
    else:
        bar_plot[i].set_color('r')

def autolabel(rects):
    for idx,rect in enumerate(bar_plot):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., .99*height,
                Bars[idx],
                ha='center', va='bottom', rotation=0,fontweight='bold')
autolabel(bar_plot)
plt.title(Date,fontweight='bold')
plt.ylabel("Percentage of Total Bees",fontweight='bold')

plt.show()
