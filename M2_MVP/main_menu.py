import normal_operation as n_o
import maintenance_mode as m_m
import data_observation_mode as DOM

#Not current main menu - 

def main_menu(board, board2, intersectionData, changeableConditions):
    """ 
    Used to select a mode 
        Parameters: 
            modeSelection: data observation mode, normal operation mode, maintenance mode 
            programQuit: quits main menu (Yes/No)
        Returns: 
            Displays mode then quits or reselects mode
    """
    

    while True:
        while True:  
            modeSelection = ""
            modeSelection = input("Modes:\n 1 - Data Observation.\n 2 - Normal Operation Mode\n 3 - Maintenance Mode\n Select Mode (1,2,3): ")
            try: 
                if modeSelection == "1":
                    print("Entering Data Observation Mode...")
                    DOM.data_observation_mode(board, board2, intersectionData, changeableConditions)
                    break
                elif modeSelection == "2": 
                    print("Entering Normal Operation Mode...")
                    n_o.normal_operation(board, board2, intersectionData, changeableConditions)
                    break
                elif modeSelection == "3":
                    print("Entering Maintenance Mode...")
                    m_m.maintenance_mode(board, board2, intersectionData, changeableConditions)
                    break
                else:
                    print("Invalid Mode Input. Re-enter mode option.")
            except KeyboardInterrupt: 
                break
                
        while True:
            programQuit = input("Would you like to quit? (Y/N) ")
            try: 
                if programQuit == "N": 
                    break 
                elif programQuit == "Y":
                    print("Closing program...")
                    return None
            except ValueError: 
                print("Invalid Input. Options available as 'Y' to continue to main menu and 'N' to end program.")
                


# # Running program
# if __name__ == "__main__":
#     pollingRate = 2
#     trafficStage = 1
#     print("working")
#     main_menu()