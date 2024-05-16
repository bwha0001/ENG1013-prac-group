from matplotlib import pyplot as plt
from numpy import random


def plotting_function(changeableConditions, intersectionData, x, y):
    """
    Creates and displays graphs of data collected by sensors
    Args:
        timeRecorded (list): list of floats of time that readings were taken
        distance (list): list of floats of distance to next vechile readings
    """


    timeRecorded = intersectionData['timeRecord']
    pollingRate = changeableConditions['pollingRate']
    distToVehicleRecord = intersectionData['distToVehicleRecord']
    plotLength = changeableConditions['plotLength']

    scatter = plt.plot(timeRecorded, distToVehicleRecord)
    ax = plt.gca()
    ax.set_ylim(ax.get_ylim()[::-1])
    ax.set_xlim(ax.get_xlim()[::-1])

    plt.show()
    
    # # plotList = range(((len(timeRecorded)-int(plotLength))//int(pollingRate)),len(timeRecorded)-1,-1) #values from end-plotLength to end counting from the end
 
    # plotList = range(0,plotLength, -pollingRate)
    # plotDistToVehichleRecord = []

    # # for i in range(len(plotList)-plotLength,len(plotList), -1):
    # for i in plotList:
    #     plotDistToVehichleRecord.append(distToVehicleRecord[i])



    # timeSince = []
    # # for i in range(len(plotList)-plotLength, len(plotList), -1): # making this run to 20 would force 20 seconds of data to 
    # for i in plotList:
    #     # get around the bug where you go in and out of mode without running polling loop to manage distance
    #     timeSince.append(round(timeRecorded[i]-timeRecorded[-1], 2))
    
    # #Plotting
    # if x.lower() == 'time':
    #     unitX = '(s)'
    # if y.lower() == 'distance':
    #     unitY = '(cm)'
    #     yValue = plotDistToVehichleRecord
    # elif y.lower() == 'velocity':
    #     unitY = 'cm/s'
    #     yValue = plotSpeedRecord
    # elif y.lower() == 'overheight':
    #     unitY = '(cm)'
    #     yValue = plotOverHeightRecord
    # elif y.lower() == "temperature":
    #     unitY = "degrees C"
    #     yValue = plotTemperatureRecord

    # plt.plot(timeSince,yValue)
    # plt.title(f'{y} vs. {x}')
    # plt.xlabel(f"{x} {unitX}")
    # plt.ylabel(f"{y} {unitY}")
    # plt.show()


changeableConditions = {
    "pollingRate" : 2,
    "plotLength": 20,
}
intersectionData= {
    # "distToVehicleRecord" : random.randint(100, size = (100)),
    "distToVehicleRecord" : range(0,100,1),
    "timeRecord" :  range(0,100,1)
}

plotting_function(changeableConditions, intersectionData, "time", "distance")