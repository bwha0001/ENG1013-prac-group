#Data Observation Mode
#Authors: Caitlin
#Version: 2 - Hardware implemented 
#Last Edit: 24 April 2024

import time
import to_7_segment_display as to_7_seg
import polling_loop as pl
import plotting_function

def data_observation_mode(board, board2, intersectionData, changeableConditions):
    """
    Where the user can veiw data collected about the intersection, displays graphs and counts to console
    
    Args:
        board: Arduino Set Up
        board2: 2nd Arduino Set Up
        intersectionData (dictonary): Data collected about the interesection
        changeableConditions (dictonary): Anything related to the system that changes
    """        
    
    #globals
    try:
        #Set 7 segment display to display d, using 7 segment display function
        #initalise varible for mode, mode used in any function call to print something to the 7 segment display
        mode = "d"
        to_7_seg.sevenSeg(board2, mode)
        #Stop polling loop, set traffic stage to suspended
        changeableConditions['trafficStage'] = "suspended"
        #Show polling loop time from normal operating mode
        print(f"Current Polling Interval is {changeableConditions['pollingRate']} seconds") 
        #get polling loop infomation 
        [intersectionData, changeableConditions, distToVehicleRecord, pedCount] = pl.polling_loop(board, board2, intersectionData, changeableConditions)
#test line        [distToVehicleRecord, pedCount] = [intersectionData['distToVehicleRecord'], intersectionData['pedCountRecord'][-1]] #logic testing line
        #Show user pedestrian counter value
        #If there is no data at all print message directing to run normal operation mode
        if pedCount == "No Data":
             print("There is no data to veiw, please enter normal operation mode(mode: 2) to collect data.\n Returning to main menu")
             return
        print(f"The current Pedestrian Count is {pedCount}")
        if len(intersectionData['pedCountRecord']) > 0:
                print(f"The current Pedestrian Count is {intersectionData['pedCountRecord'][-1]}")
        else:
                print(f"The current Pedestrian Count is {0}")


        #Check if there is enough recorded data, if so plot, if not notify user and plot sample?
        if changeableConditions['pollingRate'] * len(distToVehicleRecord) >= 20:
#test line            print("complete function plot triggered") #testing statememnt
            plotting_function.plotting_function(intersectionData['timeRecord'], intersectionData['distToVehicleRecord'])
        else:
            print("There is not 20 seconds of data, please return to normal operation mode to collect more data.\n To exit this mode enter ctrl + c in command window")    
    except KeyboardInterrupt:
        #exit button activation
        print("Exit button activated, returning to main menu")


#Software/No data collection test

# if __name__ == "__main__":
#     #initalisations
#     import time
#     import to_7_segment_display as to_7_seg
#     import polling_loop
#     import plotting_function
#     pollingRate = 2
#     changeableConditions = {
#         "trafficStage":1,
#         "pollingRate" : pollingRate, 
#         "pedCounterReset":""}
#     print("\n Test Case 1, not enough data")
#     intersectionData = {'timeRecord': [1712222887.311185, 1712222889.3174646, 1712222891.3379004], 'distToVehicleRecord': [3, 4, 4], 
#         'pedCountRecord': [1, 2, 2], 
#         'pedCounterReset': ''}
#     data_observation_mode(pollingRate)
#     time.sleep(3)
#     print("\n Test Case 2, 20 seconcds of data 1 ")
#     intersectionData = {'timeRecord': [1712223069.5302076, 1712223071.5480773, 1712223073.5522633, 1712223077.0124362, 1712223086.5804393, 1712223096.6703222, 1712223099.0712643, 1712223104.6489143, 1712223106.6522763, 1712223108.6540334], 'distToVehicleRecord': [7, 9, 5, 9, 4, 2, 7, 3, 6, 1], 'pedCountRecord': [0, 1, 2, 3, 3, 4, 4, 4, 5, 6], 'pedCounterReset': ''}
#     data_observation_mode(pollingRate)
#     time.sleep(3)
#     print("\n Test Case 3, 20 seconcds of data 2")
#     intersectionData = {'timeRecord': [1712223086.5804393, 1712223096.6703222, 1712223099.0712643, 1712223104.6489143, 1712223106.6522763, 1712223108.6540334, 1712223126.4707065, 1712223128.4798462, 1712223130.486405, 1712223132.496945], 'distToVehicleRecord': [4, 2, 7, 3, 6, 1, 2, 2, 8, 3], 'pedCountRecord': [3, 4, 4, 4, 5, 6, 6, 6, 6, 6], 'pedCounterReset': '', 'pedCountReset': 'stage1Reset'}
#     data_observation_mode(pollingRate)