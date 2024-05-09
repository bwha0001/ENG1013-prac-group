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
                    "speedRecord" :[],
                    "lightRecord":[],
                    "tempRecord":[]}

pollingRate = 2
# This needs to be updated during the meeting once everyone is confirmed with pins
changeableConditions = {
    'arduinoPins' : {
        "mainRed": 13,
        "mainYellow": 12,
        "mainGreen": 11,
        "sideRed": 9,
        "sideYellow": 10,
        "sideGreen": 7,
        "pedestrianRed": 6,
        "pedestrianGreen": 5,
        "pedButton":13,
        "triggerPin":2,
        "echoPin":3,
        "triggerPin2":4,
        "echoPin2":5,
        "echoPinOverHeight":13, # random number until pin map finalised
        "normalOverride":3,
        "temperaturePin":0,
        "ldrPin":1 
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
    
    #Light and temp changes TODO decide what is editable parameters and what is set

    "circutConditions":{
        "tempResistorOhms": 1000,
        "lightResistorOhms": 1000
    },
    "dayNightTrigger": "", #TODO esablish light value
    "nightStageLengths":{
        1:45, #Stage 1 changes to 45 seconds
        2:3, 
        3:3, 
        4:10, #Stage 4 changes to 10 seconds
        5:3,
        6:3},
    "tempTrigger": 35,
    "tempStageExtensions": {
        1:5, #extend stage 1 by 5 seconds
        2:0,
        3:0,
        4:5, #extend stage 5 by 5 seconds
        5:0,
        6:0},
    
    #changeable conditions for maintenance mode
    'pollingRate' : pollingRate,
    "overHeight" : 60,
    "extensionTime" : 3,
    "extensionTrigger":3,
    "plotLength" : 20,
    }

#set arduino pins for main board, lights
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

#set up pin for themister
board.set_pin_mode_analog_input(changeableConditions["arduinoPins"]["temperaturePin"])
#set up pin for LDR
board.set_pin_mode_analog_input(changeableConditions["arduinoPins"]["ldrPin"])

#first reading causing errors, complete and ditch inital reads

board.set_pin_mode_analog_input(changeableConditions['arduinoPins']['normalOverride'])

main.main_menu(board, board2, intersectionData, changeableConditions)

print("program ending from AA")
    # Remember to close the boards when you're done
board.shutdown()
board2.shutdown()