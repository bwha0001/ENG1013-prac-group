#polling loop
#Authors: Caitlin and Kayla 
#Version: 4 - List Storage and Global Dictonary Used, incorrect output fixed
#Dates Edited: 4 April 2024

import time
import random

def polling_loop(trafficStage, pollingRate = 2):
    '''
    Polling loop gets and stores data from sensors in intersection
    Arg:
        Traffic Stage {1,2,3,4,5,6,"suspended"}, polling rate
    Returns:
        if suspended [distance to next vechile list, pedestrian count]
    '''
    #globals
    global intersectionData
    global changeableConditions
    #required for MVP Checkpoint
    import random
    
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
        changeableConditions["pedCounterReset"]==""
    elif not intersectionData['pedCountRecord'] == []:
        pedCount = intersectionData['pedCountRecord'][-1]
    
    #Traffic Stage approprite for new readings? ie Not suspended stage and enough time has passed
    if trafficStage in {1,2,3,4,5,6}:
        pass
    elif  trafficStage == "suspended":
        #return distToVechile and current pedestrian count from prior loop
        return [intersectionData['distToVehicleRecord'], intersectionData['pedCountRecord'][-1]]
    
    if intersectionData["timeRecord"] == []:
        pass
    elif time.time() - intersectionData["timeRecord"][-1] <= pollingRate:
        return
    elif time.time() - intersectionData["timeRecord"][-1] >= pollingRate:
        pass
        
    #Set loop start time
    pollingStartTime = time.time()

    #Take readings for distance to next vehcile (ultrosonic sensor reading) and pedestrian button pressed
    #Placeholder generation for MVP Checkpoint
    distToVehicle = random.randint(1,10)

    #Has the pedestrian been pressed 
    #.....  (input of pedButton) = 1?
    pedButton = random.randint(0,1)

    if pedButton == 1:
        pedCount += 1

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

    return [distToVehicle, pedCount, pollingTime]


if __name__ == "__main__":
    #external initalisations
    #Creates a dictonary of records for data collected
    
    intersectionData = {"timeRecord":[], "distToVehicleRecord":[], "pedCountRecord":[]}
    pollingRate = 2
    changeableConditions = {
        "trafficStage":1,
        "pollingRate" : pollingRate, 
        "pedCounterReset":""}
    
    for i in range(0,25):
        if i < 5:
            trafficStage = 1
        elif i == 5 :
            trafficStage = 2
        elif i==15:
            trafficStage = 7
        elif i==20:
            changeableConditions["pedCounterReset"]="stage1Reset"
            trafficStage=1
        print(f"i={i}, trafficStage={trafficStage}")
        pollingReturn = polling_loop(trafficStage)
        if pollingReturn == "None":
            pass
        else:
            print(pollingReturn)
        time.sleep(1)
    print(intersectionData)
    