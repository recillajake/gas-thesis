import time
from LCD1 import LCD

lcd = LCD(2, 0x27, True)  

lcd.message("LPG GAS ", 1)
lcd.message("concentration: ", 2)

time.sleep(20)

lcd.clear()