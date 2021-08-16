import RPi.GPIO as GPIO
import time
import picamera
import datetime
import random

GPIO.setmode(GPIO.BCM)

################### QUICK SET VARIABLES ###################

INIT_PUMPS = True              
TEST = True                  
L_COIL_ON = False
R_COIL_ON = False
CYCLE_DURATION_TEST = 100 # seconds #
CYCLE_DURATION_RUN = 10800 # seconds; read from schedule #
WASH_PUMP_INIT_DURATION = 10 # seconds; for priming #
WASH_PUMP_RUN_DURATION = 10 # seconds #
R_REWARD_PUMP_INIT_DURATION = 10 # seconds; for priming #
R_PUNISH_PUMP_INIT_DURATION = 10 # seconds; for priming #
L_REWARD_PUMP_INIT_DURATION = 10 # seconds; for priming #
L_PUNISH_PUMP_INIT_DURATION = 10 # seconds; for priming #

REWARD_DURATION_RUN = 5 # seconds; after primed - actual dispense #
PUNISH_DURATION_RUN = 5 # seconds; after primed - actual dispense #

###########################################################

GPIO.setup(12, GPIO.OUT) # Wash_Pump
GPIO.setup(17, GPIO.OUT) # R_Punish_Pump
GPIO.setup(4, GPIO.OUT) # R_Reward_Pump
GPIO.setup(24, GPIO.OUT) #L_Punish_Pump
GPIO.setup(25, GPIO.OUT) # L_Reward_Pump
GPIO.setup(18, GPIO.OUT) # R_Coil_On
GPIO.setup(23, GPIO.OUT) # L_Coil_On

GPIO.output(12 , False)
GPIO.output(17 , False)
GPIO.output(4 , False)
GPIO.output(24 , False)
GPIO.output(25 , False)
GPIO.output(18 , False)
GPIO.output(23 , False)

###########################################################


### Initialize and prime pumps

if (INIT_PUMPS):
    GPIO.output(12, True)
    GPIO.output(17, True)
    GPIO.output(4, True)
    GPIO.output(24, True)
    GPIO.output(25, True)
    all_5_counter = 5
    start_time = time.time()
    while (all_5_counter):
        elapsed = time.time()-start_time
        if (elapsed >= WASH_PUMP_INIT_DURATION):
            GPIO.output(12, False)
            all_5_counter-=1
        if (elapsed >= R_REWARD_PUMP_INIT_DURATION):
            GPIO.output(4, False)
            all_5_counter-=1
        if (elapsed >= R_PUNISH_PUMP_INIT_DURATION):
            GPIO.output(17, False)
            all_5_counter-=1
        if (elapsed >= L_PUNISH_PUMP_INIT_DURATION):
            GPIO.output(24, False)
            all_5_counter-=1
        if (elapsed >= L_REWARD_PUMP_INIT_DURATION):
            GPIO.output(25, False)
            all_5_counter-=1
else:
    print("not initializing pumps")


### Start test or run cycles

CYCLE_FLAG = 0
while(True):
    if(TEST):
        time.sleep(CYCLE_DURATION_TEST)
        GPIO.output(12, True)
        time.sleep(WASH_PUMP_RUN_DURATION)
        GPIO.output(12, False)
    else:
        try:
            with picamera.PiCamera() as camera:
                camera.framerate = 25
                camera.resolution = (960,720)
                name = str(time.strftime("%m-%d-%Y_%H%M%S"))

                # IF RANDOM YIELDS 1 -> Left
                # IF RANDOM YIELDS 0 -> Right
                CYCLE_FLAG = random.randrange(2)

                # Wash out precycle
                GPIO.output(12, True)
                time.sleep(WASH_PUMP_RUN_DURATION)
                GPIO.output(12, False)


                path = ""
                if(CYCLE_FLAG):
                    path = "/mnt/usb/L" + name + ".h264"
                    GPIO.output(23, True) # Turn on Left Coil

                    GPIO.output(25, True) # Turn on Left Reward Pump
                    time.sleep(REWARD_DURATION_RUN)
                    GPIO.output(25, False) # Turn off Left Reward Pump

                    GPIO.output(17, True) # Turn on Right Punish Pump
                    time.sleep(PUNISH_DURATION_RUN)
                    GPIO.output(17, False) # Turn off Right Punish Pump
                else:
                    path = "/mnt/usb/R" + name + ".h264"
                    GPIO.output(18, True) # Turn on Right Coil

                    GPIO.output(4, True) # Turn on Right Reward Pump
                    time.sleep(REWARD_DURATION_RUN)
                    GPIO.output(4, False) # Turn off Right Reward Pump

                    GPIO.output(24, True) # Turn on Left Punish Pump
                    time.sleep(PUNISH_DURATION_RUN)
                    GPIO.output(24, False) # Turn off Left Punish Pump
                    

                camera.start_recording(path)
                time.sleep(CYCLE_DURATION_RUN)
                camera.stop_recording()

                # Make sure both coils are off regardless
                GPIO.output(18, False)
                GPIO.output(23, False)
                
        except:
            print("failed")

