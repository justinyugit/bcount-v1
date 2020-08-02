# Launches preview for in field / at home camera adjustments
# Created June 2019
# Written by Justin Yu


import time
import picamera
camera=picamera.PiCamera()
try:
    #camera.resolution=(960,720)
    camera.resolution=(1920,1080)
    camera.start_preview()
    time.sleep(9999)
    camera.stop_preview()
finally:
    camera.close()
