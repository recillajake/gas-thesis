import smbus2
import time

# Define I2C address of the SIM900A module
SIM900A_I2C_ADDRESS = 0x20

# Function to send SMS
def send_sms(text):
    try:
        # Open I2C bus
        bus = smbus2.SMBus(1)
        
        # Send SMS command
        command = "AT+CMGS=\"+639278363104\"\r\n"  # Replace with recipient's phone number
        bus.write_i2c_block_data(SIM900A_I2C_ADDRESS, 0, [ord(c) for c in command])
        time.sleep(0.1)
        
        # Send SMS text
        bus.write_i2c_block_data(SIM900A_I2C_ADDRESS, 0, [ord(c) for c in text])
        time.sleep(0.1)
        
        # Send Ctrl+Z to end SMS
        bus.write_i2c_block_data(SIM900A_I2C_ADDRESS, 0, [0x1A])
        time.sleep(0.1)
        
        print("SMS sent successfully.")

    except Exception as e:
        print("An error occurred:", str(e))

# Send SMS
send_sms("Hello from Raspberry Pi!")
