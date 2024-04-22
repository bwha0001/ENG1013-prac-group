#TODO File header
import to_7_segment_display
import polling_loop
import time

# function traffic stage change
# 	inputs:  current traffic stage
#      This function takes care of the repeated processes of a change in traffic stage in the traffic control system and the tasks that occur at particular stages. Displaying stage specific outputs to console. 
# 	Outputs: current traffic stage

# Reset stage start time to current time
# What is the current stage
# if current stage is 1, 3, 4, 5
# Increase the traffic stage by 1
# Display “Commencing Traffic Stage <traffic stage>” on console
# If the current stage is 3
# Increase the traffic stage by 1
# Display “Commencing Traffic Stage <traffic stage>” on console
# Display “The current pedestrian count is <pedestrian counter>” on console
# If the current stage is 6
# Set the traffic stage to 1
# Display “Commencing Traffic Stage <traffic stage>” on console
# set  pedestrian counter to 0

def normal_operation(intersectionData,changeableConditions):
    """
    normal opperation mode
    """
#TODO add function header
    # Begin normal operation\
    mode = 'c'
    to_7_segment_display(board, mode)
    # Initialize traffic stage to 1
    changeableConditions["trafficStage"] = 1

    # Initialize pedestrian count to 0
    pedCount = 0

    try:
        while True:    
            # Initialize stage start time current time
            stageStart = time.time()
            stageEndTime = time.time() + 30

            # Run function polling loop, inputting polling rate, output of polling time, current distance and pedestrian count
            [intersectionData, changeableConditions] = polling_loop(intersectionData, changeableConditions)
                #Happens within function 
                    #If polling start time plus polling time taken equals the current time
                    # Display polling time on console, “Polling loop took <polling time> to complete”
                    # If polling start time plus polling time taken equals the current time
                    # Display the current distance, “The distance to the closest vehicle is <current distance> cm.”
            # Does the traffic stage need changing?
            
            # if stage matches ‘1’ and current time minus stage start time is less than or equal to 30 seconds
            if changeableConditions["trafficStage"] == 1 and time.time()<stageEndTime:
                pass
            # if stage matches ‘1’ and current time minus stage start time is more than 30 seconds
            elif changeableConditions["trafficStage"] == 1 and time.time()>=stageEndTime:
                trafficStageChange(changeableConditions["trafficStage"])
            # traffic stage change inputting traffic stage, output is updated traffic stage
            # Continue to step 9
            elif changeableConditions["trafficStage"] == {2,3,4,5,6} and time.time()<stageEndTime:
                pass
            # if stage matches ‘1’ and current time minus stage start time is more than 30 seconds
            elif changeableConditions["trafficStage"] == 1 and time.time()>=stageEndTime:
                trafficStageChange(changeableConditions["trafficStage"])
            # if stage matches ‘2’ and current time minus stage start time is less than or equal to 3 seconds
            # Continue to step 9
            # if stage matches ‘2’ and current time minus stage start time is more than 3 seconds
            # traffic stage change inputting traffic stage, output is updated traffic stage
            # Continue to step 9
            # if stage matches ‘3’ and current time minus stage start time is less than or equal to 3 seconds
            # Continue to step 9
            # if stage matches ‘3’ and current time minus stage start time is more than 3 seconds
            # traffic stage change inputting traffic stage, output is updated traffic stage
            # Continue to step 9
            # if stage matches ‘4’ and current time minus stage start time is less than or equal to 30 seconds
            # Continue to step 9
            # if stage matches ‘4’ and current time minus stage start time is more than 30 seconds
            # traffic stage change inputting traffic stage, output is updated traffic stage
            # Continue to step 9
            # if stage matches ‘5’ and current time minus stage start time is less than or equal to 3 seconds
            # Continue to step 9
            # if stage matches ‘5’ and current time minus stage start time is more than 3 seconds
            # traffic stage change inputting traffic stage, output is updated traffic stage
            # Continue to step 9
            # if stage matches ‘6’ and current time minus stage start time is less than or equal to 3 seconds
            # Continue to step 9
            # if stage matches ‘6’ and current time minus stage start time is more than 3 seconds
            # traffic stage change inputting traffic stage, output is updated traffic stage
            # Continue to step 9
        # light state for stage, input; current stage, output; main light state, side light state, pedestrian light state
        # Light set state to led state input;  main light state side light state, pedestrian light state, output; main red, main yellow, main green, side red, side yellow, side green, pedestrian red, pedestrian green
        # Output light states to Arduino
        # Has the exit button been pressed?
        # If yes, return to main menu, step 3 of ‘Opening and Mode Selection’
        # If no, continue to step 5


#Create a dictonary of records
if __name__ == "__main__":     
    intersectionData = {"timeRecord":[], "distToVehicleRecord":[], "pedCountRecord":[], "pedCounterReset":""}

    pollingRate = 2
    changeableConditions = {
        'arduinoPins' : {
            "mainRed": 2,
            "mainYellow": 3,
            "mainGreen": 4,
            "sideRed": 5,
            "sideYellow": 6,
            "sideGreen": 7,
            "pedestrianRed": 8,
            "pedestrianGreen": 9,
            "triggerPin":0,
            "echoPin":1
            },
        'ardinoPins7seg': [],
        'trafficStage' : 1, # in the led state we need a case switching so we can assign the correct R,Y,G states from traffic stage, not neccercarily, was originally designed to have individual states entered within function call
        'pollingRate' : pollingRate,
        'pedCounterReset' : ""
    }