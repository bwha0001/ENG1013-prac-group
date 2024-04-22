import time
import math as mth
from pymata4 import pymata4 
import module_scripts as ms




# controling digits, ground needs to turn on/off
# controlling segments, power needs to turn on/off
#e.g digit 1 segment A needs GND 1, disconnect 2,3,4 and power seg A, rest low

# psuedocode
    #1. validating word is 4 charecters
def valid_7seg(message: any):
    """validates the message input can be displayed by the 7 segment display

    Args:
        message (any): message to be displayed

    Returns:
        'invalid': returns string 'invalid' which is used to determine if the output is correct
        message (str) : returns the input as a string which is then split up in sevenSeg to be displayed
    """
    #ensure the input a value that can be converted into a list
    try: 
        if type(message) == type('kjdfbkdfb'): # recognise input is a string
            length = 2
        elif type(message) == type(555): #regocnise input is an integer
            length = 3
        else:
            return 'invalid', message

        message = str(message) # convert any data type into string to take length
           
        if(len(message)<length):
            # print('valid')
            return 'valid', message
                
        elif len(message)>=length:
            print("Ensure input is d or c or n or g, or less then 3 digit number")
            return 'invalid', message
        else:
            print("how did you get here")
            return 'invalid', message
    except ValueError:
        print('insert a string')
        

    #converting the float into individual numbers
    

def convertion_dict(value: str):
    """convertes number and selected letters (a,n,m,d,g,c) as their seven segment equivelents

    Args:
        value (str): values 1-9 and letters a,n,m,d,g,c

    Returns:
        sevSegKey (str): The seven segment equivelent of the input
    """
    # ms.Validate(value, 'p') # class type validation to ensure input is string
    dictionary = {
        '0' : '11111100', 
        '1' : '00001100',
        '2' : '11011010',
        '3' : '11110010',
        '4' : '01101110',
        '5' : '10110110',
        '6' : '00111110',
        '7' : '11100000',
        '8' : '11111110',
        '9' : '11110110',
        'a' : '11101100',
        'n' : '00101010',
        'm' : '00011010',
        'd' : '01111010', 
        'c' : '00011010',
        'g' : '10111110', 
        '.' : '00000001',
        'n.' : '00101011',
        'm.' : '00011011',
        'd.' : '01111011', 
        'c.' : '00011011',
        'g.' : '10111111', 
    }

    key = value
    sevSegKey = dictionary[key] 
    return sevSegKey

def convert_to_three_digits(number):
    # Using string formatting to ensure the number is represented with leading zeros
    # number returns as decimal
    return '{:03d}'.format(number)




def to_arduino(myBoard, digDisplay, mode, number):
    
    segA = 2
    segB = 3
    segC = 4 
    segD = 5
    segE = 6
    segF = 7
    segG = 8
    segDP = 9
    digGround = [11,12,13, 10 ]#dig 0 ... dig 4 
    segmentID = [segA, segB, segC, segD, segE, segF, segG, segDP]
    # digDisplay = digDisplay[::-1] # reverse the digits cause i messed up
    # digGround = digGround[::-1]


    wakeTime = 3
    # board.set_pin_mode_digital_output(segF)
    for pin in digGround:
        myBoard.set_pin_mode_digital_output(pin)
    for pin in segmentID:
        myBoard.set_pin_mode_digital_output(pin)
    # myBoard.set_pin_mode_digital_output()
    # set digit that is desired to be grounded
    #turning off all digits
    for i in range(0,len(digGround)):
        myBoard.digital_write(digGround[i], 1)

    if number != '000':
        time1 = time.time()
        time2 = time.time()
        while mth.floor(time2)-mth.floor(time1)<=wakeTime: #Keep LEDs on for wakeTime seconds
            #INTIALISING to digit 0
            myBoard.digital_write(digGround[0], 0)
            #printing to the pins
            for i in range(0,len(digDisplay[0])):
                myBoard.digital_write(segmentID[i], int(digDisplay[0][i]))
            time.sleep(0.004)
            # clear pins
            for i in range(0,len(segmentID)):
                myBoard.digital_write(segmentID[i], 0)
            #turn off digit
            myBoard.digital_write(digGround[0],1)
            
            # INITIALISING digit 1
            myBoard.digital_write(digGround[1],0)
            #printing to the pins
            for i in range(0,len(digDisplay[1])):
                myBoard.digital_write(segmentID[i], int(digDisplay[1][i]))
            time.sleep(0.004)
            # clear pins
            for pin in segmentID:
                myBoard.digital_write(pin, 0)
            #turn off digit
            myBoard.digital_write(digGround[1],1)

            # INITIALISING digit 2
            myBoard.digital_write(digGround[2],0)
            #printing to the pins
            for i in range(0,len(digDisplay)):
                myBoard.digital_write(segmentID[i], int(digDisplay[2][i]))
            time.sleep(0.004)
            # clear pins
            for pin in segmentID:
                myBoard.digital_write(pin, 0)
            myBoard.digital_write(digGround[2],1)
            
            time2 = time.time() #update current time to update condition

    else: # writing operating mode status
        # INITIALISING digit 3
        myBoard.digital_write(digGround[3],0)
        #printing to the pins
        for i in range(0,len(digDisplay[3])):
            myBoard.digital_write(segmentID[i], int(digDisplay[3][i]))
        time.sleep(wakeTime)
        # clear pins
        for pin in segmentID:
            myBoard.digital_write(pin, 0)
        myBoard.digital_write(digGround[3],1)
    
    #Make sure pins turn off
    for i in range(0,len(digGround)):
        myBoard.digital_write(digGround[i], 1)
    print("Value sent to arduino without fail")



def sevenSeg(myBoard, mode : str, number = '000'):
    """IMPORTANT: if you want to display operating mode leave third input empty
        sevenSeg outputs either the mode or the current pedestrian counter value.
        Input '000' or leave ped counter blank to display mode and input a number as a string
        to print a number. There is failsafe inbuilt to make sure it works with integers but easier to just input it properly
        Display holds for wakeTime variable found in to_arduino function then dissapears 


    Args:
        myBoard: board = pymata4.pymata4()
        mode (str): determine whether 'd'(data obs), 'c'(maintenance mode), 'n' (normal operating) or just 'g' (general) message to display
        number (3 digit number)(str): number to be displayed, defaults to 0. e.g inputing 3 = '003'
    """

   
    validated1, message1 = valid_7seg(mode) # validate operating mode input\
    if type(number) is not type('jdf') or len(number)!= 2:  # converting any input to 3 digit string
        number = convert_to_three_digits(int(number))
        number = str(number)

    #Determine the output as strings
    if validated1 == 'valid' :
        # converting the pedestrian counter to the LED displays

        #digitNum is the corresponding segments from 1-3 and contains the string to be converted to integer list to be output to digital outputs
        listMessage = [str(d) for d in str(number)] # makes the all integers a string, so 555 = '5''5''5'
        digitNum = [0,0,0]
        for i in range(0,len(listMessage)):
            digitNum[i] = convertion_dict(listMessage[i]) # passes each number through conversion to get sevSeg equivelents

        # digit 4 dispays the state of operation
        if message1 == 'd' :
            dig4 = convertion_dict('d')
            # actual code will need to split up seg into individual integers and output 
            #them as low or high using a for loop

        if message1 == 'c' :
            dig4 = convertion_dict('c')
            # print(f"dig4 :{dig4}, dig 0 : {digitNum[0]}, dig 1 : {digitNum[1]}, dig 2 : {digitNum[2]}")
            
        if message1 == 'n':
            dig4 = convertion_dict('n')
        print(f"dig4 :{dig4}, dig 0 : {digitNum[0]}, dig 1 : {digitNum[1]}, dig 2 : {digitNum[2]}")            
        if message1 == 'g':
            dig4 = convertion_dict('g')
            # print(f"dig4 :{dig4}, dig 0 : {digitNum[0]}, dig 1 : {digitNum[1]}, dig 2 :  {digitNum[2]}")   

    # if message1 == 'c.' :
    #     dig4 = convertion_dict('c.')
    #     print(f"dig4 :{dig4}, dig 0 : {digitNum[0]}, dig 1 : {digitNum[1]}, dig 2 : {digitNum[2]}")
                
    # if message1 == 'n.':
    #     dig4 = convertion_dict('n.')
    #     print(f"dig4 :{dig4}, dig 0 : {digitNum[0]}, dig 1 : {digitNum[1]}, dig 2 : {digitNum[2]}")            
    # if message1 == 'g.':
    #     dig4 = convertion_dict('g.')
    #     print(f"dig4 :{dig4}, dig 0 : {digitNum[0]}, dig 1 : {digitNum[1]}, dig 2 :  {digitNum[2]}")   

        # seperating the segments from number digits
        # digits read right to left
        digit0 = [str(d) for d in str(digitNum[0])]
        digit1 = [str(d) for d in str(digitNum[1])]
        digit2 = [str(d) for d in str(digitNum[2])]
        digit3 = [str(d) for d in str(dig4)] # mode display digit
        digDisplay = [digit0, digit1, digit2, digit3]


    else:
        print('Invalid input')
    to_arduino(myBoard, digDisplay, mode, number)
    return digDisplay, mode, number         

# def outputSevSeg(myBoard, segments, segs, digs):
#     ms.arduino_setup(myBoard, 'digital write', [segs, digs])
#     for i in range(0,len(segments)):
#         for j in range(0,len(segments[i])):



if __name__ == "__main__": # need to initialise in a seperate file
    board = pymata4.Pymata4()
    sevenSeg(board, 'c', '123')
#     segE = 1+2
#     segD = 2+2
#     DP = 3+2
#     segC = 4+2
#     segG = 5+2
#     dig3 = 6+2
#     segB = 7+2
#     dig2 = 8+2
#     dig1 = 9+2
#     segF = 10+2
#     segA = 11+2
#     dig0 = 12+2
#     segs = [segA, segB,segC,segD,segE,segG, DP]
#     digs = [dig3,dig2,dig1, dig0]
#     board = pymata4.Pymata4
    


#     [dig4, digitNum, segments] = sevenSeg(board, 'c')



