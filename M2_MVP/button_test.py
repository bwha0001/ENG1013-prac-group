#Hardware Test button

from pymata4 import pymata4

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
counter = 0
board.set_pin_mode_analog_input(10, callback=receive_data)