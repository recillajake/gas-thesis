import RPi.GPIO as GPIO
import time
from LCD1 import LCD

lcd = LCD(2, 0x27, True)

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
mq2_dpin = 26
mq2_apin = 0

buzzer_pin = 21

# Calibration constants for LPG gas
# Adjust these values based on your calibration
LPG_Ro = 10  # Ro value of the sensor
Normal_Concentration = 0.2  # Normal LPG concentration in %

def init():
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    GPIO.setup(mq2_dpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    
    
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)
    
    GPIO.output(clockpin, False)
    GPIO.output(cspin, False)
    
    commandout = adcnum
    commandout |= 0x18
    
    commandout <<= 3
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        
    adcout = 0
    
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1
            
    GPIO.output(cspin, True)
    adcout >>= 1
    return adcout

def main():
    init()
    c = 0
    print('Please wait. . . ')
    lcd.message("CALIBRATING", 1)
    for i in range(20):
        lcd.message("MQ-2 SENSOR {:.0f}%".format(c), 2)
        c+=5
        time.sleep(1)
    while True:
        COlevel = readadc(mq2_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)
        # Convert analog value to LPG gas concentration percentage
        LPG_percentage = (COlevel / LPG_Ro) * Normal_Concentration
        if LPG_percentage <= 1.8:  # Adjust threshold as needed
            lcd.clear()
            GPIO.output(buzzer_pin, GPIO.LOW)
            print("Current LPG gas concentration = {:.2f}%".format(LPG_percentage))
            lcd.message("Normal-GAS-Consen %: ", 1)
            lcd.message("= {:.2f}%".format(LPG_percentage), 2)
            
        elif LPG_percentage > 1.8:
            lcd.clear()
            GPIO.output(buzzer_pin, GPIO.HIGH)
            lcd.message("High GAS Consen", 1)
            lcd.message("= {:.2f}%".format(LPG_percentage), 2)
            print("High LPG gas concentration detected!")
        else:
            lcd.clear()
            lcd.clear()
            GPIO.output(buzzer_pin, GPIO.LOW)
            
        
            
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        lcd.clear()
        pass
GPIO.cleanup()
    

