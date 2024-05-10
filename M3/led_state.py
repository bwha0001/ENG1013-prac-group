# This converts the LED's into on/off/flashing and converts the traffic light setting to Arduino commands
# Author: Hayley Dusting 
# Date: 22/4/2024
# Version = 4.0 Hardware tested, software checks commented out

import time
from pymata4 import pymata4

def light_setting_state(board, changeableConditions, mainState, sideState, pedestrianState):
    """
    Used to set traffic light state to on/off/flashing(if applicable) for each LED on the Arduino
    Note: sideRed and pedestrianRed opperate together
        Args:
            board: Arduino Set Up
            board2: 2nd Arduino Set Up
            changeableConditions (dictonary): Anything related to the system that changes
            main traffic light state ('red','yellow','green','off'): state/colour of light set
            side traffic light state ('red','yellow','green','off'): state/colour of light set
            pedestrian light state ('red','green','flashing','off'): state/colour of light set
        Returns:
    """
    #test line
    print("test line entered led_setting_state")

    
    #Extract from the globals
    #input order to shift r
    ledPins = changeableConditions['circutConditions']["ledShiftOrder"]
    
    ser = changeableConditions["arduinoPins"]["ledSer"]
    rclk = changeableConditions["arduinoPins"]["ledRclk"]
    srclk = changeableConditions["arduinoPins"]["ledSrclk"]

    #Create list for shift inputs
    toLedShift =[0,0,0,0,0,0,0,0]

    #Check for invalid input, if side state is red pedestrian state must also be red
    if sideState == "red":
        if pedestrianState == "red":
            pass
        elif pedestrianState != "red":
            #print error message of invlalid combination and do not continue with light setting
            print("!!!!!!!!!!\nError invlaid lights combination; side and pedestrian lights must both be set to red at the same time")
            return


###### TODO Decide how flashing should be handled for maintence mode ie through this function or not?

#main traffic light
    if mainState == "red":
        toLedShift[ledPins["mainRed"]] = 1
        toLedShift[ledPins["mainYellow"]] = 0
        toLedShift[ledPins["mainGreen"]] = 0
        # print("main red on")
        # print("main yellow off\nmain green off")
    elif mainState == "yellow":
        toLedShift[ledPins["mainRed"]] = 0
        toLedShift[ledPins["mainYellow"]] = 1
        toLedShift[ledPins["mainGreen"]] = 0
        # print("main red off \nmain yellow on\nmain green off")
    elif mainState == "green":
        toLedShift[ledPins["mainRed"]] = 0
        toLedShift[ledPins["mainYellow"]] = 0
        toLedShift[ledPins["mainGreen"]] = 1
        # print("main red off \nmain yellow off\n main green on")
        pass
    elif mainState == "off":
        toLedShift[ledPins["mainRed"]] = 0
        toLedShift[ledPins["mainYellow"]] = 0
        toLedShift[ledPins["mainGreen"]] = 0
        # print("main red off \nmain yellow off\n main green off")
# side state
    if sideState == "red":
        toLedShift[ledPins["side/PedRed"]] = 1
        toLedShift[ledPins["sideYellow"]] = 0
        toLedShift[ledPins["sideGreen"]] = 0
        # print("side red on \n side yellow off\n side green off")
    elif sideState == "yellow":
        toLedShift[ledPins["side/PedRed"]] = 0
        toLedShift[ledPins["sideYellow"]] = 1
        toLedShift[ledPins["sideGreen"]] = 0
        # print("side red off \n side yellow on\n side green off")
    elif sideState == "green":
        toLedShift[ledPins["side/PedRed"]] = 0
        toLedShift[ledPins["sideYellow"]] = 0
        toLedShift[ledPins["sideGreen"]] = 1
        # print("side red off \n side yellow off\n side green on")
    elif sideState == "off":
        toLedShift[ledPins["side/PedRed"]] = 0
        toLedShift[ledPins["sideYellow"]] = 0
        toLedShift[ledPins["sideGreen"]] = 0
        # print("side red off \nside yellow off\n side green off")
# pedestrian light
    if pedestrianState == "red":
        toLedShift[ledPins["side/PedRed"]] = 1
        toLedShift[ledPins["pedestrianFlashing"]] = 0
        toLedShift[ledPins["pedestrianGreen"]] = 0
        # print("pedestrian light red on \npedestrian green off")
    elif pedestrianState == "green":
        toLedShift[ledPins["side/PedRed"]] = 0
        toLedShift[ledPins["pedestrianFlashing"]] = 0
        toLedShift[ledPins["pedestrianGreen"]] = 1
        # print("pedestrian light red of \npedestrian green on")
    elif pedestrianState == "flashing":
        toLedShift[ledPins["side/PedRed"]] = 0
        toLedShift[ledPins["pedestrianFlashing"]] = 1
        toLedShift[ledPins["pedestrianGreen"]] = 0
        #print("pedestrian light green off  \npedestrian green flashing")
    elif pedestrianState == "off":
        toLedShift[ledPins["side/PedRed"]] = 0
        toLedShift[ledPins["pedestrianFlashing"]] = 0
        toLedShift[ledPins["pedestrianGreen"]] = 0
        # print("pedestrian red off \n pedestrian green off")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

    #Send to shift register
    for i in range(0,len(toLedShift)):
        #Send to the shift(input) register
        board.digital_pin_write(srclk,0)
        board.digital_pin_write(ser, toLedShift[i])
        time.sleep(0.001)
        board.digital_pin_write(srclk,1)

    #send to the storage(output) register
    board.digital_pin_write(rclk, 1)
    time.sleep(0.001)
    board.digital_pin_write(rclk, 0)