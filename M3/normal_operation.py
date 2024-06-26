#Normal Operation Mode for Traffic Control System
#Authors: Caitlin 
#Version: 3 - Reworked for hardware implementation
#Last Edit: 25 April 2024
import time
import math as mth
#from pymata4 import pymata4
import to_7_segment_display as to_7_seg
import maintenance_mode as m_m
import led_state as led
import polling_loop as pl
import main_menu as main
import normal_operation as n_o
import data_observation_mode as DOM
import global_variables as GLOB
import temperature_handling as temp
import ldr_function as ldr

def ped_button_callback(data):
    """
    Callback function for pedestrian button press.
    """
    if data[2] == 1 and time.time() > GLOB.lastButtonPress + 0.0001:
        GLOB.pedsPresent += 1
        GLOB.pedSequence += 1
        GLOB.lastButtonPress = time.time()


    # print(f"Test line button data: {changeableConditions['pedsPresent']}, {changeableConditions['lastButtonPress']}")

def traffic_stage_change(board, intersectionData, changeableConditions, trafficStage):
    """_summary_

    Args:
        intersectionData (dictonary): Data collected about the interesection
        changeableConditions (dictonary): Anything related to the system that changes
        trafficStage (1,2,3,4,5,6,"suspended"): \Traffic Stage of intersection
    Returns:
        intersectionData (dictonary): Data collected about the interesection
        changeableConditions (dictonary): Anything related to the system that changes
        trafficStage(1,2,3,4,5,6): the stage of the traffic sequence that was just entered
        stageEndTime(float): the end time of the current traffic sequence stage
    """    
    
    #Process for changing traffic stage

    if trafficStage == "suspended" or trafficStage == 6:
        #initalise stage 1
        #reset ped counter on next poll
        changeableConditions["pedCountReset"] = "stage1Reset"
        #update traffic stage
        trafficStage = 1
    elif trafficStage in {1,2,3,4,5}:
        #set stage end time to be x number of seconds from now determined by set value in changeable conditions
            #go to key of the current traffic stage in the lengths dictonary which is within changeable conditons
        stageEndTime = time.time() + changeableConditions["stageLengths"][trafficStage]
        #increase stage by one
        #update traffic stage
        trafficStage += 1   
    else:
        print("traffic light operating")
    
    #update changeable conditons with new traffic stage
    changeableConditions["trafficStage"]=trafficStage
    #set stage end time to be x number of seconds from now determined by set value in changeable conditions
    #go to key of the current traffic stage in the lengths dictonary which is within changeable conditons
    stageEndTime = time.time() + changeableConditions["stageLengths"][changeableConditions["trafficStage"]]
    #Display traffic stage commencing on console
    print(f"Commencing Traffic Stage {trafficStage}")

    ######

    #Stage Length edits

    #Extend stage if approprite based on low light or high temp
    stageExtensionTime = 0
    #Take reading from themistor and ldr
    #funtion calls
    currentLight = ldr.ldr(board, changeableConditions)
    currentTemp = temp.temperature(board, changeableConditions)
    print(currentTemp)
    print(currentLight)
    #if current temprature is above the temprature for triggering add to the extension time
    if currentTemp == changeableConditions["tempTrigger"]:
        stageExtensionTime += changeableConditions["tempStageExtensions"][trafficStage]
        #Debugging line, TODO Remove once tested
        print("temp extestion trigger met, time added if required")
    #if current light level is night add to the extension time
    if currentLight == "night":
        #Find the extension time required by the differance in stage lengths
        stageExtensionTime += changeableConditions["nightStageLengths"][trafficStage] - changeableConditions["stageLengths"][trafficStage]
        print("day/night extestion trigger met, time added if required")
        #Debugging line, TODO Remove once tested

    #Add the extension time to stageEndTime
    stageEndTime += stageExtensionTime
    
    ######

    #Stage specific tests, completed based on stage entering

    #Stage 1
    if changeableConditions["trafficStage"] == 1:
        #reset the peds presence per traffic seqence
        GLOB.pedSequence = 0

    #Stage 3

    #display pedestrian count if entered stage 3, reset stage 2 extended variable
    if changeableConditions["trafficStage"] == 3:
        #print message and last value in the list stored in intersection data
        pedCount = intersectionData["pedCountRecord"][-1]
        print(f"Pedestrian Count: {[pedCount]}")
        #reset stage 2 extension for cars too close
        changeableConditions["stage2extended"] = 0

    #return to normal opperating mode    
    return intersectionData,changeableConditions, trafficStage, stageEndTime


'''
def thermistor_adjust(changeableConditions):
    if tempCelcius > 35:
        changeableConditions["stageLengths"][1] += 5
        changeableConditions["stageLengths"][4] += 5
'''


def normal_operation(board, board2, intersectionData,changeableConditions):
    """Manages the opperation of the traffic lights and polling loop

    Args:
        board: Arduino Set Up
        board2: 2nd Arduino Set Up
        intersectionData (dictonary): Data collected about the interesection
        changeableConditions (dictonary): Anything related to the system that changes
    Returns:
        intersectionData (dictonary): Data collected about the interesection
        changeableConditions (dictonary): Anything related to the system that changes
    """

    #define dictonary of traffic light colours to stage
    lightForStage = {
        1: ["green", "red", "red"],
        2: ["yellow", "red", "red"],
        3: ["red", "red", "red"],
        4: ["red", "green", "green"],
        5: ["red", "yellow", "flashing"],
        6: ["red", "red", "red"]
        } 

    # Begin normal operation, display to user
    mode = 'n'
    to_7_seg.sevenSeg(board2, mode)
    
    #Activate the pedestrian button checking, calculations and long term recording handled internally or by polling loop
    pedButton = changeableConditions['arduinoPins']['pedButton']
    board.set_pin_mode_digital_input(pedButton,callback=ped_button_callback)


    #pull traffic stage from dictonary
    trafficStage = changeableConditions['trafficStage']

    #use changeable conditions to start operation from suspended stage, restarts at stage 1
    if trafficStage == "suspended":
        intersectionData, changeableConditions, trafficStage, stageTimeEnd = traffic_stage_change(board, intersectionData, changeableConditions, trafficStage)
        #set light colours
        [mainState, sideState, pedestrianState] = lightForStage[changeableConditions["trafficStage"]]
        #output lights to arduino
        led.light_setting_state(board, changeableConditions, mainState, sideState, pedestrianState)
    
    try:
        while True:           
            ###TODO Remove once ped button working
            #if ped button doesn't work after entering polling loop, add activation to here
            
            
            #Check for Override switch
            overrideRead = board.analog_read(changeableConditions['arduinoPins']['normalOverride'])
            #print(overrideRead)
            if overrideRead[0] == 1023:
                #override switch active, suspend traffic sequence, exit normal operation mode
                trafficStage = "suspended"
                trafficStage = changeableConditions['trafficStage'] = "suspended"
                print("Manual Override Switch activated, exiting normal operation mode")
                return intersectionData, changeableConditions
            elif int(overrideRead[0])== 0:
                #Override switch not active, safe to enter normal operation mode
                pass
            #else: 
                # #Error line, unexpected switch circut reading
                # print("\n\n!!!!Irregular override switch reading...check override switch circuit!!!!!\n")
                # print(overrideRead)
                # #For while incomplete circiuts
                # print("Remain in normal opperation mode for debugging")
            
            
            ## PLACE PED BUTTON STAGE REDUCTION HERE
            #if there is more than 5 sec left in stage 1 check if the ped button was pressed
            if trafficStage == 1 and stageTimeEnd - time.time() > 5:
                #if the button was pressed reduced time left to 5 seconds from current time
                if time.time() - GLOB.lastButtonPress < 0.01:
                    stageTimeEnd = time.time() + 5


            # Does the traffic stage need changing?
            if time.time()>=stageTimeEnd:              
                #Check if the traffic stage is able to be changed if stage 2, ie next vechile isnt too close
                if trafficStage == 2 and changeableConditions["stage2extended"] == 0:
                    #Check for nearest vechile from ultrasonic
                    distToNextVechile = board.sonar_read(changeableConditions['arduinoPins']['triggerPin'])
                    if distToNextVechile[0] < changeableConditions["extensionTrigger"]:
                        stageTimeEnd += changeableConditions["extensionTrigger"]
                        #record that stage 2 was extended
                        changeableConditions["stage2extended"] = 1
                        #debugging line
                        print("stage 2 extended")
                else:
                    #Change traffic stage
                    intersectionData,changeableConditions, trafficStage, stageTimeEnd = traffic_stage_change(board, intersectionData, changeableConditions, trafficStage)
                    #set light colours
                    [mainState, sideState, pedestrianState] = lightForStage[changeableConditions["trafficStage"]] 
                    #output lights to arduino
                    led.light_setting_state(board, changeableConditions, mainState, sideState, pedestrianState)
             
            #if it is approprite to poll enter polling loop
            if intersectionData["timeRecord"] == [] or time.time() - intersectionData["timeRecord"][-1] >= changeableConditions["pollingRate"]:
                # Run function polling loop, inputting polling rate, output of polling time, current distance and pedestrian count
                [intersectionData, changeableConditions] = pl.polling_loop(board, board2, intersectionData, changeableConditions)
                #Happens within function 
                    #If polling start time plus polling time taken equals the current time
                    # Display polling time on console, “Polling loop took <polling time> to complete”
                    # If polling start time plus polling time taken equals the current time
                    # Display the current distance, “The distance to the closest vehicle is <current distance> cm.”
            elif time.time() - intersectionData["timeRecord"][-1] <= changeableConditions["pollingRate"]:
                #not enough time has passed, do not enter polling loop
                pass
            
            if trafficStage==3:
                pedestrianStage3 = intersectionData['pedPresentRecord'][-1]
                #Runnaway line commented out
                #print(f"pedestrian count at stage 3")
                to_7_seg.sevenSeg(board2, 'n', pedestrianStage3)

            #Due to need to continue flashing while polling loop still runs
            #trigger light setting again (ped green flashing) if in stage 5
            #if trafficStage == 5:
                #led.light_setting_state(board, changeableConditions, mainState, sideState, pedestrianState)
            if time.time() - intersectionData["overheightRecord"][-1]>=2 and changeableConditions["buzzerOnOff"] == 1:
                changeableConditions["buzzerOnOff"] = 0
                board.digital_write(changeableConditions["arduinoPins"]["buzzerFlashingOverHead"], changeableConditions["buzzerOnOff"])
    except KeyboardInterrupt:
        #exit button activation
        print("Exit button activated, returning to main menu\n\n\n\n\n")

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
