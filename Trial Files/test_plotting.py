
from matplotlib import pyplot as plt
import numpy as np
import math

def plotting_function(changeableConditions, intersectionData, x, y):
    try:
        # Load in all lists
        timeRecorded = intersectionData['timeRecord']
        pollingRate = changeableConditions['pollingRate']
        distToVehicleRecord = intersectionData['distToVehicleRecord']
        overHeight = intersectionData["overheightRecord"]
        plotLength = changeableConditions['plotLength']
        speedRecord = intersectionData['speedRecord']
        temperatureRecord = intersectionData['tempRecord']
        
        # Calculate the number of points to show in the plot
        points_to_show = max(plotLength, len(timeRecorded) * pollingRate)

        # Getting values ready for y values
        plotDistToVehicleRecord = distToVehicleRecord[-(points_to_show + 1):]
        plotOverHeightRecord = overHeight[-(points_to_show + 1):]
        plotSpeedRecord = speedRecord[-(points_to_show + 1):]
        plotTemperatureRecord = temperatureRecord[-(points_to_show + 1):]

        # x values
        plotTime = timeRecorded[-(points_to_show + 1):]

        # Ensure x and y arrays have the same length
        xValue = plotTime[:min(plotLength, len(plotTime))]

        # Plotting
        if y.lower() == 'distance':
            unitY = '(cm)'
            yValue = plotDistToVehicleRecord[:len(xValue)]
        elif y.lower() == 'velocity' or "speed":
            unitY = 'cm/s'
            yValue = plotSpeedRecord[:len(xValue)]
        elif y.lower() == 'overheight':
            unitY = '(cm)'
            yValue = plotOverHeightRecord[:len(xValue)]
        elif y.lower() == "temperature":
            unitY = "degrees C"
            yValue = plotTemperatureRecord[:len(xValue)]

        plt.plot(xValue, yValue)
        
        ax = plt.gca()
        # ax.set_ylim(ax.get_ylim()[::-1])
        ax.set_xlim(ax.get_xlim()[::-1])

        plt.title(f'{y} vs. {x}')
        plt.xlabel(f"{x} (s)")
        plt.ylabel(f"{y} {unitY}")
        plt.show()
    except Exception as e:
        print(f"Error: {e}")

        
changeableConditions = {
    "pollingRate" : 2,
    "plotLength": 50,
}
intersectionData = {
    "distToVehicleRecord" : np.arange(100),
    "timeRecord" :  np.arange(100),
    "overheightRecord": np.random.randint(50, size=100),
    "speedRecord" : np.random.randint(20, size=100),
    "tempRecord" : np.random.randint(10, size=35)
}

plotting_function(changeableConditions, intersectionData, "time", "velocity")

