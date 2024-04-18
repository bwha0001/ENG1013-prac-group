import time
import math as mth
#ST. from pymata4 import pymata4 
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

        #Create a dictonary of records
        intersectionData = {"timeRecord":[], "distToVehicleRecord":[], "pedCountRecord":[], "pedCounterReset":""}

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
                "pedestrianGreen": 9
                },
            'ardinoPins7seg': {},
            'trafficStage' : 1, # in the led state we need a case switching so we can assign the correct R,Y,G states from traffic stage, not neccercarily, was originally designed to have individual states entered within function call
            'pollingRate' : pollingRate,
            'pedCounterReset' : ""
        }
        
        trafficStage = 1   
        
        trafficStage = 1

        main.main_menu(intersectionData, changeableConditions)
        
    except KeyboardInterrupt:
        print("program end")
        break