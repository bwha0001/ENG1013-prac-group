import time
import math as mth
from pymata4 import pymata4
import to_7_segment_display as to_7_seg
import maintenance_mode as m_m
import led_state as led
import polling_loop as pl
# new normal opperation makes this obsolete
#import traffic_light_sequence as TLS
import main_menu as main
import normal_operation as n_o
import data_observation_mode as DOM
import global_variables as GLOB

# initialise global variables for the rest of the script
GLOB.init()
# Board 1
board = pymata4.Pymata4()        # Do something with board1

# # Board 2
#board2 = pymata4.Pymata4()
#Single Arduino Test
board2 = ""
# # Do something with board2


#Create a dictonary of records
intersectionData = {"timeRecord":[], "distToVehicleRecord":[], "pedCountRecord":[], "pedPresentRecord":[]}

pollingRate = 2
changeableConditions = {
    'arduinoPins' : {
        "mainRed": 2+3,
        "mainYellow": 3+3,
        "mainGreen": 4+3,
        "sideRed": 5+3,
        "sideYellow": 6+3,
        "sideGreen": 7+3,
        "pedestrianRed": 8+3,
        "pedestrianGreen": 9+3,
        "pedButton":2,
        "triggerPin":3,
        "echoPin":4
        },
    'ardinoPins7seg': [],
    'stageLengths':{
        1:30,
        2:3,
        3:3,
        4:3,
        5:3,
        6:3
    },
    'trafficStage' :"suspended",
    'pollingRate' : pollingRate,
    'pedCounterReset' : "",
    'pedsPresent' : 0, #PEDCOUNTER IS NOW IN THE DICTIONARY, WILL BE PASSED THROUGH THE ENTIRE THING
    'lastButtonPress' : 0 #updated in line 91
}

#set arduino pins for main board
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainRed"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainYellow"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainGreen"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideRed"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideYellow"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideGreen"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["pedestrianRed"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["pedestrianGreen"])
# Configure pin to sonar
board.set_pin_mode_sonar(changeableConditions["arduinoPins"]["triggerPin"], changeableConditions["arduinoPins"]["echoPin"], timeout=200000)
#Configiure ped button pin
changeableConditions['lastButtonPress'] = time.time() - 0.1
# board.set_pin_mode_digital_input(changeableConditions["arduinoPins"]["pedButton"], callback=ped_button(changeableConditions))
# board.set_pin_mode_digital_input(changeableConditions["arduinoPins"]["pedButton"])
main.main_menu(board, board2, intersectionData, changeableConditions)

print("program ending from AA")
    # Remember to close the boards when you're done
board.shutdown()
board2.shutdown()