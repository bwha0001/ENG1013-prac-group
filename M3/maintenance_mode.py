#Maintenacence Mode for Traffic Control System
#Author: Caitlin Macdonald
#Last Edit: 24 April 2024
#Version: 2 - Hardware tested

import to_7_segment_display as to_7_seg
import time

def maintenance_mode(board, board2, intersectionData, changeableConditions):
    '''
    Maintenance mode allows the user, with the correct PIN to edit conditons and reaction for the intersection
    Args:
        board: Arduino Set Up
        board2: 2nd Arduino Set Up
        intersectionData (dictonary): Data collected about the interesection
        changeableConditions (dictonary): Anything related to the system that changes
    User Inputs: 
        pin, condition to edit, new condition value
    Returns: 
        intersectionData (dictonary): Data collected about the interesection
        changeableConditions (dictonary): Anything related to the system that changes
    '''
    
    try:
        #Check if locked out
        lockOutTime = changeableConditions['lockOutTime']
        if time.time() < lockOutTime:
            print(f"You are locked out. Wait {round(lockOutTime-time.time()/60, 2)} mins till you can enter maintenance mode.")
            return
        to_7_seg.sevenSeg(board2, 'c')
        #Initalisations, what is avaible to change, what acceptable values are
        changesCodes = {"PLR":"polling rate"}
        changesRules = {"PLR":{1, 2, 3, 4 ,5}}
        changesToVaribles = {"PLR":"pollingRate"}
        #Suspend polling loop, set mode infomation
        changeableConditions["trafficStage"] = "suspended"
        
        #PIN - Checks if pin matches stored. If matches enter maintenance mode, if it doesnt match determine whether the user has any more attempts avaible to them
        pin = "1234"
        triesAllowed = 3
        attemptsMade = 0
        for i in range(0,triesAllowed):
            pinInput = input("Enter the PIN:")
            if pinInput == pin:
                accessEndTime = time.time() + changeableConditions["accessTime"]
                print("Password Correct, entering maintenance mode")
                #Set access time to accessTime from current time, this resets every time enter maintence mode
                accessTime = changeableConditions["accessTime"]
                accessEndTime = time.time() + accessTime
                break
            elif 2-i > 0 and not pinInput == pin:
                print(f"PIN incorrect, {2-i} tries remaining")
                attemptsMade += 1
            elif 2-i== 0 and not pinInput == pin:
                print("PIN incorrect, no attempts remaining. \n You have been locked out of maintenance mode for 2 minites, returing to main menu.")
                changeableConditions['lockOutTime'] = time.time() + changeableConditions['lockOutLength']
                return None
        
        while time.time()<=accessEndTime:
            #Choose option to edit
            print(f"Enter of the the following to codes to change associated condition:\n {changesCodes}")
            optionCode  = input("Enter Condition to edit:")
            if optionCode in changesCodes.keys():
                #Change option
                while True:
                    changeToConditon = input(f"Enter alternation to {changesCodes[optionCode]}:")
                    try:
                        if int(changeToConditon) in changesRules[optionCode]:
                            changeableConditions[changesToVaribles[optionCode]] = int(changeToConditon)
                            to_7_seg.sevenSeg(board2, 'c', int(changeToConditon))
                            pass
                        else:
                            invalidChangeMessage = f"Change requested to {changesCodes[optionCode]} not avalible. Acceptable changes are to {changesRules[optionCode]}"
                            print(invalidChangeMessage)
                    except ValueError:
                        print(invalidChangeMessage)
            else:
                print(f"Input does not match change code.\n The codes and their changes are as follows:\n {changesCodes}\n")
                #Restart loop
                continue

            #Change another conditon?
            while True:        
                contInput = input("Would you like to continue making changes to conditions? (Y/N): ")
                if contInput in {"Y","N"}:
                    break
                else:
                    print("Invalid Input, input 'Y' to make more changes or 'N' to return to exit")
            #Determine whether to repeat asking process
            if contInput == "Y":
                continue
            elif contInput == "N":
                return intersectionData, changeableConditions
        
        #This line accessed if access time over
        #Double check time passed
        if time.time()>accessEndTime:
            print(changeableConditions["accessTime"])
            #print(f"Access Timed Out, after {changeableConditions["accessTime"]} mins of access.")
            return intersectionData, changeableConditions
        
    except KeyboardInterrupt:
        #exit button activation
        print("Exit button activated, returning to main menu")
        return intersectionData, changeableConditions
    


# if __name__ == "__main__":
#     global changeableConditions
#     changeableConditions = {
#         "trafficStage" : 1,
#         "pollingRate" : 2, 
#         "pedCounterReset":""}
    
#     maintenance_mode()