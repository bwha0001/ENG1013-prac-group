#Author: Team F12
#Version: 2
#Last Edit: 10 April 2024
#Purpose: Maintenacence Mode

def maintenece_mode():
    '''
    Purpose: Maintenace mode allows the user, with the correct PIN to edit conditons and reaction for the intersection
    Inputs: Direct to function none, user will be prompted for Pin, Condition to edit and new condition 
    Outputs: Alters conditions dictonary
    '''
    try:
        #Initalisations, what is avaible to change, what acceptable values are
        changesCodes = {"PLR":"polling rate"}
        changesRules = {"PLR":{1, 2, 3, 4 ,5}}
        changesToVaribles = {"PLR":"pollingRate"}
        #Suspend polling loop, set mode infomation
        changeableConditions["trafficStage"] = "suspended"
        mode = "c."
        #PIN - Checks if pin matches stored. If matches enter maintence mode, if it doesnt match determine whether the user has any more attempts avaible to them
        pin = "1234"
        triesAllowed = 3
        attemptsMade = 0
        for i in range(0,triesAllowed):
            pinInput = input("Enter the PIN:")
            if pinInput == pin: 
                print("Password Correct, entering maintenace mode")
                break
            elif 2-i > 0 and not pinInput == pin:
                print(f"PIN incorrect, {2-i} tries remaining")
            elif 2-i== 0 and not pinInput == pin:
                print("PIN incorrect, no attempts remaining, returing to main menu")
                return None

        #As properly entered mode now change 7 segment display
#Commented out for testing TODO        to_7_segment_display(mode)
        
        while True:
            while True:
                #Choose option to edit
                optionCode  = input("Enter Condition to edit:")
                if optionCode in changesCodes.keys():
                    #Change option
                    while True:
                        changeToConditon = input(f"Enter alternation to {changesCodes[optionCode]}:")
                        if int(changeToConditon) in changesRules[optionCode]:
                            changeableConditions[changesToVaribles[optionCode]] = changeToConditon
                            break
                        else:
                            print(f"Change requested to {changesCodes[optionCode]} not avalible. Acceptable changes are to {changesRules[optionCode]}")
                    break
                else:
                    print(f"Input does not match change code.\n The codes and their changes are as follows:\n {changesCodes}")
            #Change another conditon?
            while True:        
                contInput = input("Would you like to contunie making changes to conditions? (Y/N): ")
                if contInput in {"Y","N"}:
                    break
                else:
                    print("Invalid Input, input 'Y' to make more changes or 'N' to return to exit")
            #Determine whether to repeat asking process
            if contInput == "Y":
                pass
            elif contInput == "N":
                break    
    except KeyboardInterrupt:
        #exit button activation
        print("Exit button activated, returning to main menu")
        return
    
if __name__ == "__main__":
    changeableConditions= {"trafficStage":"stage2", "pollingRate":2}
    maintenece_mode()