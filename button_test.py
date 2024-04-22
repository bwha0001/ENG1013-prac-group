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
    if data[2] >600:
        counter += 1
        print(counter)
    print(data)


board=pymata4.Pymata4()
#code to set pin mode to analog input and set up the callback 
#TODO digital or analog
#board.set_pin_mode_digital_input(13, callback=receive_data)
board.set_pin_mode_analog_input(5, callback=receive_data, differential=100)

print("ped button read started")

startTime = time.time()
counter = 0

while startTime + 20 >= time.time():
    pass

print("closing")
board.shutdown()