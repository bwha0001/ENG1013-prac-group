from pymata4 import pymata4
import time

board = pymata4.Pymata4()

pin = 3

board.set_pin_mode_analog_input(pin)
count = 0

while True:
    try:
        print(board.analog_read(pin))
        time.sleep(0.5)
    except KeyboardInterrupt:
        board.shutdown()
        quit()