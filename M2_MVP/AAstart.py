import time
import math as mth
from pymata4 import pymata4
import module_scripts as ms
import to_7_segment_display as to_7_seg
import maintenance_mode as m_m
import led_state as led
import polling_loop as pl
import traffic_light_sequence as TLS
import main_menu as main
import normal_operation as n_o
import data_observation_mode as DOM

while True:
    try:
        global intersectionData
        global changeableConditions 
        global pollingRate
        # Board 1
        board = pymata4.Pymata4()        # Do something with board1

        # # Board 2
        # board2 = pymata4.Pymata4()
        # # Do something with board2

       
        #Create a dictonary of records
        intersectionData = {"timeRecord":[], "distToVehicleRecord":[], "pedCountRecord":[]}

        pollingRate = 2
        changeableConditions = {
            'arduinoPins' : {
                "mainRed": 2,
                "mainYellow": 3,
                "mainGreen": 4,
                "sideRed": 5,
                "sideYellow": 6,
                "sideGreen": 7,
                "pedestrianRed": 8,
                "pedestrianGreen": 9,
                "triggerPin":12,
                "echoPin":13
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
            'pedCounterReset' : ""
        }
        
        #Set up arduino
        board = pymata4.Pymata4()

        #set arduino pins
        board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainRed"])
        board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainYellow"])
        board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainGreen"])
        board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideRed"])
        board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideYellow"])
        board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideGreen"])
        board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["pedestrianRed"])
        board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["pedestrianGreen"])
        # Configure pin to sonar
        board.set_pin_mode_sonar(changeableConditions["triggerPin"], changeableConditions["echoPin"], timeout=200000)
        #Configiure ped button pin


        main.main_menu(board, intersectionData, changeableConditions)
        
    except KeyboardInterrupt:
        print("program end")
         # Remember to close the boards when you're done
        board.close()
        # board2.close()
        break