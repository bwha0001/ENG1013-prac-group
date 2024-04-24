#Hardware Test button

from pymata4 import pymata4
import time

def ped_button(data):
    """
    :param data: a list containing pin type, pin number, 
                 data value and time-stamp
    """
    # Print the value out (code goes here to do something with the data)
    global pedCounter

    global lastButtonPress
    
    if data[2] ==1 and time.time()-lastButtonPress>0.1:
        pedCounter += 1
        print(pedCounter)
    
    print(data)
    lastButtonPress = time.time()



board=pymata4.Pymata4()
#code to set pin mode to analog input and set up the callback 
#TODO digital or analog
board.set_pin_mode_digital_input(10, callback=ped_button)
#board.set_pin_mode_analog_input(5, callback=receive_data)

print("ped button read started")

startTime = time.time()
pedCounter = 0
lastButtonPress = time.time() - 0.1

while startTime + 20 >= time.time():
    pass

print("closing")
board.shutdown()