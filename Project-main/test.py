import RPi.GPIO as GPIO
import os
#from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from datetime import datetime,date
from mq2test import *

dorrPin = 18
warningPin= 17
trigPin = 23
echoPin = 24
MAX_DISTANCE = 220          # define the maximum measuring distance, unit: cm
flamePin= 21
pirPin=12
resetPin=19
securityMode=20
buzzerPin=27


timeOut = MAX_DISTANCE*60   # calculate timeout according to the maximum measuring distance

def get_time():
    time=datetime.now().strftime(" %H:%M:%S ")
    dat= date.today().strftime(" %D")
    return time,dat

"""def print_time():
    tid=get_time()
    print("the date is :", tid)"""

def dorr_Setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(warningPin,GPIO.OUT)
	GPIO.setup(dorrPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	#GPIO.setup(dorrPin,GPIO.IN)
	GPIO.setup(flamePin,GPIO.IN)
	GPIO.setup(pirPin, GPIO.IN)
	GPIO.setup(resetPin, GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(securityMode,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(buzzerPin,GPIO.OUT)
	
	
def ultra_Setup():
    GPIO.setmode(GPIO.BCM)      # use PHYSICAL GPIO Numbering
    GPIO.setup(trigPin, GPIO.OUT)   # set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN)    # set echoPin to INPUT mode
    
def pulseIn(pin,level,timeOut): # obtain pulse time of a pin under timeOut
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime

def getSonar():     # get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH)      # make trigPin output 10us HIGH level 
    time.sleep(0.00001)     # 10us
    GPIO.output(trigPin,GPIO.LOW) # make trigPin output LOW level 
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut)   # read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0     # calculate distance with sound speed 340m/s
    time.sleep(1)
    return distance

def en_Dorr():
    try:  
        if  (GPIO.input(dorrPin)==GPIO.LOW)  :
            alarm_On(3)
        else:
            alarm_Off()
            return 0
    except:
        pass
            
def ultra_Sonic():
    try:
        dis = getSonar()
        if  (dis<= 8.0) and (dis>0) :
            alarm_On(2)
        else:
            alarm_Off()
            return 0
    except:
        pass
            
   
# ideer :larm counter under dagen    
def alarm_On(alarm_Type):  # types 1 = flame, 2 = ultrasonic, 3 = dorr,  4 = PIR sensor, 5= smoke
    #GPIO.output(warningPin,GPIO.HIGH)
    if (alarm_Type==1) or (alarm_Type==5):
        GPIO.output(warningPin,GPIO.HIGH)
        GPIO.output(buzzerPin,GPIO.HIGH)
    else:
        GPIO.output(warningPin,GPIO.HIGH)
    tid=get_time()
    print("type of alarm is : %s at : %s" %(alarm_Type, tid))
    time.sleep(1)
    
# ideer: ta med type of larm för att deaktivera, kanske lösenord
def alarm_Off():
    if (GPIO.input(resetPin)==GPIO.LOW) :
        GPIO.output(warningPin,GPIO.LOW)
        GPIO.output(buzzerPin,GPIO.LOW)
    else:
        return 0
    
 
def destroy():
	GPIO.cleanup()
	


def get_Flame():
    if (GPIO.input(flamePin)==GPIO.LOW):
        alarm_On(1)
        time.sleep(0.05)
    else:
        alarm_Off()
        return 0

	
def get_Movement():
    #GPIO.add_event_detect(pirPin,GPIO.BOTH,bouncetime=300)
    while True:
        #test=GPIO.event_detected(pirPin)
        if (GPIO.input(pirPin)==GPIO.HIGH):
            alarm_On(4)
            time.sleep(0.05)
        else:
            alarm_Off()
            return 0
def get_Smoke():
    while True:
        COlevel=readadc(mq2_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)
        SmokeTrigger = ((COlevel/1024.)*3.3)

        if SmokeTrigger > 0.7:
            alarm_On(5)
            #print("Gas leakage")
            #print("Current Gas AD vaule = " +str("%.2f"%((COlevel/1024.)*3.3))+" V")
            time.sleep(0.05)

        else:
            time.sleep(0.05)
            return 0
def secure_Not_Home():
    
    for i in range(5):
        if i==0:
            get_Flame()
        elif i==1:
            ultra_Sonic()
        elif i==2:
            en_Dorr()
        elif i==3:
            get_Smoke()
        else:
            get_Movement()
def secure_At_Home():
    for i in range(2):
        if i==0:
            get_Flame()
        else:
            get_Smoke()
    
def loop():
    while True:
        
        if (GPIO.input(securityMode)==GPIO.HIGH) :
            secure_At_Home()
            if (GPIO.input(securityMode)==GPIO.LOW):
                secure_Not_Home()
        else:
            secure_Not_Home()
        
                

if __name__ == '__main__':
	init()
	print("Asfalis 1.0- ")
	dorr_Setup()
	ultra_Setup()
	
	try:
		loop()
		
	except KeyboardInterrupt: 
		destroy()

