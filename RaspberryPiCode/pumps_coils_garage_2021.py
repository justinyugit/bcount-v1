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

def turn_on_wash():
    GPIO.output(12, True)
def turn_off_wash():
    GPIO.output(12, False)
def turn_on_r_punish():
    GPIO.output(17, True)
def turn_off_r_punish():
    GPIO.output(17, False)
def turn_on_r_reward():
    GPIO.output(4, True)
def turn_off_r_reward():
    GPIO.output(4, False)
def turn_on_l_punish():
    GPIO.output(24, True)
def turn_off_l_punish():
    GPIO.output(24, False)
def turn_on_l_reward():
    GPIO.output(25, True)
def turn_off_l_reward():
    GPIO.output(25, False)
def turn_on_r_coil():
    GPIO.output(18, True)
def turn_off_r_coil():
    GPIO.output(18, False)
def turn_on_l_coil():
    GPIO.output(23, True)
def turn_off_l_coil():
    GPIO.output(23, False)


turn_off_wash()
turn_off_r_punish()
turn_off_l_punish()
turn_off_r_reward()
turn_off_l_reward()
turn_off_l_coil()
turn_off_r_coil()

###########################################################


### Initialize and prime pumps

if (INIT_PUMPS):

    turn_on_wash()
    turn_on_r_punish()
    turn_on_r_reward()
    turn_on_l_punish()
    turn_on_l_reward()

    all_5_counter = 5
    start_time = time.time()
    while (all_5_counter):
        elapsed = time.time()-start_time
        if (elapsed >= WASH_PUMP_INIT_DURATION):
            turn_off_wash()
            all_5_counter-=1
        if (elapsed >= R_REWARD_PUMP_INIT_DURATION):
            turn_off_r_reward()
            all_5_counter-=1
        if (elapsed >= R_PUNISH_PUMP_INIT_DURATION):
            turn_off_r_punish()
            all_5_counter-=1
        if (elapsed >= L_PUNISH_PUMP_INIT_DURATION):
            turn_off_l_punish()
            all_5_counter-=1
        if (elapsed >= L_REWARD_PUMP_INIT_DURATION):
            turn_off_l_reward()
            all_5_counter-=1
else:
    print("not initializing pumps")


### Start test or run cycles



CYCLE_FLAG = 0 # If 0, Right, if 1, Left
while(True):
    try:
        with picamera.PiCamera() as camera:
            camera.framerate = 25
            camera.resolution = (960,720)
            name = str(time.strftime("%m-%d-%Y_%H%M%S"))

            # IF RANDOM YIELDS 1 -> Left
            # IF RANDOM YIELDS 0 -> Right
            CYCLE_FLAG = random.randrange(2)

            # Wash out precycle
            turn_on_wash()
            time.sleep(WASH_PUMP_RUN_DURATION)
            turn_off_wash()


            path = ""
            if(CYCLE_FLAG):
                path = "/mnt/usb/L" + name + ".h264"
                turn_on_l_coil()

                turn_on_l_reward()
                time.sleep(REWARD_DURATION_RUN)
                turn_off_l_reward()
    
                turn_on_r_punish()
                time.sleep(PUNISH_DURATION_RUN)
                turn_off_r_punish()

            else:
                path = "/mnt/usb/R" + name + ".h264"
                turn_on_r_coil()
                
                turn_on_r_reward()
                time.sleep(REWARD_DURATION_RUN)
                turn_off_r_reward()

                turn_on_l_punish()
                time.sleep(PUNISH_DURATION_RUN)
                turn_off_l_punish()
                    

            camera.start_recording(path)
            if(TEST):
                time.sleep(CYCLE_DURATION_TEST)
            else:
                time.sleep(CYCLE_DURATION_RUN)
            camera.stop_recording()

            # Make sure both coils are off regardless
            turn_off_l_coil()
            turn_off_r_coil()
            
                
    except:
        print("failed")

