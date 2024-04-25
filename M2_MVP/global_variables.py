#File for storage of global varibles
#Authors: Team F12
#Version: 1 - Implemented for the button
#Last Edit: 25 April 2024


# Define your global variables here
pedsPresent = None
lastButtonPress = None
intersectionData = None
changeableConditions = None
pollingRate = None

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
