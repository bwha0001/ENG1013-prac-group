# This converts the LED's into on/off/flashing and converts the traffic light setting to Arduino commands
# Author: Hayley Dusting 
# Date: 22/4/2024
# Version = 4.0 Hardware tested, software checks commented out

import time
from pymata4 import pymata4

#function for flashing to turn LED on and off every 0.5 seconds (2Hz)
def flashing_led(board,pin):
    """
    Used to make LED flash at 2Htz for 1 second
    
    Args:
        board: Arduino Set Up
        pin (interger): Arduino Pin which LED is connected to
    """    
    
    board.digital_write(pin,1)
    time.sleep(0.3)
    board.digital_write(pin,0)
    time.sleep(0.3)


#function to convert traffic light state into LED state
def light_setting_state(board, changeableConditions, mainState, sideState, pedestrianState):
    #readded modes to function call based on the function header
    """
    Used to set traffic light state to on/off/flashing for each LED on the Arduino
        Args:
            board: Arduino Set Up
            board2: 2nd Arduino Set Up
            changeableConditions (dictonary): Anything related to the system that changes
            main traffic light state ('red','yellow','green','flashing','off'): state/colour of light set
            side traffic light state ('red','yellow','green','flashing','off'): state/colour of light set
            pedestrian light state ('red','green','flashing', ,'off'): state/colour of light set
        Returns:
            None
    """
    # importing the globals

    #dictonary of pin assignment for ardino
    ledPins = changeableConditions["arduinoPins"]

    print("test line entered led_setting_state")
    '''
    mainState = changableConditions['trafficStage']
    if mainState == 1:
        mainState = 'red' #currently should start as red
    else:
        mainState = 'green'
    sideState = 'red'
    pedestrianState = 'red'
    pedCountRecord = changableConditions['pedCountRecord']
    '''

    ledPins = changeableConditions['arduinoPins']

#main traffic light
    if mainState == "red":
        board.digital_write(ledPins["mainRed"], 1)
        board.digital_write(ledPins["mainYellow"], 0)
        board.digital_write(ledPins["mainGreen"], 0)
        # print("main red on")
        # print("main yellow off\nmain green off")
    elif mainState == "yellow":
        board.digital_write(ledPins["mainRed"], 0)
        board.digital_write(ledPins["mainYellow"], 1)
        board.digital_write(ledPins["mainGreen"], 0)
        # print("main red off \nmain yellow on\nmain green off")
    elif mainState == "green":
        board.digital_write(ledPins["mainRed"], 0)
        board.digital_write(ledPins["mainYellow"], 0)
        board.digital_write(ledPins["mainGreen"], 1)
        # print("main red off \nmain yellow off\n main green on")
    elif mainState == "flashing":
        board.digital_write(ledPins["mainRed"], 0)
        #board.pwm_write(ledPins["mainYellow"], 30)
        flashing_led(board,ledPins["mainYellow"])
        board.digital_write(ledPins["mainGreen"], 0)
        # print("main red off \nmain yellow flashing\n main green off")
    elif mainState == "off":
        board.digital_write(ledPins["mainRed"], 0)
        board.digital_write(ledPins["mainYellow"], 0)
        board.digital_write(ledPins["mainGreen"], 0)
        # print("main red off \nmain yellow off\n main green off")
# side state
    if sideState == "red":
        board.digital_write(ledPins["sideRed"], 1)
        board.digital_write(ledPins["sideYellow"], 0)
        board.digital_write(ledPins["sideGreen"], 0)
        # print("side red on \n side yellow off\n side green off")
    elif sideState == "yellow":
        board.digital_write(ledPins["sideRed"], 0)
        board.digital_write(ledPins["sideYellow"], 1)
        board.digital_write(ledPins["sideGreen"], 0)
        # print("side red off \n side yellow on\n side green off")
    elif sideState == "green":
        board.digital_write(ledPins["sideRed"], 0)
        board.digital_write(ledPins["sideYellow"], 0)
        board.digital_write(ledPins["sideGreen"], 1)
        # print("side red off \n side yellow off\n side green on")
    elif sideState == "flashing":
        board.digital_write(ledPins["sideRed"], 0)
        flashing_led(board,ledPins["sideYellow"])
        board.digital_write(ledPins["sideGreen"], 0)
        # print("side red off \n side yellow flashing\n side green off")
    elif sideState == "off":
        board.digital_write(ledPins["sideRed"], 0)
        board.digital_write(ledPins["sideYellow"], 0)
        board.digital_write(ledPins["sideGreen"], 0)
        # print("side red off \nside yellow off\n side green off")
# pedestrian light
    if pedestrianState == "red":
        board.digital_write(ledPins["pedestrianRed"], 1)
        board.digital_write(ledPins["pedestrianGreen"], 0)
        # print("pedestrian light red on \npedestrian green off")
    elif pedestrianState == "green":
        board.digital_write(ledPins["pedestrianRed"], 0)
        board.digital_write(ledPins["pedestrianGreen"], 1)
        # print("pedestrian light red of \npedestrian green on")
    elif pedestrianState == "flashing":
        board.digital_write(ledPins["pedestrianRed"], 0)
        flashing_led(board,ledPins["pedestrianGreen"])
        #print("pedestrian light green off  \npedestrian green flashing")
    elif pedestrianState == "off":
        board.digital_write(ledPins["pedestrianRed"], 0)
        board.digital_write(ledPins["pedestrianGreen"], 0)
        # print("pedestrian red off \n pedestrian green off")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
