# Asfalis
This repository contains the code for a home security system that runs on a Raspberry Pi. The system includes multiple security features, including a PIR sensor, a flame sensor, an ultrasonic sensor, a door sensor, and a reset button. The system also has a buzzer and a warning light that will be activated if any of the security features are triggered.

## Requirements
-Raspberry Pi  
-PIR sensor  
-Flame sensor  
-Ultrasonic sensor  
-Door sensor  
-Buzzer  
-Warning light  
-Jumper wires  
-Breadboard  
-Power supply for the Raspberry Pi  
## Pin Configuration
The following is the pin configuration for the Raspberry Pi. Please note that these may vary depending on the type of sensors and components used.  

dorrPin = 18  
warningPin = 17  
trigPin = 23  
echoPin = 24  
lightPin = 13  
flamePin = 21  
pirPin = 12  
resetPin = 19  
securityMode = 20  
buzzerPin = 27  
## State Array
The state array keeps track of the current state of the system. The state array is an array of integers with the following possible values:  

000 = alarm on, not home, light off  
001 = alarm on, not home, light on  
010 = alarm on, at home, light off  
011 = alarm on, at home, light on  
100 = reset alarm, not home, light off  
101 = reset alarm, not home, light on  
110 = reset alarm, at home, light off  
111 = reset alarm, at home, light on  
## Function Descriptions
dorr_Setup() sets up the door sensor.  
ultra_Setup() sets up the ultrasonic sensor.  
pulseIn(pin, level, timeOut) obtains the pulse time of a pin under the specified timeout.  
getSonar() returns the measurement result of the ultrasonic sensor in centimeters.  
en_Dorr() activates the alarm if the door sensor is triggered.  
ultra_Sonic() activates the alarm if the ultrasonic sensor is triggered.  
alarm_On(alarm_Type) activates the alarm and warning light based on the type of alarm that has been triggered.  
alarm_Off() deactivates the alarm and warning light.  
get_time() returns the current time and date.  
## External Libraries
The following external libraries are used in this project:  

RPi.GPIO  
os  
socket  
time  
datetime  
mq2test  
servToESP  
sendEmail  
array  
dataBasPush  
## Conclusion
This is a basic setup for a home security system using a Raspberry Pi. The system can be easily customized by adding or removing security features and adjusting the code accordingly. With a few modifications, the system can be integrated with a web application to provide remote access and control.
