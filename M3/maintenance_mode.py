#Maintenacence Mode for Traffic Control System
#Author: Caitlin Macdonald
#Last Edit: 24 April 2024
#Version: 2 - Hardware tested

import to_7_segment_display as to_7_seg
import time
import time_conversion as tc


#TODO update overheight availible values to be used
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
            #find how long remaining in lockout, in mins and seconds
            lockOutMin, lockOutSec = tc.time_conversion(lockOutTime-time.time(), "sec")
            #print message about how much time remaining to console
            print(f"You are locked out. {lockOutMin} mins and {lockOutSec} seconds till maintenance mode can be accessesed.")
            return
        to_7_seg.sevenSeg(board2, 'c')

        changeToCondition = 0 # initialise changeToCondition which is updated in 95
        #Initalisations, what is avaible to change, what acceptable values are
        changesCodes = {"PLR":"polling rate",
                        "OHH": "Over head height", 
                        "ETC" : "Extension time for car",
                        "ETT":"Distance for nearest vechile to extend yellow",
                        "PLT": "Plot length time"}

        changesToVaribles = {"PLR":"pollingRate",
                             "OHH": "overHeight",
                             "ETC":"extensionTime",
                             "ETT":"extensionTrigger",
                             "PLT": "plotLength"} # orange light needs to hold longer
        
        OHHAllowableValues = [int(d) for d in range(1,10,1)] # minimum overHeight closness is 1cm and max is 10cm 
        ETCAlloableValues = [3,4,5,6,7,8]
        PLTAllowableValues = [int(d) for d in range(20,80,10)]
        
        
        changesRules = {"PLR": [1, 2, 3, 4 ,5],
                        "OHH": OHHAllowableValues,
                        "ETC": ETCAlloableValues,
                        "PLT": PLTAllowableValues
                        }
        #Suspend polling loop, set mode infomation
        changeableConditions["trafficStage"] = "suspended"
        
        #PIN - Checks if pin matches stored. If matches enter maintenance mode, if it doesnt match determine whether the user has any more attempts avaible to them
        pin = "1234"
        triesAllowed = 3
        attemptsMade = 0
        for i in range(0,triesAllowed):
            pinInput = input("\n\n\nEnter the PIN:")
            if pinInput == pin:
                accessEndTime = time.time() + changeableConditions["accessTime"]
                print("\n\nPassword Correct, entering maintenance mode")
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

        #Initalise varible for option changing to be saved in, initalise as empty string to say it can be overwritten
        optionCode = ""


        #make changes
        #things that can can be changed

        #1. time held for plotting
        #2. extenstion time if car is close
        #3. overheight height
        
        while time.time()<=accessEndTime:
            #Check if a new input should be asked for
            if optionCode == '':
                #Choose option to edit
                print(f"Enter of the the following to codes to change associated condition:\n ")
                keys = list(changesCodes.keys())
                values = list(changesCodes.values())
                for i in range(0,len(changesCodes)):
                    print(f"{keys[i]} for {values[i]}\n")
                optionCode  = input("Enter Condition to edit: ").upper()

            # #Check that option to edit is valid
            # if optionCode in changesCodes.keys():
            #     #If valid input changeCode remains saved
            #     pass
            if optionCode not in changesCodes.keys():
                print(f"Input does not match change code.\n")
                #Do not save optionCode entered by user overwritten to condition of optionCode being an asked for ie. empty string\
                optionCode = ''
                #Restarts loop
                continue

            #Change option
            changeToConditon = input(f"Enter alternation to {changesCodes[optionCode]}:").upper()
            try:
                if int(changeToConditon) in changesRules[optionCode]:
                    changeableConditions[changesToVaribles[optionCode]] = int(changeToConditon) #updates dictionary with new value
                    #Confirms that chnage was made
                    conditionChanged = 1 
                    to_7_seg.sevenSeg(board2, 'c', int(changeToConditon))
                    optionCode = ""
                else:
                    if changesCodes[optionCode] == 'OHH':
                        invalidChangeMessage = f"Change requested to {changesCodes[optionCode]} not avalible. Acceptable changes are to between 5 to 60cm" # just to stop printing out a masive list
                        print(invalidChangeMessage)
                    else:
                        invalidChangeMessage = f"Change requested to {changesCodes[optionCode]} not avalible. Acceptable changes are to {changesRules[optionCode]}"
                        print(invalidChangeMessage)
                    #Restart loop
                    continue
            except ValueError:
                print(invalidChangeMessage)
                continue

### TODO ### Get rid of while loops that won't trigger timeout
            contInput = ""
            #Change another conditon? given time out not occoured
            while time.time()<= accessEndTime:
                #Ask if want to continue to make changes or quit
                contInput = input("Would you like to continue making changes to conditions? (Y/N): ").upper()
                if contInput in {"Y","N"}:
                    break
                else:
                    print("Invalid Input, input 'Y' to make more changes or 'N' to return to exit")

            #Determine whether to repeat asking process
            if contInput == "Y":
                continue
            elif contInput == "N":
                return intersectionData, changeableConditions
        
        #This line accessed if access time over and loop is broken
        #Double check time passed
        if time.time()>accessEndTime:
            #Print time out message
            print(f"Access Timed Out, after {round(changeableConditions['accessTime']/60,2)} mins of access.")
            return intersectionData, changeableConditions
        
    except KeyboardInterrupt:
        #exit button activation
        print("\n\nExit button activated, returning to main menu\n\n\n\n")
        return intersectionData, changeableConditions
    


# if __name__ == "__main__":
#     global changeableConditions
#     changeableConditions = {
#         "trafficStage" : 1,
#         "pollingRate" : 2, 
#         "pedCounterReset":""}
    
#     maintenance_mode()