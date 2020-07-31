import RPi.GPIO as GPIO
from time import sleep
import datetime

import os

sleep(2)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
sleep(2)

try:
    
    while(True):
        dateString = str(datetime.datetime.now())
        if(GPIO.input(18)):
            os.system('date +"%Y%m%d_%H%M%S" >> /mnt/usb/sugar.txt')
        elif(GPIO.input(18)==0):
            os.system('date +"%Y%m%d_%H%M%S" >> /mnt/usb/water.txt')
        sleep(60)

except:
    GPIO.cleanup()
