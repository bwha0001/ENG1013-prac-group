#Hardware Test button

from pymata4 import pymata4
import time


def receive_data(data):
    """
    :param data: a list containing pin type, pin number, 
                 data value and time-stamp
    """
    # Print the value out (code goes here to do something with the data)
    time1 = time.time()
    global counter
    counter = 0
    if time1- data[3] <0.2:
        counter += 1
    else:
        data[2]=0
        # print(counter)
    # print(data)


board=pymata4.Pymata4()
#code to set pin mode to analog input and set up the callback 
#TODO digital or analog
#board.set_pin_mode_digital_input(13, callback=receive_data)
board.set_pin_mode_analog_input(5, callback=receive_data, differential=100)

print("ped button read started")

startTime = time.time()
counter = 0

while startTime + 10 >= time.time():
    receive_data(board.analog_read(5))
    pass

print("closing")
board.shutdown()