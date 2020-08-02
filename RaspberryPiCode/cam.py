import picamera
from time import sleep
import time
import datetime
import os
try:
    while True:
        with picamera.PiCamera() as camera:
            camera.framerate = 25
            camera.resolution = (960,720)

            name = str(datetime.datetime.now())
            #name = str(time.strfttime("%m%d%Y-%H%M%S"))
            path = ("/mnt/usb/" + name + ".h264")
            camera.start_recording(path)
            sleep(1200)
            camera.stop_recording()
except:
    os.system("./mounter.sh")
    
