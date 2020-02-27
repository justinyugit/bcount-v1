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
        plt.plot(xframe,yLFlat)
        plt.title('Left Side')
if type=="right":
    with open(csvPathR) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            yR.append(row)
        for sublist in yR:
            for item in sublist:
                yRFlat.append(item)
        for i in range(len(yRFlat)):
            xframe.append(i/1500)
        plt.plot(xframe,yRFlat)
        plt.title('Right Side')
            
            

plt.xlabel('Minutes since start')
plt.ylabel('Number of bees')
plt.show()

