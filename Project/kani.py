import RPi.GPIO as GPIO
import time
import os


GPIO.setmode(GPIO.BCM)


DO_PIN = 2
buzzer_pin = 21

GPIO.setup(DO_PIN, GPIO.IN)
GPIO.setup(buzzer_pin, GPIO.OUT)

try:
    while True:
        gas_present = GPIO.input(DO_PIN)


        if gas_present == GPIO.LOW:
            gas_state = "Gas Present"
            GPIO.output(buzzer_pin, GPIO.HIGH)
        else:
            gas_state = "No Gas"
            GPIO.output(buzzer_pin, GPIO.LOW)
        os.system('clear')
        print(f"Gas State: {gas_state}")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Gas detection stopped by user")

finally:
    GPIO.cleanup()
