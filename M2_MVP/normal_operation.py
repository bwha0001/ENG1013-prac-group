#TODO File header
import time
import math as mth
#from pymata4 import pymata4
import to_7_segment_display as to_7_seg
import maintenance_mode as m_m
import led_state as led
import polling_loop as pl
import traffic_light_sequence as TLS
import main_menu as main
import normal_operation as n_o
import data_observation_mode as DOM
import global_variables as GLOB




    # print(f"Test line button data: {changeableConditions['pedsPresent']}, {changeableConditions['lastButtonPress']}")

def traffic_stage_change(intersectionData, changeableConditions, trafficStage):
    """
    This function takes care of the repeated processes of a change in traffic stage in the traffic control system and 
    the tasks that occur at particular stages. Displaying stage specific outputs to console.
    parameters:  current traffic stage
    outputs: current traffic stage
    """

    if trafficStage == "suspended" or trafficStage == 6:
        #initalise stage 1
        #reset ped counter on next poll
        changeableConditions["pedCountReset"] = "stage1Reset"
        #update traffic stage
        trafficStage = 1
        #set stage end time to be x number of seconds from now determined by set value in changeable conditions
            #go to key of the current traffic stage in the lengths dictonary which is within changeable conditons
        stageEndTime = time.time() + changeableConditions["stageLengths"][trafficStage]
        #increase stage by one
        #update traffic stage
        trafficStage += 1   
    else:
        print("How did you get here?")
    
    #update changeable conditons with new traffic stage
    changeableConditions["trafficStage"]=trafficStage
    #set stage end time to be x number of seconds from now determined by set value in changeable conditions
    #go to key of the current traffic stage in the lengths dictonary which is within changeable conditons
    stageEndTime = time.time() + changeableConditions["stageLengths"][changeableConditions["trafficStage"]]
    #Display traffic stage commencing on console
    print(f"Commencing Traffic Stage {trafficStage}")
    #display pedestrian count if entered stage 3
    if changeableConditions["trafficStage"] == 3:
        #print message and last value in the list stored in intersection data
        pedCount = intersectionData["pedCountRecord"][-1]
        print(f"Pedestrian Count: {[pedCount]}")
    return intersectionData,changeableConditions, trafficStage, stageEndTime










def normal_operation(board, board2, intersectionData,changeableConditions):
    """_summary_

    Args:
        board (_type_): _description_
        board2 (_type_): _description_
        intersectionData (_type_): _description_
        changeableConditions (_type_): _description_

    Returns:
        _type_: _description_
    """
    # calling from the global library global_variables and assining it the initial values to be overwritted
    #define dictonary of traffic light colours to stage
    lightForStage = {
        1: ["green", "red", "red"],
        2: ["yellow", "red", "red"],
        3: ["red", "red", "red"],
        4: ["red", "green", "green"],
        5: ["red", "yellow", "flashing"],
        6: ["red", "red", "red"]
        } 

    # Begin normal operation
    mode = 'n'
    to_7_seg.sevenSeg(board2, mode)
    #initialise the pedestrian button
    # board.set_pin_mode_digital_input(changeableConditions['arduinoPins']['pedButton'], callback = ped_button)
    # pedButton = changeableConditions['arduinoPins']['pedButton']
    # # Call the function with the_callback as the callback

    #pull traffic stage from dictonary
    trafficStage = changeableConditions['trafficStage']

    #use changeable conditions to start operation from suspended stage, restarts at stage 1
    if trafficStage == "suspended":
        intersectionData, changeableConditions, trafficStage, stageTimeEnd = traffic_stage_change(intersectionData, changeableConditions, trafficStage)
        #set light colours
        [mainState, sideState, pedestrianState] = lightForStage[changeableConditions["trafficStage"]]
        #output lights to arduino
        led.light_setting_state(board, changeableConditions, mainState, sideState, pedestrianState)
    
    try:
        while True:           
            # Does the traffic stage need changing?
            if time.time()>=stageTimeEnd:
                intersectionData,changeableConditions, trafficStage, stageTimeEnd = traffic_stage_change(intersectionData, changeableConditions, trafficStage)
                #set light colours
                [mainState, sideState, pedestrianState] = lightForStage[changeableConditions["trafficStage"]] 
                #output lights to arduino
                led.light_setting_state(board, changeableConditions, mainState, sideState, pedestrianState)
                # Run function polling loop, inputting polling rate, output of polling time, current distance and pedestrian count
            [intersectionData, changeableConditions] = pl.polling_loop(board, board2, intersectionData, changeableConditions)
            #Happens within function 
                #If polling start time plus polling time taken equals the current time
                # Display polling time on console, “Polling loop took <polling time> to complete”
                # If polling start time plus polling time taken equals the current time
                # Display the current distance, “The distance to the closest vehicle is <current distance> cm.”
            
            #Due to need to continue flashing while polling loop still runs
            #trigger light setting again (ped green flashing) if in stage 5
            if trafficStage == 5:
                led.light_setting_state(board, changeableConditions, mainState, sideState, pedestrianState)
    except KeyboardInterrupt:
        #exit button activation
        print("Exit button activated, returning to main menu")

    return intersectionData, changeableConditions
        
    
    
    

# #Create a dictonary of records
# if __name__ == "__main__":     
#     from pymata4 import pymata4
    
#     #   Create a dictonary of records
#     intersectionData = {"timeRecord":[], "distToVehicleRecord":[], "pedCountRecord":[]}

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
#             "triggerPin":0,
#             "echoPin":1
#             },
#         'ardinoPins7seg': [],
#         'stageLengths':{
#             1:30,
#             2:3,
#             3:3,
#             4:3,
#             5:3,
#             6:3
#         },
#         'trafficStage' : 'suspended',
#         'pollingRate' : 2,
#         'pedCounterReset' : ""
#     }

#     board =pymata4.Pymata4()

#     #set arduino pins
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainRed"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainYellow"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainGreen"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideRed"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideYellow"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideGreen"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["pedestrianRed"])
#     board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["pedestrianGreen"])
#     # Configure pin to sonar
#     board.set_pin_mode_sonar(changeableConditions["arduinoPins"]["triggerPin"], changeableConditions["arduinoPins"]["echoPin"], timeout=200000)
#     #Start ped button checker
#     pedsPresent = 0
#     lastButtonPress = time.time()-0.1
#     board.set_pin_mode_digital_input(changeableConditions['pedsPresent'], callback=ped_button(changeableConditions[pedsPresent]))
    
#     normal_operation(board, intersectionData, changeableConditions)