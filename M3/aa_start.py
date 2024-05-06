#Traffic Management Start Up File
#Authors: Team F12
#Version: 5 - Hardware Implementation
#Last Edit: 25 April 2024


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

'''
#two arduino operation
# Board 1
board = pymata4.Pymata4(com_port="COM8")     
# # Board 2
board2 = pymata4.Pymata4(com_port="COM7")
'''



#single arduino
board = pymata4.Pymata4()
board2 = ""


#Create a dictonary of records
intersectionData = {"timeRecord":[], "distToVehicleRecord1":[], #regular distance sensor
                    'overheightRecord' : [], # overhight sensor 
                    "pedCountRecord":[], 
                    "pedPresentRecord":[], 
                    "speedRecord" :[]}

pollingRate = 2
# This needs to be updated during the meeting once everyone is confirmed with pins
changeableConditions = {
    'arduinoPins' : {
        "mainRed": 6,
        "mainYellow": 7,
        "mainGreen": 8,
        "sideRed": 9,
        "sideYellow": 10,
        "sideGreen": 11,
        "pedestrianRed": 12,
        "pedestrianGreen": 13,
        "pedButton":13,
        "triggerPin":2,
        "echoPin":3,
        "triggerPin2":4,
        "echoPin2":5,
        "echoPinOverHeight":13, # random number until pin map finalised
        "normalOverride":3
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
    'pedCounterReset' : "",
    'lockOutTime': 0,    # for maintenance mode lock out
    "lockOutLength": 120, #Locked out for 2 mins
    "accessTime": 60, #testing at 1 min #180 #time able to access maintence mode 3 mins(access time in seconds)
    
    #changeable conditions for maintenance mode
    'pollingRate' : pollingRate,
    "overHeight" : 60,
    "extensionTime" : 3,
    "extensionTrigger":3,
    "plotLength" : 20

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
# Configure trigger and echo to sonar

#######
# potentially need to put set pin mode sonar in polling to initialise before being called
#######
board.set_pin_mode_sonar(changeableConditions["arduinoPins"]["triggerPin"], changeableConditions["arduinoPins"]["echoPin"])
board.set_pin_mode_sonar(changeableConditions["arduinoPins"]["triggerPin2"], changeableConditions["arduinoPins"]["echoPin2"])

#first reading causing errors,

board.set_pin_mode_analog_input(changeableConditions['arduinoPins']['normalOverride'])

main.main_menu(board, board2, intersectionData, changeableConditions)

print("program ending from AA")
    # Remember to close the boards when you're done
board.shutdown()
board2.shutdown()