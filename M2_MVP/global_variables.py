<<<<<<< Updated upstream
#File for storage of global varibles
#Authors: Team F12
#Version: 1 - Implemented for the button
#Last Edit: 25 April 2024

=======
"""
    This module holds global variables that are required to make the call back function to run the 
    ped_button function work in order to have an interrupt so the pedestrian button can be 
    pressed at any time as long as the polling loop is active
"""
>>>>>>> Stashed changes

# Define your global variables here
pedsPresent = None
lastButtonPress = None

# Initialize the global variables
def init():
    global pedsPresent
    global lastButtonPress 
    # global intersectionData
    # global changeableConditions 
    # global pollingRate
    
    # Initialize your global variables here
    pedsPresent = 0
    lastButtonPress = 0
    # intersectionData = {}  # Initialize as an empty dictionary
    # changeableConditions = {}  # Initialize as an empty dictionary
    # pollingRate = 3  # Default polling rate
