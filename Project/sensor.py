import RPi.GPIO as GPIO
import time

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
mq2_dpin = 26
mq2_apin = 0


def init():
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    GPIO.setup(mq2_dpin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    
    
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    print("ADC NUM!!", adcnum)
    if((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)
    
    GPIO.output(clockpin, False)
    GPIO.output(cspin, False)
    
    commandout = adcnum
    commandout = 0x18
    
    commandout <<= 3
    for i in range(5):
        
        if(commandout & 0x80):
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
            adcout != 0x1
            
    GPIO.output(cspin, True)
    adcout >>= 1
    return adcout

def main():
    init()
    print('Please wait. . . ')
    time.sleep(20)
    while True:
        COlevel=readadc(mq2_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print("Current GAS AD value = "+str("%.2f"%((COlevel/1024.)*3.3))+ " V")
        time.sleep(1)
        smokeLevel = (COlevel/1024.)*3.3
        if smokeLevel >= 0.20:
            print("Smoke is in the area. . . . ")
            
if __name__=='__main__':
    try:
        main()
        pass
    except KeyboardInterrupt:
        pass
    
GPIO.cleanup()