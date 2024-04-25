#Main Menu of Traffic Control System
#Authors: Jenny
#Version: 5 - Hardware Implementation
#Last Edit: 22 April 2024

import normal_operation as n_o
import maintenance_mode as m_m
import data_observation_mode as DOM
import led_state as led

def main_menu(board, board2, intersectionData, changeableConditions):
    """ 
    Used to select a mode and to quit the program       
        
    Args:
        board: Arduino Set Up
        board2: 2nd Arduino Set Up
        intersectionData (dictonary): Data collected about the interesection
        changeableConditions (dictonary): Anything related to the system that changes
    Returns: 
        None
    """   

    while True:
        while True:  
            #modeSelection = ""
            #Set all LED's to off
            led.light_setting_state(board, changeableConditions, "off", "off", "off")
            modeSelection = input("Modes:\n 1 - Data Observation.\n 2 - Normal Operation Mode\n 3 - Maintenance Mode\n Select Mode (1,2,3): ")
            try: 
                if modeSelection == "1":
                    print("Entering Data Observation Mode...")
                    DOM.data_observation_mode(board, board2, intersectionData, changeableConditions)
                    print("\n\nCurrently in Main Menu")
                    break
                elif modeSelection == "2": 
                    print("Entering Normal Operation Mode...")
                    n_o.normal_operation(board, board2, intersectionData, changeableConditions)
                    print("\n\nCurrently in Main Menu")
                    break
                elif modeSelection == "3":
                    print("Entering Maintenance Mode...")
                    m_m.maintenance_mode(board, board2, intersectionData, changeableConditions)
                    print("\n\nCurrently in Main Menu")
                    break
                else:
                    print("Invalid Mode Input. Re-enter mode option.")
            except KeyboardInterrupt: 
                break
                
        while True:
            programQuit = input("Would you like to quit the program? (Y/N) ")
            if programQuit == "N" or programQuit == 'n': 
                break 
            elif programQuit == "Y" or programQuit == 'y':
                print("Closing program...")
                break
            else:
                print("Invalid Input. Options available as 'Y' to continue to main menu and 'N' to end program.") 
        
        if programQuit == "N":
            pass
        elif programQuit == "Y":
            return
                
                


# # Running program
# if __name__ == "__main__":
#     pollingRate = 2
#     trafficStage = 1
#     print("working")
#     main_menu()