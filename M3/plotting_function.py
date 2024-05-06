#Plotting Data
#Author: Jenny
#Last Edit: 10 April 2024
#Version: 2

import matplotlib.pyplot as plt
import time

# input ultrasonic sensor list and time list 
# voltage to distance calculation 
def plotting_function(changeableConditions, timeRecorded, distance):
    """
    Creates and displays graphs of data collected by sensors
    Args:
        timeRecorded (list): list of floats of time that readings were taken
        distance (list): list of floats of distance to next vechile readings
    """

# TODO handle values to length from changeable conditions
    #Convert time record to number of seconds since
    timeSince = []
    for i in range(0, len(timeRecorded), 1): # making this run to 20 would force 20 seconds of data to 
        # get around the bug where you go in and out of mode without running polling loop to manage distance
        timeSince.append(round(timeRecorded[i]-timeRecorded[-1], 2))
    #Plotting
    plt.plot(timeSince,distance)
    plt.title('Distance vs. Time')
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (cm)")
    plt.show()
