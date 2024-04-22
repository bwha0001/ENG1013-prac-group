#Hardware Test button

from pymata4 import pymata4
import time

def receive_data(data):
    """
    :param data: a list containing pin type, pin number, 
                 data value and time-stamp
    """
    # Print the value out (code goes here to do something with the data)
    global counter
    counter += 1
    print(counter)
    print(data)


board=pymata4.Pymata4()
#code to set pin mode to analog input and set up the callback 
board.set_pin_mode_digital_input(13, callback=receive_data)
#board.set_pin_mode_analog_input(5, callback=receive_data)

startTime = time.time()
counter = 0

while startTime + 10 >= time.time():
    pass
