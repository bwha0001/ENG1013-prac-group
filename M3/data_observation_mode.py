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
             print("There is no data to veiw, please enter normal operation mode(mode: d) to collect data.\n Returning to main menu")
             return
        print(f"The current Pedestrian Count is {pedCount}")
        if len(intersectionData['pedCountRecord']) > 0:
                print(f"The current Pedestrian Count is {intersectionData['pedCountRecord'][-1]}")
                to_7_seg.sevenSeg(board2,'p')
                to_7_seg.sevenSeg(board2, mode, intersectionData['pedCountRecord'][-1])
        else:
                print(f"The current Pedestrian Count is {0}")


        #Check if there is enough recorded data, if so plot, if not notify user and plot sample?
        plotLength = changeableConditions["plotLength"]
        if changeableConditions['pollingRate'] * len(distToVehicleRecord) >= plotLength:
#test line            print("complete function plot triggered") #testing statememnt
                plotting_function.plotting_function(changeableConditions, intersectionData, 'time', 'distance')
                plotting_function.plotting_function(changeableConditions, intersectionData, 'time', 'velocity')
                plotting_function.plotting_function(changeableConditions, intersectionData, 'time', 'overHeight')
                plotting_function.plotting_function(changeableConditions, intersectionData, 'time', 'temperature')

          
            ##############################################
            # plot temperature
        else:
            print("There is not 20 seconds of data, please return to normal operation mode to collect more data.\n To exit this mode enter ctrl + c in command window")    
    except KeyboardInterrupt:
        #exit button activation
        print("Exit button activated, returning to main menu")

