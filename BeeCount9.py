##  12/7/19: Cleaned Up BeeCount8Texture.py
##  Python3

from matplotlib import pyplot as plt
import numpy as np
import cv2
import sys
import csv
import os

csvPath = os.path.dirname(os.path.realpath(sys.argv[1]))

##  initializes Background Reduction Object
fgbg = cv2.createBackgroundSubtractorKNN(250,500,False)

##  bees array used to output tracked dynamic foreground pixels
bees = [0]

##  x array for frame count, and y array for left and right side bee count
dev_x = [0]
dev_yL = [0]
dev_yR = [0]

##  xyz is the second argument when calling Python3 BeeCount9.py
xyz = sys.argv[2]

##  standard deviation of greyscale values
def getContourSTD(contour, image1):
    mask = np.zeros(image1.shape, dtype="uint8")
    cv2.drawContours(mask, [contour], -1, 255, -1)
    mean, stddev = cv2.meanStdDev(image1, mask=mask)
    return stddev[0][0]

##  calls video from first argument; while loop of 29900 frames is 19 min 56 sec
def PROCESS(type):
    cap = cv2.VideoCapture(sys.argv[1])
    frames = 0
    dev_x = [0]
    while (frames < 29900):
        ret, frame = cap.read()
        ##  sets a region of interest of 200x360 pixels
        if (type == "left"):
            roi = frame[250:450, 0:360]
        elif (type == "right"):
            roi = frame[250:450, 600:960]
        ##  applies background reduction mask
        fgmask = fgbg.apply(roi)
        ##  applies colored frame to a masked frame and converts to gray scale
        colorMaskFrame = roi * (fgmask[:,:,None].astype(roi.dtype))
#        cv2.imshow('colorMaskFrame', colorMaskFrame)
        grayMaskFrame = cv2.cvtColor(colorMaskFrame, cv2.COLOR_BGR2GRAY)
#        cv2.imshow('grayMaskFrame', grayMaskFrame)
#        cv2.imshow('originalFrame', roi)
#        cv2.imshow('binaryMaskFrame', fgmask)
        ##  applies contour function on masked frame
        cnts = cv2.findContours(fgmask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
        Lower = 25
        Upper = 400
        for cnt in cnts:
            if Lower < cv2.contourArea(cnt) < Upper and getContourSTD(cnt, grayMaskFrame) > 15:
                bees.append(cnt)
#                print(getContourSTD(cnt, grayMaskFrame))
#            elif Lower < cv2.contourArea(cnt) < Upper:
#                print(getContourSTD(cnt, grayMaskFrame))
#        print("#ofBees: " + str(len(bees)) + " frame:" + str(frames))
        frames = frames + 1
        ##  rules out outliers of greater than 40 "bees" -> artifacts / grain
        if len(bees)<40 and type=="left":
            dev_yL.append(len(bees))    
            dev_x.append(frames/1500)
        elif len(bees)<40 and type=="right":
            dev_x.append(frames/1500)
            dev_yR.append(len(bees))
        elif len(bees)>=40 and type=="left":
            print("too high")
            dev_yL.append(0)
            dev_x.append(frames/1500)
        elif len(bees)>=40 and type=="right":
            dev_x.append(frames/1500)
            dev_yR.append(0)
        ##  empties bee count array for next iteration of the frames loop
        bees.clear()
        ##  waitKey(1) -> continuous waitKey(0) -> frame by frame keyboard input
        k = cv2.waitKey(1) & 0xff
        if k == ord('c'):
            break

##  calls above function to process the argument-specified side "left" or "right"
PROCESS(xyz)


##  writes the final arrays to respective csv file
if (xyz=="left"):
    with open(csvPath + 'left.csv', 'a') as left_file:
        csv_writer=csv.writer(left_file)
        csv_writer.writerow(dev_yL)
elif (xyz=="right"):
    with open(csvPath + 'right.csv', 'a') as right_file:
        csv_writer=csv.writer(right_file)
        csv_writer.writerow(dev_yR)

