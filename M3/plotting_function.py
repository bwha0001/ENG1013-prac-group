#Plotting Data
#Author: Jenny
#Last Edit: 10 April 2024
#Version: 2

import matplotlib.pyplot as plt
import time

# input ultrasonic sensor list and time list 
# voltage to distance calculation 
def plotting_function(changeableConditions, intersectionData, timeRecorded, distance, x, y):
    """
    Creates and displays graphs of data collected by sensors
    Args:
        timeRecorded (list): list of floats of time that readings were taken
        distance (list): list of floats of distance to next vechile readings
    """

# TODO handle values to length from changeable conditions
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
    timeRecorded = intersectionData['timeRecord']
    #Convert time record to number of seconds since
    pollingRate = intersectionData['pollingRate']
    distToVehicleRecord = intersectionData['distToVehicleRecord']
    plotLength = changeableConditions['plotLength']
    speedRecord = intersectionData['speedRecord']
    # this will work but a more robust method is to just record plot Length of data as a temp rather then deleting data
    plotList = range(((len(timeRecorded)-plotLength)/pollingRate),len(timeRecorded)-1,-1) #values from end-plotLength to end counting from the end
    plotDistToVehichleRecord = []
    plotSpeedRecord = []
    for i in plotList:
        plotDistToVehichleRecord.append(distToVehicleRecord(i))
        plotSpeedRecord.append(speedRecord(i))



    # ########## leave below if collecting data points doesn't work
    # flag = True
    # while flag:
    #     if len(timeRecorded)>(plotLength/pollingRate): 
    #         timeRecorded.pop(0)
    #     if len(distToVehicleRecord)>(plotLength/pollingRate):
    #         distToVehicleRecord.pop(0)
    #     if len(pedCountRecord)>(plotLength/pollingRate):
    #         pedCountRecord.pop(0)
    #     if len(speedRecord)>(plotLength/pollingRate):
    #         velocity.pop(0)
    #     #if len(temperatureRecord)> (plotLength/pollingRate):    
    #     # intersectionData['temperatureRecord'].pop(0)
    #     if len(timeRecorded)<(plotLength/pollingRate) and  len(distToVehicleRecord)<(plotLength/pollingRate) and len(pedCountRecord)>(plotLength/pollingRate) and len(speedRecord)>(plotLength/pollingRate):
    #         flag = False

    ##########

    timeSince = []
    for i in range(0, len(plotList), 1): # making this run to 20 would force 20 seconds of data to 
        # get around the bug where you go in and out of mode without running polling loop to manage distance
        timeSince.append(round(timeRecorded[i]-timeRecorded[-1], 2))
    
    #Plotting
    if x.lower == 'time':
        unitX = '(s)'
    if y.lower() == 'distance':
        unitY = '(cm)'
        yValue = plotDistToVehichleRecord
    if y.lower() == 'velocity':
        unitY = 'cm/s'
        yValue = plotSpeedRecord

    plt.plot(timeSince,yValue)
    plt.title(f'{y} vs. {x}')
    plt.xlabel(f"{x} {unitX}")
    plt.ylabel(f"{y} {unitY}")
    plt.show()
