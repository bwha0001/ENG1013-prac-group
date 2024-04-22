from pymata4 import pymata4
import numpy as np
import time
"""simplified version of my debounce from slc3. it uses polling loop so i dont think its appropriate
    for this project. But maybe it can be used to filter a callback function
"""
board = pymata4.pymata4()
button = 4
board.set_pin_mode_digital_input(button)

# define the maximum amount of levels
attemps = 0
maxLevels = 4
gameLength = 5
    
#generating a random sequence
while attemps<maxLevels:
    # this bit of code it just here to make the logic make sense
    try:
        rng = np.random.default_rng()
        sequence = rng.integers(low = 1, high = 4, size = gameLength) #creating random array for LED's
        print(sequence)
        for i in range(0,len(sequence)):
            board.digital_pin_write(sequence[i]+3,1)
            time.sleep(0.8)
            board.digital_pin_write(sequence[i]+3,0)
            time.sleep(0.8)
            #above is just getting a random array and pronting it to the led's, ignore it for debounce
 
    #polling rate
        pollingRate = 0.1
        Time = [time.time()]
        oldButtonStorage = [1,0,0,0,0,0]
        memory = []
        print("Begin")
        replay = True
        j=0

        while replay:
            #read in data
            buttonStorage = [board.digital_read(button)]
            TIME = buttonStorage[1]
            buttonStorage = buttonStorage[0] #pull out time from data
            # debounce condition, is the value of the button different to the old value of the button
            if(buttonStorage[0:gameLength] != oldButtonStorage[0:gameLength] and oldButtonStorage[0:gameLength] != [0,0,0,0,0]): #its array [0,0,]
                    # because it was for game, for us probs could leave it as just 0
                    
            memory.append(oldButtonStorage) #track value, we are going to filter out press and depress with memory variable
            # original time stamp
            Time.append(buttonStorage[5])

            oldButtonStorage = buttonStorage #update stored value    
            time.sleep(pollingRate)
            j+=1

            #filter out all zeros in storage array
            buttonValue = []
            for i in range(1,len(memory)): #skipping initialisation and origial null list
                for j in range(gameLength): #values not including time stamp
                    try: 
                        if len(buttonValue)>len(memory):
                            break
                        if memory[i][j]==1: #this condition here makes sure we have only 1's in the time stamp
                            buttonValue.append(j)
                    except KeyboardInterrupt :
                        break


board.shutdown()
