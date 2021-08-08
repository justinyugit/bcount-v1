import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

################### QUICK SET VARIABLES ###################

INIT_PUMPS = True              
TEST = True                  
L_COIL_ON = False
R_COIL_ON = False
CYCLE_DURATION_TEST = 100 # seconds #
CYCLE_DURATION_RUN = 0 # seconds; read from schedule #
WASH_PUMP_INIT_DURATION = 10 # seconds; for priming #
WASH_PUMP_RUN_DURATION = 10 # seconds #
R_REWARD_PUMP_INIT_DURATION = 10 # seconds #
R_PUNISH_PUMP_INIT_DURATION = 10 # seconds #
L_REWARD_PUMP_INIT_DURATION = 10 # seconds #
L_PUNISH_PUMP_INIT_DURATION = 10 # seconds #

###########################################################

GPIO.setup(12, GPIO.OUT) # Wash_Pump
GPIO.setup(17, GPIO.OUT) # R_Punish_Pump
GPIO.setup(4, GPIO.OUT) # R_Reward_Pump
GPIO.setup(24, GPIO.OUT) #L_Punish_Pump
GPIO.setup(25, GPIO.OUT) # L_Reward_Pump
GPIO.setup(18, GPIO.OUT) # R_Coil_On
GPIO.setup(23, GPIO.OUT) # L_Coil_On

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
    # Read from schedule and do stuff


### Start test or run cycles

while(True):
    if(TEST):
        time.sleep(CYCLE_DURATION_TEST)
        GPIO.output(12, True)
        time.sleep(WASH_PUMP_RUN_DURATION)
        GPIO.output(12, False)
    else:
        # Read from schedule and do stuff
        print("THIS IS THE REAL CYCLE")

