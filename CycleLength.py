# Returns barchart of exact cycle lengths
# Created 8/18/20
# Written by Justin Yu

import sys
from matplotlib import pyplot as plt

waterFILE = sys.argv[1]
sugarFILE = sys.argv[2]

water = open(waterFILE, "r")
sugar = open(sugarFILE, "r")

# X has all the times
# Y has all the 0 and 1 representing water and sugar

X=[]
Y=[]
Date = water.readline()[4:6] + '/' + water.readline()[6:8] + '/' + water.readline()[0:4] 

#reset 3 places for first 3 lines
water = open(waterFILE, "r")
sugar = open(sugarFILE, "r")
for line in water:
    X.append(int(line[9:13]))   
    Y.append(0)

for line in sugar:
    X.append(int(line[9:13]))
    Y.append(1)

X, Y = zip(*sorted(zip(X,Y)))

Minutes = []
countMinutes = 0
Cycles = []
Times = []

if(len(str(X[0]))==4):
    Times.append(str(X[0])[0:2] + ":" + str(X[0])[2:4])
else:
    Times.append(str(X[0])[0:1] + ":" + str(X[0])[1:3])
for index in range(len(Y)):
    try:            
        if(Y[index]!=Y[index+1]):
            Cycles.append(Y[index])
            Minutes.append(countMinutes)
            countMinutes=0
            if(len(str(X[index]))==4):
                Times.append(str(X[index])[0:2] + ":" + str(X[index])[2:4])
            else:
                Times.append(str(X[index])[0:1] + ":" + str(X[index])[1:3])
            
        countMinutes=countMinutes+1
    except:
        Cycles.append(Y[index])
        Minutes.append(countMinutes)
        if(len(str(X[index]))==4):
            Times.append(str(X[index])[0:2] + ":" + str(X[index])[2:4])
        else:
            Times.append(str(X[index])[0:1] + ":" + str(X[index])[1:3])
Labels = []
countIndex = 0


for val in Cycles:
    if(val==0):
        Labels.append("W - " + str(Times[countIndex]))
        countIndex = countIndex+1
    elif(val==1):
        Labels.append("S - " + str(Times[countIndex]))
        countIndex = countIndex+1
print(Labels)
print(Minutes)
print(Cycles)
plt.xlabel("Minutes (Cycle Length)")
plt.barh(Labels,Minutes)

plt.title(Date)
for index, value in enumerate(Minutes):
    plt.text(value, index, str(int(value)))
plt.show()
