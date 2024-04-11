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

        #Creates a dictonary of records if one doesnt exist
        intersectionData = {"timeRecord":[], "distToVehicleRecord":[], "pedCountRecord":[], "pedCounterReset":""}
        
        global pollingRate
        pollingRate = 2
        changeableConditions = {
            'trafficStage' : 1,
            'pollingRate' : pollingRate,
            'pedCounterReset' : ""
        }
        
        trafficStage = 1   
        

        main.main_menu(intersectionData, changeableConditions)
        print("hi")
    except KeyboardInterrupt:
        break