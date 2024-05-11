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
intersectionData = {"timeRecord":[], 
                    "distToVehicleRecord":[], #regular distance sensor
                    'overheightRecord' : [], # overhight sensor 
                    "pedCountRecord":[], #count of pedestrian per traffic cycle
                    "pedPresentRecord":[], #count of how many times the button has been pressed
                    "speedRecord" :[],
                    "lightRecord":[], # records if day or night at time of polling
                    "tempRecord":[]}

pollingRate = 2
# This needs to be updated during the meeting once everyone is confirmed with pins
changeableConditions = {
    'arduinoPins' : {
        #7 Segment Display
        
        #Traffic Lights Shift
        "ledSer":5,
        "ledRclk":6,
        "ledSrclk":7,
        "maintenceFlashing":8, #pin to trigger non-normal opperation mode flashing
        "buzzerFlashingOverHead": 9, #activates overhight vechile alerts
        #UltraSonic1
        "triggerPin":10,
        "echoPin":11,
        #UltraSonic2
        "triggerPin2":12,
        "echoPin2":13,
        #Analog pins
        "temperaturePin":0,
        "ldrPin":1,
        "pedButton":2,
        "normalOverride":3,

        "echoPinOverHeight":13, #TODO is this pin required or already covered? random number until pin map finalised

        },
    'ardinoPins7seg': [],

    'trafficStage' :"suspended",
    'pedCounterReset' : "",
    "stage2extended": 0,
    'lockOutTime': 0,    # for maintenance mode lock out, time locked out until
    "lockOutLength": 120, #Locked out for 2 mins
    "accessTime": 60, #testing at 1 min #180 #time able to access maintence mode 3 mins(access time in seconds)
    
    #Light and temp changes TODO decide what is editable parameters and what is set

    "circutConditions":{
        "tempResistorOhms": 1000,
        "lightResistorOhms": 1000,
        "ledShiftOrder":{
            "mainRed": 0, #QH
            "mainYellow": 1, #QG
            "mainGreen": 2, #QF
            "side/PedRed": 3, #QE
            "sideYellow": 4, #QD
            "sideGreen": 5, #QC
            "pedestrianGreen": 6, #QB
            "pedestrianFlashing": 7 #QA
            }
        },
    
    'stageLengths':{
        1:30,
        2:3,
        3:3,
        4:3,
        5:3,
        6:3
    },
    "dayNightTrigger": 2.72, #Voltage
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

'''
#set arduino pins for main board, lights
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainRed"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainYellow"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainGreen"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideRed"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideYellow"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideGreen"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["pedestrianRed"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["pedestrianGreen"])
''' 

#Traffic lights output set up
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["ledSer"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["ledRclk"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["ledSrclk"])

#Overheight altert set up
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["buzzerFlashingOverHead"])



# Configure trigger and echo to sonar

#######
# potentially need to put set pin mode sonar in polling to initialise before being called
#######
board.set_pin_mode_sonar(changeableConditions["arduinoPins"]["triggerPin"], changeableConditions["arduinoPins"]["echoPin"])
board.set_pin_mode_sonar(changeableConditions["arduinoPins"]["triggerPin2"], changeableConditions["arduinoPins"]["echoPin2"])
board.sonar_read(changeableConditions["arduinoPins"]["triggerPin"]) 
board.sonar_read(changeableConditions["arduinoPins"]["triggerPin2"]) 

#set up pin for themister
board.set_pin_mode_analog_input(changeableConditions["arduinoPins"]["temperaturePin"])
#set up pin for LDR
board.set_pin_mode_analog_input(changeableConditions["arduinoPins"]["ldrPin"])

#set up pin for normal override switch
board.set_pin_mode_analog_input(changeableConditions['arduinoPins']['normalOverride'])

main.main_menu(board, board2, intersectionData, changeableConditions)

print("program ending from AA")
    #Remember to reset shift register unless you want funky things on intial start when repeatedly ending and starting
#Switch off all lights to reset shift register
led.light_setting_state(board, changeableConditions, "off", "off", "off")    
    #Remember to close the boards when you're done
board.shutdown()