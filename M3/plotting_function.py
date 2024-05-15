#Plotting Data
#Author: Jenny
#Last Edit: 10 April 2024
#Version: 2

import matplotlib.pyplot as plt
import time
import math as mth

# input ultrasonic sensor list and time list 
# voltage to distance calculation 
def plotting_function(changeableConditions, intersectionData, x, y):
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

    # plotList = range(((len(timeRecorded)-int(plotLength))//int(pollingRate)),len(timeRecorded)-1,-1) #values from end-plotLength to end counting from the end
    # plotList = range((len(timeRecorded)-int(plotLength)), len(timeRecorded)-1, pollingRate)
    # plotDistToVehichleRecord = []
    # plotSpeedRecord = []
    # plotTemperatureRecord = []
    # plotOverHeightRecord = []
    # for i in range(0,len(plotList)):
    #     plotDistToVehichleRecord.append(distToVehicleRecord[i])
    #     plotSpeedRecord.append(speedRecord[i])
    #     plotTemperatureRecord.append(temperatureRecord[i])
    #     plotOverHeightRecord.append(overHeight[i])
# Calculate the starting index
    plotLength = changeableConditions['plotLength']
    pollingRate = changeableConditions['pollingRate']
    distToVehicleRecord = intersectionData['distToVehicleRecord']
    overHeight = intersectionData["overheightRecord"]
    speedRecord = intersectionData['speedRecord']
    temperatureRecord = intersectionData['tempRecord']
    
    # Calculate the starting index
    # Calculate the starting index
    end_index = len(distToVehicleRecord) - 1
    start_index = max(0, end_index - mth.ceil(plotLength / pollingRate))

    # Generate timeSince
    timeSince = [round((end_index - i) * pollingRate, 2) for i in range(end_index, start_index - 1, -1)]

    # Trim lists to match the length of plotLength
    plotDistToVehicleRecord = distToVehicleRecord[start_index:]
    plotSpeedRecord = speedRecord[start_index:]
    plotTemperatureRecord = temperatureRecord[start_index:]
    plotOverHeightRecord = overHeight[start_index:]

    # Truncate timeSince if necessary to match data length
    if len(plotDistToVehicleRecord) < len(timeSince):
        timeSince = timeSince[:len(plotDistToVehicleRecord)]


    # Plotting
    if x.lower() == 'time':
        unitX = '(s)'
        xValue = timeSince
    else:
        unitX = ''
        xValue = range(len(plotDistToVehicleRecord)) #any variable with correct length
    
    if y.lower() == 'distance':
        unitY = '(cm)'
        yValue = plotDistToVehicleRecord
    elif y.lower() == 'velocity':
        unitY = 'cm/s'
        yValue = plotSpeedRecord
    elif y.lower() == 'overheight':
        unitY = '(cm)'
        yValue = plotOverHeightRecord
    elif y.lower() == "temperature":
        unitY = "degrees C"
        yValue = plotTemperatureRecord

    # Reverse both x_data and y_data
    xValues = list(reversed(xValue))
    yValues = list(reversed(yValue))

  # Reverse both x_data and y_data
    # xValue = list(reversed(timeSince))

    # this will work but a more robust method is to just record plot Length of data as a temp rather then deleting data

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

    # timeSince = []
    # for i in range(0, len(plotList), 1): # making this run to 20 would force 20 seconds of data to 
    #     # get around the bug where you go in and out of mode without running polling loop to manage distance
    #     timeSince.append(round(timeRecorded[i]-timeRecorded[-1], 2))
    
    # #Plotting
    # if x.lower() == 'time':
    #     unitX = '(s)'
    # if y.lower() == 'distance':
    #     unitY = '(cm)'
    #     yValue = plotDistToVehicleRecord
    # elif y.lower() == 'velocity':
    #     unitY = 'cm/s'
    #     yValue = plotSpeedRecord
    # elif y.lower() == 'overheight':
    #     unitY = '(cm)'
    #     yValue = plotOverHeightRecord
    # elif y.lower() == "temperature":
    #     unitY = "degrees C"
    #     yValue = plotTemperatureRecord

    plt.plot(xValues,yValues)
    plt.title(f'{y} vs. {x}')
    plt.xlabel(f"{x} {unitX}")
    plt.ylabel(f"{y} {unitY}")
    plt.show()
