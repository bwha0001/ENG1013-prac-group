#polling loop
#Authors: Caitlin and Kayla 
#Version: 5 - Hardware Implementation
#Dates Edited: 24 April 2024

import time

#function for pedButton
def ped_button(data):
    """
    :param data: a list containing pin type, pin number, 
                data value and time-stamp
    """
    
    # Print the value out (code goes here to do something with the data)
    global pedsPresent
    global lastButtonPress

    if data[2] ==1 and time.time() > lastButtonPress+0.0001:
        pedsPresent += 1
        lastButtonPress = time.time()
        print(f"Peds present: {pedsPresent}")

    print(f"Test line button data: {data}")
    #lastButtonPress = time.time()

def polling_loop(board, intersectionData, changeableConditions):
    '''
    Polling loop gets and stores data from sensors in intersection
    Arg:
        board, Traffic Stage {1,2,3,4,5,6,"suspended"}, polling rate
    Returns:
        if suspended [distance to next vechile list, pedestrian count]
    '''
    #globals
    pollingRate = changeableConditions['pollingRate']
    trafficStage = changeableConditions['trafficStage']

    global pedsPresent

    #required for MVP Checkpoint

    #polling loop to read sensors for traffic control
    #inputs: trafficStage, pollingRate which defaults to 2
    #outputs: Current distance to next vehicle, Distance to vehicle record, Pedestrian Counter, Time taken for polling

    #Creates a dictonary of records if one doesnt exist
    try:
        intersectionData
    except NameError:
        print("Can't access golbal intersection data")
        intersectionData = {"timeRecord":[], "distToVehicleRecord":[], "pedCountRecord":[]}

    #import data from dictonary of intersectionData
    timeRecord = intersectionData['timeRecord']
    distToVehicleRecord = intersectionData['distToVehicleRecord']
    pedCountRecord = intersectionData['pedCountRecord']

    if intersectionData['pedCountRecord'] == [] or changeableConditions["pedCounterReset"]=="stage1Reset":
        pedCount = 0
        # changeableConditions["pedCounterReset"]==""
    elif not intersectionData['pedCountRecord'] == []:
        pedCount = intersectionData['pedCountRecord'][-1]

    #Traffic Stage approprite for new readings? ie Not suspended stage and enough time has passed
    if trafficStage in {1,2,3,4,5,6}:
        pass
    elif  trafficStage == "suspended":
        #return distToVechile and current pedestrian count from prior loop
        try:
            return [intersectionData, changeableConditions, intersectionData['distToVehicleRecord'], intersectionData['pedCountRecord'][-1]]
        except IndexError:
            return [intersectionData, changeableConditions, intersectionData['distToVehicleRecord'], "No Data"]
    
    if intersectionData["timeRecord"] == []:
        pass
    elif time.time() - intersectionData["timeRecord"][-1] <= pollingRate:
        return [intersectionData, changeableConditions]
    elif time.time() - intersectionData["timeRecord"][-1] >= pollingRate:
        pass
        
    #Set loop start time
    pollingStartTime = time.time()

    #Take readings for distance to next vehcile (ultrosonic sensor reading) and pedestrian button pressed
    #Placeholder generation for MVP Checkpoint
    distToVehicle, distReadingTime = board.sonar_read(changeableConditions["arduinoPins"]["triggerPin"])


    #Update ped count total
    pedCount = pedCount + pedsPresent
    #Once total updated, reset the ped present count inbetween saves by polling
    pedsPresent= 0
    #Has the pedestrian been pressed 
    #.....  (input of pedButton) = 1?
    
    """pedButton = random.randint(0,1)

    if pedButton == 1:
        pedCount += 1"""

    #Store record of time of readings, ultrasonic sensor reading and pedestrian count, all stored with same list index
    timeRecord.append(pollingStartTime)
    distToVehicleRecord.append(distToVehicle)
    pedCountRecord.append(pedCount)

    #Check if all lists have more readings than should be the case for 20 seconds, remove earliest reading to bring back to 20 sec
    if len(timeRecord)>20/pollingRate and len(distToVehicleRecord)>20/pollingRate and len(pedCountRecord)>20/pollingRate:
        #Remove first item in each of the lists
        timeRecord.pop(0)
        distToVehicleRecord.pop(0)
        pedCountRecord.pop(0)

    #Set polling time to the time it took to execute
    pollingEndTime = time.time()
    pollingTime = pollingEndTime - pollingStartTime
    print(f"Time taken to poll: {round(pollingTime, 2)} seconds")
    #Print the distnace to the nearest vechile
    print(f"Distance to nearest vechile: {distToVehicle} cm")
    #test line
    print(f"Test Line Ped Count Record Value: {pedCount}\n")

    return intersectionData, changeableConditions

#Hardware Test
if __name__ == "__main__":
    import random
    from pymata4 import pymata4
    
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
            "pedestrianGreen": 9,
            "pedButton":10,
            "triggerPin":11,
            "echoPin":12
            },
        'ardinoPins7Seg': {},
        'trafficStage' : 1, # in the led state we need a case switching so we can assign the correct R,Y,G states from traffic stage, not neccercarily, was originally designed to have individual states entered within function call
        'pollingRate' : 2,
        'pedCounterReset' : ""
        }
    
    board =pymata4.Pymata4()

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
    board.set_pin_mode_sonar(changeableConditions["arduinoPins"]["triggerPin"], changeableConditions["arduinoPins"]["echoPin"], timeout=200000)
    #Start ped button checker
    pedsPresent = 0
    lastButtonPress = time.time() - 0.1
    board.set_pin_mode_digital_input(changeableConditions["arduinoPins"]["pedButton"], callback=ped_button)
    
    #Test for 30 seconds
    startTime = time.time()

    while startTime + 30 > time.time():
        try:
            polling_loop(board, intersectionData, changeableConditions)
        except KeyboardInterrupt:
            print("Close")
            break
    board.shutdown()
    exit()

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
