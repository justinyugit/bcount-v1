#This is a version 8 where I disable detectShadows in the background subtractor, although in theory it should track and remove shadows, it does better when it is disabled. I did not apply the texture method to the contours yet, but I will try.
#removed shadows based on texture 12/7/19


from matplotlib import pyplot as plt
import numpy as np
import cv2
import sys
import csv

#Initializes Background Reduction Object
#fgbg=cv2.bgsegm.createBackgroundSubtractorMOG()
fgbg=cv2.createBackgroundSubtractorKNN(250,500,False)

#fgbg=cv2.bgsegm.createBackgroundSubtractorMOG(250,500,False)

#Initializes bees count array used to output tracked dynamic foreground pixels
bees = [0]

#Intiailizes x array for frame count, and y array for left and right side bee count; 
dev_x=[0]
dev_yR=[0]
dev_yL=[0]

#Second argument specifies processing on "left" or "right" side.
xyz=sys.argv[2]

#standard deviation greyscale function
def getContourInfo(contour, image1):
    mask = np.zeros(image1.shape,dtype="uint8")
    cv2.drawContours(mask, [contour], -1,255,-1)
    mean, stddev= cv2.meanStdDev(image1,mask=mask)
    std = stddev[0][0]
    return std

#Function brings in video from the first argument; while loop of 29900 frames is 4 seconds padding of the 20 minute video files.
def PROCESS(type):
    cap = cv2.VideoCapture(sys.argv[1])
    frames=0
    dev_x=[0]
    while(frames<29900):

        #returns ret of true/false if frame is grabbed
        ret, frame = cap.read()

        #Trying a smaller ROI 12/4/19
        if (type=="left"):
            roi=frame[250:450, 0:360]
        if (type=="right"):
            roi=frame[250:450, 600:960]
            

#        sets region of interest in reference to the second argument
#        if (type=="left"):
#            roi=frame[250:450, 0:420]
#        if (type=="right"):
#            roi=frame[250:450, 540:960]

        #Create blank black image
        #blankFrame=np.zeros(shape=[200,420],dtype=np.uint8)
        
        #applies background reduction mask
        fgmask = fgbg.apply(roi)
        #roi.copyTo(blankFrame, fgmask)
        
        colorMaskFrame=roi*(fgmask[:,:,None].astype(roi.dtype))
        cv2.imshow('color', colorMaskFrame)
        grayMaskFrame=cv2.cvtColor(colorMaskFrame, cv2.COLOR_BGR2GRAY)
        
        cv2.imshow('gray', grayMaskFrame)
        #provides live feed of masked video and original video in separate windows
        #cv2.imshow('frame', fgmask)
        cv2.imshow('actual', roi)

        #applies contour function on the masked frame
        cnts = cv2.findContours(fgmask, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2]
        #cnts = cv2.findContours(roi, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        #sets lower and upperbound for contour size and determines whether in range of said bounds
        #originally s1=5, set to 15 seems to be working well
        s1=25
        s2=400

        #calculate standard deviation from the avg bee count to see whether the contour is a shadow or bee
        
        
        for cnt in cnts:
            if s1<cv2.contourArea(cnt)<s2 and getContourInfo(cnt, grayMaskFrame)>15:
                bees.append(cnt)
                cv2.drawContours(fgmask, [cnt], 0,(255,0,0), thickness=cv2.FILLED)
                print(getContourInfo(cnt, grayMaskFrame))
            elif s1<cv2.contourArea(cnt)<s2:
                print(getContourInfo(cnt, grayMaskFrame))
                
        cv2.imshow('frame', fgmask)
        #Commented out print to save time
        print("#ofBees: " + str(len(bees)) + " frame:" + str(frames))
        
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
        k = cv2.waitKey(0) & 0xff
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


