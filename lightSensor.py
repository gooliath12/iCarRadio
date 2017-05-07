#!/usr/bin/python


from upm import pyupm_grove
import mraa
import time
import sys


LIGHT_SENSOR_PIN=0         # Analog input port where the the light sensor is connected
MAX_LIGHT = 50
LED_PWM_PIN=5

def getLight():
    light = pyupm_grove.GroveLight(LIGHT_SENSOR_PIN)
    pwm = mraa.Pwm(LED_PWM_PIN)
    pwm.period_us(5000) # Set the period as 5000 us or 5ms
    pwm.enable(True)    # enable PWM
    pwm.write(0)
    return light.value()
    """
    ambientLight = light.value()
    tempLight = ambientLight
    if tempLight > MAX_LIGHT:
        tempLight = MAX_LIGHT      # Nromalize the value
        
    pwmValue = (MAX_LIGHT - tempLight)/float(MAX_LIGHT)

    pwm.write(pwmValue)
    
    for i in range(0, MAX_LIGHT):
        if ambientLight > i:
            sys.stdout.write("=")
        elif ambientLight == i:
            sys.stdout.write("|")
        else:
            sys.stdout.write(" ")
           
    return ambientLight
    #return pwmValue
    time.sleep(1) 
    """
#print getLight()
