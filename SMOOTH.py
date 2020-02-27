import csv
from matplotlib import pyplot as plt
import sys
from numpy import trapz
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import os

xframe=[]
yR=[]
yL=[]
yLFlat=[]
yRFlat=[]
yDIFF=[]
Rside=[]
Lside=[]
RSMOOTH=[]
LSMOOTH=[]

#this argument is used to determine the name of the csv's
name=sys.argv[1]
csvPath = os.path.dirname(os.path.realpath(name))
csvPathL = csvPath + "left.csv"
csvPathR = csvPath + "right.csv"
print(csvPathL)



with open(csvPathL) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    for row in csv_reader:
        yL.append(row)
    for sublist in yL:
        for item in sublist:
            yLFlat.append(item)
    for i in range(len(yLFlat)):
        xframe.append(i/1500)
        

with open(csvPathR) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    for row in csv_reader:
        yR.append(row)
    for sublist in yR:
        for item in sublist:
            yRFlat.append(item)

        




npL = np.asarray(yLFlat)
npR = np.asarray(yRFlat)
npDIFF = npR-npL


#1 minute interval is 25*60 frames = 1500

for i in range(len(npDIFF)):
    if npDIFF[i] >= 0:
        Rside.append(npDIFF[i])
        Lside.append(0)
    elif npDIFF[i] < 0:
        Lside.append(abs(npDIFF[i]))
        Rside.append(0)

#UNFINISHED##### Has small issue of printing the last 100 frames also to the array, but not too important because it is just 4 seconds
##when calculating average, need to not include zeroes somehow
framesForDiff=0
AveragedSmoothData=[]
while(framesForDiff<(len(npDIFF))):
    lower=framesForDiff
    upper=framesForDiff+3000
    temporaryLower=framesForDiff
    temporaryUpper=framesForDiff+3000
    sum=0
    while(temporaryLower<temporaryUpper and temporaryLower<(len(npDIFF))):
        sum+=npDIFF[temporaryLower]
        temporaryLower+=1
    #append 100 of the sum/100 to the averagedsmoothdata array
    print(sum/3000)
    for b in range(3000):
        AveragedSmoothData.append(sum/3000)
    sum=0
    
    framesForDiff=framesForDiff+3000






xSmooth=[]
for abc in range(len(AveragedSmoothData)):
    xSmooth.append(abc/1500)


plt.plot(xSmooth,AveragedSmoothData)

plt.axhline(linewidth=2, color='r')
#plt.title('Smooth 120sec: Positive = More Right, Vice Versa')
plt.title(csvPath)
plt.xlabel('Minutes since start')
plt.ylabel('Number of bees')
plt.show()

