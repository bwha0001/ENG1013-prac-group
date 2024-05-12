from pymata4 import pymata4
import time

board = pymata4.Pymata4()

board.set_pin_mode_digital_output(7)
print("on")
timeNow = time.time()

board.digital_write(7,1)
currentTime = timeNow-time.time()
time.sleep(3)
board.digital_write(7,0)
# board.digital_write(7,0)
print("off")


board.shutdown()