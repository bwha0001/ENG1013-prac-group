from pymata4 import pymata4

board = pymata4.Pymata4

board.set_pin_mode_digital_output(6)

board.digital_write(6,1)


