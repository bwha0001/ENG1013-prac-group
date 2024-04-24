import matplotlib.pyplot as plt
import time

# input ultrasonic sensor list and time list 
# voltage to distance calculation 
def plotting_function(timeRecorded, distance):

    # globals
    # global intersectionData
    # global changeableConditions
    #Convert time record to number of seconds since
    timeSince = []
    for i in range(0, len(timeRecorded), 1):
        timeSince.append(round(timeRecorded[i]-timeRecorded[-1], 2))
    #Plotting
    plt.plot(timeSince,distance)
    plt.title('Distance vs. Time')
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (cm)")
    plt.show()

if __name__ == "__main__":
    print("\n Test Case 2, 20 seconcds of data 1 ")
    intersectionData = {'timeRecord': [1712223069.5302076, 1712223071.5480773, 1712223073.5522633, 1712223077.0124362, 1712223086.5804393, 1712223096.6703222, 1712223099.0712643, 1712223104.6489143, 1712223106.6522763, 1712223108.6540334], 'distToVehicleRecord': [7, 9, 5, 9, 4, 2, 7, 3, 6, 1], 'pedCountRecord': [0, 1, 2, 3, 3, 4, 4, 4, 5, 6], 'pedCounterReset': ''}
    plotting_function(intersectionData['timeRecord'], intersectionData['distToVehicleRecord'])
    print("\n Test Case 3, 20 seconcds of data 2")
    intersectionData = {'timeRecord': [1712223086.5804393, 1712223096.6703222, 1712223099.0712643, 1712223104.6489143, 1712223106.6522763, 1712223108.6540334, 1712223126.4707065, 1712223128.4798462, 1712223130.486405, 1712223132.496945], 'distToVehicleRecord': [4, 2, 7, 3, 6, 1, 2, 2, 8, 3], 'pedCountRecord': [3, 4, 4, 4, 5, 6, 6, 6, 6, 6], 'pedCounterReset': '', 'pedCountReset': 'stage1Reset'}
    plotting_function(intersectionData['timeRecord'], intersectionData['distToVehicleRecord'])