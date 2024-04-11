# This converts the LED's into on/off/flashing and converts the traffic light setting to Arduino commands
# Author: Hayley Dusting
# Date: 10/4/2024
# Version ='2.0'

import time
from pymata4 import pymata4
board = pymata4.Pymata4()

#assign pin numbers for LEDs on Arduino
ledPins = {
    "mainRed": 1,
    "mainYellow": 3,
    "mainGreen": 4,
    "sideRed": 5,
    "sideYellow": 6,
    "sideGreen": 7,
    "pedestrianRed": 8,
    "pedestrianGreen": 9
}

#function for flashing to turn LED on and off every 0.5 seconds (2Hz)
def flashing_led(pin):
    """
    Used to make LED flash
        Parameters:
            pin
        Returns:
            function has no returns
    """
    try:
        while True:
            board.digital_write(pin, 1)
            time.sleep(0.5)
            board.digital_write(pin, 0)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

#function to convert traffic light state into LED state
def light_setting_state(mainState, sideState, pedestrianState):
    """
    Used to set traffic light state to on/off/flashing for each LED on the Arduino
        Parameters:
            main traffic light state ('red','yellow','green','flashing'),
            side traffic light state ('red','yellow','green','flashing'),
            pedestrian light state ('red','green','flashing')
        Returns:
            main LED red, main LED yellow, main LED green, main LED flashing, side LED red, side LED yellow, side LED green, side LED flashing, pedestrian LED red, pedestrian LED green, pedestrian LED flashing
    """
    ledStates = {
        "mainRed": 0,
        "mainYellow": 0,
        "mainGreen": 0,
        "sideRed": 0,
        "sideYellow": 0,
        "sideGreen": 0,
        "pedestrianRed": 0,
        "pedestrianGreen": 0
    }

#main traffic light
    if mainState == "red":
        ledStates["mainRed"] = 1
        board.digital_write(ledPins["mainRed"], 1)
        board.digital_write(ledPins["mainYellow"], 0)
        board.digital_write(ledPins["mainGreen"], 0)
        print("main red on")
        print("main yellow off\nmain green off")
    elif mainState == "yellow":
        ledStates["mainYellow"] = 1
        board.digital_write(ledPins["mainRed"], 0)
        board.digital_write(ledPins["mainYellow"], 1)
        board.digital_write(ledPins["mainGreen"], 0)
        print("main red off \nmain yellow on\nmain green off")
    elif mainState == "green":
        ledStates["mainGreen"] = 1
        board.digital_write(ledPins["mainRed"], 0)
        board.digital_write(ledPins["mainYellow"], 0)
        board.digital_write(ledPins["mainGreen"], 1)
        print("main red off \nmain yellow off\n main green on")
    elif mainState == "flashing":
        ledStates["mainYellow"] = -1
        board.digital_write(ledPins["mainRed"], 0)
        flashing_led(ledPins["mainYellow"])
        board.digital_write(ledPins["mainGreen"], 0)
        print("main red off \nmain yellow flashing\n main green on")
# main state
    if sideState == "red":
        ledStates["sideRed"] = 1
        board.digital_write(ledPins["sideRed"], 1)
        board.digital_write(ledPins["sideYellow"], 0)
        board.digital_write(ledPins["sideGreen"], 0)
        print("side red on \n side yellow off\n side green off")
    elif sideState == "yellow":
        ledStates["sideYellow"] = 1
        board.digital_write(ledPins["sideRed"], 0)
        board.digital_write(ledPins["sideYellow"], 1)
        board.digital_write(ledPins["sideGreen"], 0)
        print("side red off \n side yellow on\n side green off")

    elif sideState == "green":
        ledStates["sideGreen"] = 1
        board.digital_write(ledPins["sideRed"], 0)
        board.digital_write(ledPins["sideYellow"], 0)
        board.digital_write(ledPins["sideGreen"], 1)
        print("side red off \n side yellow off\n side green on")
    elif sideState == "flashing":
        ledStates["sideYellow"] = -1
        board.digital_write(ledPins["sideRed"], 0)
        flashing_led(ledPins["sideYellow"])
        board.digital_write(ledPins["sideGreen"], 0)
        print("side red off \n side yellow flashing\n side green off")
# pedestrian light
    if pedestrianState == "red":
        ledStates["pedestrianRed"] = 1
        board.digital_write(ledPins["pedestrianRed"], 1)
        board.digital_write(ledPins["pedestrianGreen"], 0)
        print("pedestrian light red on \npedestrian green off")
    elif pedestrianState == "green":
        ledStates["pedestrianGreen"] = 1
        board.digital_write(ledPins["pedestrianRed"], 0)
        board.digital_write(ledPins["pedestrianGreen"], 1)
        print("pedestrian light red of \npedestrian green on")
    elif pedestrianState == "flashing":
        board.digital_write(ledPins["pedestrianRed"], 0)
        flashing_led(ledPins["pedestrianGreen"])
        print("pedestrian light green off  \npedestrian green flashing")

    return ledStates

if __name__ == 'main':
    light_setting_state("red", "green", "flashing")
    # do we demo without arduino? cause then we need to comment out all of the elite programming and save it 
    # for mpv3