from matplotlib import pyplot as plt
import numpy as np
import cv2
import sys
import csv

#Initializes Background Reduction Object
fgbg=cv2.bgsegm.createBackgroundSubtractorMOG()

#Initializes bees count array used to output tracked dynamic foreground pixels
bees = [0]

#Intiailizes x array for frame count, and y array for left and right side bee count; 
dev_x=[0]
dev_yR=[0]
dev_yL=[0]

#Second argument specifies processing on "left" or "right" side.
xyz=sys.argv[2]

#Function brings in video from the first argument; while loop of 29900 frames is 4 seconds padding of the 20 minute video files.
def PROCESS(type):
    cap = cv2.VideoCapture(sys.argv[1])
    frames=0
    dev_x=[0]
    while(frames<29900):

        #returns ret of true/false if frame is grabbed
        ret, frame = cap.read()

        #sets region of interest in reference to the second argument
        if (type=="left"):
            roi=frame[250:450, 0:420]
        if (type=="right"):
            roi=frame[250:450, 540:960]

        #applies background reduction mask
        fgmask = fgbg.apply(roi)

        #provides live feed of masked video and original video in separate windows
        cv2.imshow('frame', fgmask)
        cv2.imshow('actual', roi)

        #applies contour function on the masked frame
        cnts = cv2.findContours(fgmask, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2]

        #sets lower and upperbound for contour size and determines whether in range of said bounds
        s1=5
        s2=400
        for cnt in cnts:
            if s1<cv2.contourArea(cnt)<s2:
                bees.append(cnt)

        #Commented out print to save time
        print(len(bees))
        frames=frames+1

        #Appends to left or right array, and rules out outliers of greater than 40 (result of video grain/artifacts)
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

        #empties bee count array for next iteration of the frames loop
        bees.clear()
        k = cv2.waitKey(1) & 0xff
        if k == ord('c'):
            break

#calls above function to process the argument-specified side "left" or "right"
PROCESS(xyz)


#writes the final arrays to respective csv file
if (xyz=="left"):
    with open('YL.csv', 'a') as left_file:
        csv_writer=csv.writer(left_file)
        csv_writer.writerow(dev_yL)
elif (xyz=="right"):
    with open('YR.csv', 'a') as right_file:
        csv_writer=csv.writer(right_file)
        csv_writer.writerow(dev_yR)


