# This converts the LED's into on/off/flashing and converts the traffic light setting to Arduino commands
# Author: Hayley Dusting 
# Date: 10/4/2024
# Version ='3.0' Hardware testing, software checks still included

#function for flashing to turn LED on and off every 0.5 seconds (2Hz)
def flashing_led(pin):
    """
    Used to make LED flash
        Parameters:
            pin
        Returns:
            function has no returns
    """ 
    board.digital_write(pin,1)
    time.sleep(0.5)
    board.digital_write(pin,0)
    time.sleep(0.5)

#TODO change flashing opperation, this gets stuck in infinate loop - change to do with hardware 555 timer?


"""    try:
        while True:
            board.digital_write(pin, 1)
            time.sleep(0.5)
            board.digital_write(pin, 0)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
"""

#function to convert traffic light state into LED state
def light_setting_state(board, changeableConditions, mainState, sideState, pedestrianState):
    #readded modes to function call based on the function header
    """
    Used to set traffic light state to on/off/flashing for each LED on the Arduino
        Parameters:
            main traffic light state ('red','yellow','green','flashing','off'),
            side traffic light state ('red','yellow','green','flashing','off'),
            pedestrian light state ('red','green','flashing', ,'off')
        Returns:
            main LED red, main LED yellow, main LED green, main LED flashing, side LED red, side LED yellow, side LED green, side LED flashing, pedestrian LED red, pedestrian LED green, pedestrian LED flashing
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

#TODO what is the purpose of this? Nothing?
    # ledStates = {
    #     "mainRed": 0,
    #     "mainYellow": 0,
    #     "mainGreen": 0,
    #     "sideRed": 0,
    #     "sideYellow": 0,
    #     "sideGreen": 0,
    #     "pedestrianRed": 0,
    #     "pedestrianGreen": 0
    # }
    ledStates = changeableConditions['arduinoPins']

#main traffic light
    if mainState == "red":
        ledStates["mainRed"] = 1
        board.digital_write(ledPins["mainRed"], 1)
        board.pwm_write(ledPins["mainYellow"], 0)
        board.digital_write(ledPins["mainGreen"], 0)
        print("main red on")
        print("main yellow off\nmain green off")
    elif mainState == "yellow":
        ledStates["mainYellow"] = 1
        board.digital_write(ledPins["mainRed"], 0)
        board.pwm_write(ledPins["mainYellow"], 255)
        board.digital_write(ledPins["mainGreen"], 0)
        print("main red off \nmain yellow on\nmain green off")
    elif mainState == "green":
        ledStates["mainGreen"] = 1
        board.digital_write(ledPins["mainRed"], 0)
        board.pwm_write(ledPins["mainYellow"], 0)
        board.digital_write(ledPins["mainGreen"], 1)
        print("main red off \nmain yellow off\n main green on")
    elif mainState == "flashing":
        ledStates["mainYellow"] = -1
        board.digital_write(ledPins["mainRed"], 0)
        #board.pwm_write(ledPins["mainYellow"], 30)
        flashing_led(ledPins["mainYellow"])
        board.digital_write(ledPins["mainGreen"], 0)
        print("main red off \nmain yellow flashing\n main green off")
    elif mainState == "off":
        ledStates["mainRed"] = 0
        ledStates["mainYellow"] = 0
        ledStates["mainGreen"] = 0
        board.digital_write(ledPins["mainRed"], 0)
        board.pwm_write(ledPins["mainYellow"], 0)
        board.digital_write(ledPins["mainGreen"], 0)
        print("main red off \nmain yellow off\n main green off")
# side state
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
    elif sideState == "off":
        ledStates["sideRed"] = 0
        ledStates["sideYellow"] = 0
        ledStates["sideGreen"] = 0
        board.digital_write(ledPins["sideRed"], 0)
        board.digital_write(ledPins["sideYellow"], 0)
        board.digital_write(ledPins["sideGreen"], 0)
        print("side red off \nside yellow off\n side green off")
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
    elif pedestrianState == "off":
        ledStates["pedestrianRed"] = 0
        ledStates["pedestrianYellow"] = 0
        ledStates["pedestrianGreen"] = 0
        board.digital_write(ledPins["pedestrianRed"], 0)
        board.digital_write(ledPins["pedestrianGreen"], 0)
        print("pedestrian red off \n pedestrian green off")
    return ledStates                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

# if __name__ == '__main__':

#     import time
#     from pymata4 import pymata4
#     board = pymata4.Pymata4()

#     changeableConditions = {
#         'arduinoPins' : {
#             "mainRed": 2,
#             "mainYellow": 3,
#             "mainGreen": 4,
#             "sideRed": 5,
#             "sideYellow": 6,
#             "sideGreen": 7,
#             "pedestrianRed": 8,
#             "pedestrianGreen": 9,
#             "trigger":0
#             },
#         'ardinoPins7Seg': {},
#         'trafficStage' : 1, # in the led state we need a case switching so we can assign the correct R,Y,G states from traffic stage, not neccercarily, was originally designed to have individual states entered within function call
#         'pollingRate' : 2,
#         'pedCounterReset' : ""
#         }
    
#     #set arduino pins
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainRed"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainYellow"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainGreen"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideRed"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideYellow"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideGreen"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["pedestrianRed"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["pedestrianGreen"])

#     light_setting_state(board, changeableConditions, "yellow", "green", "green")
#     time.sleep(3)
#     light_setting_state(board, changeableConditions, "red", "green", "red")
#     time.sleep(3)
#     light_setting_state(board, changeableConditions, "green", "yellow", "off")
#     time.sleep(3)
#     light_setting_state(board, changeableConditions, "off", "green", "green")
#     time.sleep(3)
#     light_setting_state(board, changeableConditions, "flashing", "green", "red")
#     light_setting_state(board, changeableConditions, "flashing", "green", "red")
#     light_setting_state(board, changeableConditions, "flashing", "green", "red")
#     light_setting_state(board, changeableConditions, "off", "green", "green")

#     board.shutdown()