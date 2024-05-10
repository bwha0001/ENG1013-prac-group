#File for storage of global varibles
#Authors: Ben Whan
#Version: 1 - Implemented for the button
#Last Edit: 25 April 2024


"""
    This module holds global variables that are required to make the call back function to run the 
    ped_button function work in order to have an interrupt so the pedestrian button can be 
    pressed at any time as long as the polling loop is active
"""

# Define your global variables 
pedsPresent = None
lastButtonPress = None
overHeadTime1 = None
overHeadTime2 = None

# Initialize the global variables
def init():
    """
        init holds the global variables, so in order to intialise the globals init() is called
        in the initial set up and the rest of the global_variables become accesable across multiple files

    """
    global pedsPresent
    global lastButtonPress 
    global overHeadTime1
    global overHeadTime2
    
    
    # Initialize your global variables 
    pedsPresent = 0
    lastButtonPress = 0
    overHeadTime1 = 0
    overHeadTime2 = 0
    
