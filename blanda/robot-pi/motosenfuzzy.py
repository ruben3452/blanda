import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from Tkinter import *
import RPi.GPIO as GPIO
import time


x_distacex = np.arange(0, 200, 1)
x_velocidad = np.arange(0, 100, 1)


distacex_small = fuzz.trimf(x_distacex, [0, 10, 20])
distacex_safe = fuzz.trimf(x_distacex, [30, 50, 60])
distacex_big = fuzz.trimf(x_distacex, [70, 100, 150])

velocidad_stop = fuzz.trimf(x_velocidad, [0, 0, 0])
velocidad_slow = fuzz.trimf(x_velocidad, [30, 40, 50])
velocidad_normal = fuzz.trimf(x_velocidad, [60,70, 80 ])
velocidad_hing = fuzz.trimf(x_velocidad, [90, 100, 110])

#plt.plot(distacex_small,distacex_safe,distacex_big)
#plt.show()
def measure():
 # This function measures a distance
 GPIO.output(GPIO_TRIGGER, True)
 time.sleep(0.00001)
 GPIO.output(GPIO_TRIGGER, False)
 start = time.time()

 while GPIO.input(GPIO_ECHO)==0:
   start = time.time()

 while GPIO.input(GPIO_ECHO)==1:
   stop = time.time()

 elapsed = stop-start
 distance = (elapsed * 34300)/2

 return distance

GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 20
GPIO_ECHO    = 21

#motor

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18,100)

left_in1_pin = 24
left_in2_pin = 23
right_in1_pin = 22
right_in2_pin = 27
class Motor(object):
    def __init__(self, in1_pin, in2_pin):
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
                   
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)
	
    def clockwise(self):
        GPIO.output(self.in1_pin, True)    
        GPIO.output(self.in2_pin, False)
    def counter_clockwise(self):
        GPIO.output(self.in1_pin, False)
        GPIO.output(self.in2_pin, True)
                   
    def stop(self):
        GPIO.output(self.in1_pin, False)    
        GPIO.output(self.in2_pin, False)
        
        

               


print "Ultrasonic Measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
# Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)
# Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)
time.sleep(0.01)
GPIO.output(GPIO_TRIGGER, True)
time.sleep(0.001)
GPIO.output(GPIO_TRIGGER, False)
begin = time.time()
try:
    left_motor = Motor(left_in1_pin, left_in2_pin)
    right_motor = Motor(right_in1_pin, right_in2_pin)
           
    direction = None
           
    while True:

        distance = measure()
	#print "Distance : %.1f" % distance
        time.sleep(0.01)
       
        if (distance > 30) : 
            left_motor.clockwise()
            right_motor.clockwise()
            
            pwm.start(70)
       
            
        elif (distance <= 9 ) :
            left_motor.counter_clockwise()
            right_motor.counter_clockwise()
            pwm.start(100)
            time.sleep(0.9)
        
       
        elif (direction <=  17 and distance >=11 ): # opposite1
            left_motor.counter_clockwise()
            right_motor.clockwise()
            pwm.start(55)
        
        
        else:
            left_motor.stop()
            right_motor.stop()
        
       

except KeyboardInterrupt:
    left_motor.stop()
    right_motor.stop()
    GPIO.cleanup()
