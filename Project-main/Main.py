import RPi.GPIO as GPIO
import os
import socket
import time
from datetime import datetime,date
from mq2test import *
from servToESP import *
from sendEmail import *
import array as arr
from dataBasPush import *

dorrPin = 18
warningPin= 17
trigPin = 23
echoPin = 24
lightPin= 13
MAX_DISTANCE = 220          # define the maximum measuring distance, unit: cm
flamePin= 21
pirPin=12
resetPin=19
securityMode=20
buzzerPin=27
state =arr.array('i',[0,0,0]) # 000 = alarm on, not home, lampa av
                              # 001 = alarm on, not home, lapma på
                              # 010 = alarm on, at home, lampa av
                              # 011 = alarm on, at home, lampa på
                              # 100 = reset larm, not home, lamp av
                              # 101 = reset larm, not home, lampa på
                              # 110 = reset larm, at home,  lampa av
                              # 111 = reset larm, at home, lampa på

timeOut = MAX_DISTANCE*60   # calculate timeout according to the maximum measuring distance

def get_time():
    time=datetime.now().strftime(" %H:%M:%S ")
    dat= date.today().strftime(" %D")
    return time,dat


def dorr_Setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(warningPin,GPIO.OUT)
	GPIO.setup(lightPin,GPIO.OUT)
	GPIO.setup(dorrPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
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
    #time.sleep(1)                           # DEN HÖR GJORDE PHP KNAPPARNA LÅNGSAMMA 
    return distance

def en_Dorr():
    try:  
        if  (GPIO.input(dorrPin)==GPIO.HIGH)  :
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
    #dataPush(alarm_Type)
    #if ( (GPIO.input(securityMode)==GPIO.LOW) or (state[1]==0) ):
        #send_Email()
    state[0]=0
    if (alarm_Type==1) or (alarm_Type==5):
        GPIO.output(warningPin,GPIO.HIGH)
        GPIO.output(buzzerPin,GPIO.HIGH)
        
    else:
        GPIO.output(warningPin,GPIO.HIGH)
    tid=get_time()
    print("type of alarm is : %s at : %s" %(alarm_Type, tid))
    
    
# ideer: ta med type of larm för att deaktivera, kanske lösenord
def alarm_Off():
    if ( (GPIO.input(resetPin)==GPIO.LOW) or (state[0] ==1) ) :
        GPIO.output(warningPin,GPIO.LOW)
        GPIO.output(buzzerPin,GPIO.HIGH)
    else:
        #state[0]=0
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
    
    while True:
        if (GPIO.input(pirPin)==GPIO.HIGH):
            alarm_On(4)
            #start_Client()
                
            time.sleep(0.05)      
        else:
            alarm_Off()
            return 0
def get_Smoke():
    while True:
        COlevel=readadc(mq2_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)
        SmokeTrigger = ((COlevel/1024.)*3.3)

        if SmokeTrigger > 0.5:
            alarm_On(5)
            #print("Gas leakage")
            #print("Current Gas AD vaule = " +str("%.2f"%((COlevel/1024.)*3.3))+" V")
            time.sleep(0.05)

        else:
            time.sleep(0.05)
            return 0
def secure_Not_Home():
    
    for i in range(6):
        if i==0:
            get_Flame()
        elif i==1:
            ultra_Sonic()
        elif i==2:
            en_Dorr()
        elif i==3:
            get_Smoke()
        elif i==4:
            home_lighting()
        else:
            get_Movement()
def secure_At_Home():
    for i in range(3):
        if i==0:
            get_Flame()
        elif i==1:
            home_lighting()
        else:
            get_Smoke()
            
def home_lighting():
    if (state[2]==1):
        GPIO.output(lightPin,GPIO.HIGH)
    else:
        GPIO.output(lightPin,GPIO.LOW)
        
        

            
    
def loop():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM)as s:
        s.bind(('',12345))
        s.setblocking(0)
        while True:
            try:
                
                x=s.recv(1024)
                if ((x==b"Ares")):
                    state[0]=1
                elif (x==b"Aon"):
                    state[0]=0
                    #print("funkar")
                elif (x==b"Noth"):
                    state[1]=0
                elif (x==b"Ath"):
                    state[1]=1
                elif (x==b"Lon"):
                    state[2]=1
                elif (x==b"Loff"):
                    state[2]=0
                    
                #print(x)
            except:
                pass
            
        
            if ((GPIO.input(securityMode)==GPIO.HIGH) or (state[1]==1) ) :
                secure_At_Home()
                
            elif ((GPIO.input(securityMode)==GPIO.LOW) or (state[1]==0) ):
                secure_Not_Home()
            time.sleep(0.1)    
            

if __name__ == '__main__':
	init()
	print("Asfalis 2.0- ")
	dorr_Setup()
	ultra_Setup()
	
	try:
		loop()
		
	except KeyboardInterrupt: 
		destroy()

