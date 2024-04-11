import time
import math as mth
#ST. from pymata4 import pymata4 
import module_scripts as ms
import to_7_segment_display as to_7_seg
import maintenance_mode as m_m
import led_state as led
import traffic_light_sequence as TLS
import main_menu as main
import normal_operation as n_o

#globals
global intersectionData
#Creates a dictonary of records if one doesnt exist
intersectionData = {"timeRecord":[], "distToVehicleRecord":[], "pedCountRecord":[], "pedCounterReset":""}
global changeableConditions 
global pollingRate
pollingRate = 2
changeableConditions = {
    'trafficStage' : 1,
    'pollingRate' : pollingRate,
    'pedCounterReset' : ""
    }

#functions
def polling_loop(trafficStage, pollingRate = 2):
    '''
    Polling loop gets and stores data from sensors in intersection
    Arg:
        Traffic Stage {1,2,3,4,5,6,"suspended"}, polling rate
    Returns:
        if suspended [distance to next vechile list, pedestrian count]
    '''

    #required for MVP Checkpoint
    import random
    
    #polling loop to read sensors for traffic control
    #inputs: trafficStage, pollingRate which defaults to 2
    #outputs: Current distance to next vehicle, Distance to vehicle record, Pedestrian Counter, Time taken for polling

    #Creates a dictonary of records if one doesnt exist
    try:
        intersectionData
    except NameError:
        print("Can't access global intersection data")
        intersectionData = {"timeRecord":[], "distToVehicleRecord":[], "pedCountRecord":[]}

    try:
        changeableConditions
    except:
        print("Can't access changeable conditons, defining ")
        changeableConditions = {
            'trafficStage' : 1,
            'pollingRate' : pollingRate,
            'pedCounterReset' : ""
            }

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


def data_observation_mode(pollingRate):
    try:
        #Set 7 segment display to display d, using 7 segment display function TODO # output code is active ?
#        to_7_seg.sevenSeg("d.")
        #Stop polling loop, set traffic stage to suspended
        changeableConditions['trafficStage'] = "suspended"
        #Show polling loop time from normal operating mode
        print(f"Current Polling Interval is {pollingRate} seconds")

        #get polling loop infomation 
        [distToVehicleRecord, pedCount] = polling_loop(changeableConditions['trafficStage'], changeableConditions['pollingRate'])
#test line        [distToVehicleRecord, pedCount] = [intersectionData['distToVehicleRecord'], intersectionData['pedCountRecord'][-1]] #logic testing line
        #Show user pedestrian counter value
#        print(f"The current Pedestrian Count is {pedCount}")
        print(f"The current Pedestrian Count is {intersectionData['pedCount'][-1]}")

        #Check if there is enough recorded data, if so plot, if not notify user and plot sample?
        if pollingRate * len(distToVehicleRecord) >= 20:
#test line            print("complete function plot triggered") #testing statememnt
            plotting_function(intersectionData['timeRecord'], intersectionData['distToVehicleRecord'])
        else:
            print("There is not 20 seconds of data, please return to normal operation mode to collect more data.\n To exit this mode enter ctrl + c in command window")    
    except KeyboardInterrupt:
        #exit button activation
        print("Exit button activated, returning to main menu")

while True:
    try:

        
        trafficStage = 1
        data_observation_mode(trafficStage)


        main.main_menu()
        print("hi")
    except KeyboardInterrupt:
        break
data_observation_mode(2)

