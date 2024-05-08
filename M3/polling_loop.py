#polling loop
#Authors: Caitlin and Kayla and Ben
#Version: 5 - Hardware Implementation
#Dates Edited: 25 April 2024

import time
import global_variables as GLOB
import to_7_segment_display as to_7_seg
import instentaneous_speed 
# import AAstart as start

def ped_button_callback(data):
    """
    Callback function for pedestrian button press.
    """
    if data[2] == 1 and time.time() > GLOB.lastButtonPress + 0.0001:
        GLOB.pedsPresent += 1
        GLOB.lastButtonPress = time.time()
 

def polling_loop(board, board2, intersectionData, changeableConditions):
    """
    Reads and stores from intersection sensors
    
    Args:
        board: Arduino Set Up
        board2: 2nd Arduino Set Up
        intersectionData (dictonary): Data collected about the interesection
        changeableConditions (dictonary): Anything related to the system that changes

    Returns:
        intersectionData (dictonary): Data collected about the interesection
        changeableConditions (dictonary): Anything related to the system that changes
    Conditional Returns, when intersection opperation is suspended:
        distToVechile(list): distance to next vechile record for the last 20 seconds
        pedCount(int): number of pedestrian button presses in current iteration of the traffic sequence

    """    
    #globals

    pollingRate = changeableConditions['pollingRate']
    trafficStage = changeableConditions['trafficStage']
    
    
    #import data from dictonary of intersectionData
    timeRecord = intersectionData['timeRecord']
    distToVehicleRecord = intersectionData['distToVehicleRecord1']
    overheightDist = intersectionData["overheightRecord"] #  initialising overheight sensor as well
    pedCountRecord = intersectionData['pedCountRecord']
    speedRecord = intersectionData['speedRecord']



    #Traffic Stage approprite for new readings? ie Not suspended stage and enough time has passed
    #is in the correct stage to pollling to continue
    if trafficStage in {1,2,3,4,5,6}:
        if intersectionData["timeRecord"] == []:
            pass
        elif time.time() - intersectionData["timeRecord"][-1] <= pollingRate:
            return [intersectionData, changeableConditions]
        elif time.time() - intersectionData["timeRecord"][-1] >= pollingRate:
            pass
    elif  trafficStage == "suspended":
        #return distToVechile and current pedestrian count from prior loop
        try:
            return [intersectionData, changeableConditions, intersectionData['distToVehicleRecord1'], intersectionData['pedCountRecord'][-1]]
        except IndexError:
            return [intersectionData, changeableConditions, intersectionData['distToVehicleRecord1'], "No Data"]
        
    #Set loop start time
    pollingStartTime = time.time()
    
    #Take readings for distance to next vehcile (ultrosonic sensor reading) and pedestrian button pressed
    distToVehicle1, distReadingTime1 = board.sonar_read(changeableConditions["arduinoPins"]["triggerPin"]) 
    overHeightDist, distReadingTime1 = board.sonar_read(changeableConditions["arduinoPins"]["triggerPin2"])

    time.sleep(0.05)
    distToVehicle2, distReadingTime2 = board.sonar_read(changeableConditions["arduinoPins"]["triggerPin"])
    
    ## adding collecting instentaneous velocity by running the ultrasonic sensor twice
    speed = instentaneous_speed.velocity(distToVehicle1, distToVehicle2, distReadingTime1, distReadingTime2)
    speedRecord.append(speed)
    
    #intersectionData["speedRecord"].append(speed)

    ###################
    #over height detection with a bit of ASCI art to make sure its obvious
    if overHeightDist <changeableConditions["overHeight"]: #change over height in changeable conditions rather then just hardcode
        print("##########################################\n")
        print("WARNING, VEHICHLE OVERHEIGHT\n")
        print("##########################################\n")
    #################### need to flash an led --> write as a function to flash an independant LED

    ##############################################################################################
    # add in a line of code to take temperature as a voltage from an analogue input
    thermRes = board.analog_read(changeableConditions["arduinoPins"]["temperaturePin"])
    tempVoltage = thermistor_voltage(thermRes, voltIn)
    tempCelcius = temperature(tempVoltage)
    intersectionData['temperatureRecord'].append(tempcelcius)

    #code for LDR to take light from an analogue input
    #light = board.analog_read(changeableConditions["arduinoPins"]["ldrPin"])
    #intersectionData['lightRecord'].append(light)

    # pedsPresent, lastButtonPress = ped_button(pedsPresent, lastButtonPress)
    pedButton = changeableConditions['arduinoPins']['pedButton']
    board.set_pin_mode_digital_input(pedButton,callback=ped_button_callback)
    
    #Update pedButtonRecord to number of presses so far
    intersectionData['pedPresentRecord'].append(GLOB.pedsPresent)

    if intersectionData['pedCountRecord'] == [] or changeableConditions["pedCounterReset"]=="stage1Reset":
        #pedestrians so far in this interation of traffic sequence
        pedCount = 0
        #Set to 0 as there have been no peds in this interation of traffic sequence
        pedButton = 0
        # changeableConditions["pedCounterReset"]==""
    elif not intersectionData['pedCountRecord'] == []:
        pedCount = intersectionData['pedCountRecord'][-1]
        #find the number of pedButton presses between polling loops, pedButton
        pedButton = intersectionData['pedPresentRecord'][-1]-intersectionData['pedPresentRecord'][-2]

    #Test line - global updating
    #print(GLOB.pedsPresent)

    #Update ped count total
    pedCount += pedButton
    

    #Store record of time of readings, ultrasonic sensor reading and pedestrian count, all stored with same list index
    intersectionData['timeRecord'].append(pollingStartTime)
    intersectionData['distToVehicleRecord1'].append(distToVehicle1)
    intersectionData['pedCountRecord'].append(pedCount)
    intersectionData["overheightRecord"].append(overHeightDist)
    

#this limits data to 20 seconds, now it holds data for infinite length and adjusting pot length will be done in plotting
    # #Check if all lists have more readings than should be the case for 20 seconds, remove earliest reading to bring back to 20 sec
    # if len(timeRecord)>(20/pollingRate) and len(distToVehicleRecord)>(20/pollingRate) and len(pedCountRecord)>(20/pollingRate):
    #     #Remove first item in each of the lists
    #     #aliasing back to dictionaries
    #     timeRecord.pop(0)
    #     distToVehicleRecord.pop(0)
    #     pedCountRecord.pop(0)
    #     intersectionData["speedRecord"].pop(0)
    #     # intersectionData['temperatureRecord'].pop(0)


        

    #Set polling time to the time it took to execute
    # time.sleep(changeableConditions['pollingRate'])
    pollingEndTime = time.time()
    pollingTime = pollingEndTime - pollingStartTime
    #Print time between readings, if it is the inital readings print differant message
    try:
        print(f"\nTime between polling readings: {round(timeRecord[-1]-timeRecord[-2], 2):.2f} seconds.")
    except IndexError:
        print(f"Taking inital readings took {round(pollingTime,2):.2f} seconds.")
    #Print the distnace to the nearest vechile
    print(f"Distance to nearest vechile: {round(float(distToVehicle1),2):.2f} cm\n")
   
    to_7_seg.sevenSeg(board2, 'n', distToVehicle1) # display distance to vehicle
    return intersectionData, changeableConditions

# #Hardware Test
# if __name__ == "__main__":
#     import random
#     from pymata4 import pymata4
    
#     #function for pedButton
#     def ped_button(data):
#         """
#         :param data: a list containing pin type, pin number, 
#                     data value and time-stamp
#         """
        
#         # Print the value out (code goes here to do something with the data)
#         global pedsPresent
#         global lastButtonPress

#         if data[2] ==1 and time.time() > lastButtonPress+0.0001:
#             pedsPresent += 1
#             lastButtonPress = time.time()
#             print(f"Peds present: {pedsPresent}")

#         print(f"Test line button data: {data}")
#         #lastButtonPress = time.time()

#     #Create a dictonary of records
#     intersectionData = {"timeRecord":[], "distToVehicleRecord":[], "pedCountRecord":[], "pedCounterReset":""}

#     pollingRate = 2
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
#             "pedButton":10,
#             "triggerPin":13,
#             "echoPin":12
#             },
#         'ardinoPins7Seg': {},
#         'trafficStage' : 1, # in the led state we need a case switching so we can assign the correct R,Y,G states from traffic stage, not neccercarily, was originally designed to have individual states entered within function call
#         'pollingRate' : 2,
#         'pedCounterReset' : ""
#         }
    
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
#     lastButtonPress = time.time() - 0.1
#     board.set_pin_mode_digital_input(changeableConditions["arduinoPins"]["pedButton"], callback=ped_button)
    
#     board2 = ''

#     #Test for 30 seconds
#     startTime = time.time()

#     while startTime + 30 > time.time():
#         try:
#             polling_loop(board, board2, intersectionData, changeableConditions)
#         except KeyboardInterrupt:
#             print("Close")
#             break
#     board.shutdown()
#     exit()

'''
    while True:
        try:
            polling_loop(board, intersectionData, changeableConditions)
        except KeyboardInterrupt:
            print("Close")
            board.shutdown()
            exit()
'''

#sOFTWARE TEST
# if __name__ == "__main__":
#     #external initalisations
#     #Creates a dictonary of records for data collected
    
#     intersectionData = {"timeRecord":[], "distToVehicleRecord":[], "pedCountRecord":[]}
#     pollingRate = 2
#     changeableConditions = {
#         "trafficStage":1,
#         "pollingRate" : pollingRate, 
#         "pedCounterReset":""}
    
#     for i in range(0,25):
#         if i < 5:
#             trafficStage = 1
#         elif i == 5 :
#             trafficStage = 2
#         elif i==15:
#             trafficStage = 7
#         elif i==20:
#             changeableConditions["pedCounterReset"]="stage1Reset"
#             trafficStage=1
#         print(f"i={i}, trafficStage={trafficStage}")
#         pollingReturn = polling_loop(intersectionData, changeableConditions)
#         if pollingReturn == "None":
#             pass
#         else:
#             print(pollingReturn)
#         time.sleep(1)
#     print(intersectionData)
