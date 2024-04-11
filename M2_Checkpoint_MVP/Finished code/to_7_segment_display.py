import time
import math as mth
# from pymata4 import pymata4 
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

        str(message) # convert any data type into string to take length
           
        if(len(message)<length):
            # print('valid')
            return 'valid', message
                
        elif len(message)>=length:
            print("ensure input is d or c or n or g, or less then 3 digit number")
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
        '0' : '1111110', 
        '1' : '0000110',
        '2' : '1101101',
        '3' : '1111001',
        '4' : '0110011',
        '5' : '1011011',
        '6' : '0011111',
        '7' : '1110000',
        '8' : '1111111',
        '9' : '1111011',
        'a' : '1110110',
        'n' : '0010101',
        'm' : '0001101',
        'd' : '0111101', 
        'c' : '0001101',
        'g' : '1011111'
    }

    key = value
    sevSegKey = dictionary[key] 
    return sevSegKey
    
def sevenSeg(mode : str, pedCounter = 0):
    """sevenSeg outputs the value of the pedestrian counter across the first three digits
        and the operating mode in the 4th digit.
        It could be updated easily so that any value edited in the maintenance mode is displayed on the 7 seg

    Args:
        mode (str): determine whether 'd'(data obs), 'c'(maintenance mode), 'n' (normal operating) or just 'g' (general) message to display
        pedCounter (int): number to be displayed, defaults to 0
    """
    validated1, message1 = valid_7seg(mode) # validate operating mode input
    

    #Determine first digit output
    if validated1 == 'valid' :
        # converting the pedestrian counter to the LED displays
        #digitNum is the corresponding segments from 1-3 and contains the string to be converted to integer list to be output to digital outputs
        listMessage = [str(d) for d in str(pedCounter)] 
        digitNum = [0,0,0]
        for i in range(0,len(listMessage)):
            digitNum[i] = convertion_dict(listMessage[i])

        # digit 4 dispays the state of operation
        if message1 == 'd' :
            dig4 = convertion_dict('d')
            # actual code will need to split up seg into individual integers and output 
            #them as low or high using a for loop

        if message1 == 'c' :
            dig4 = convertion_dict('c')
            print(f"dig4 :{dig4}, dig 3 : {digitNum[0]}, dig 2 : {digitNum[1]}, dig 3 : {digitNum[2]}")
            
        if message1 == 'n':
            dig4 = convertion_dict('n')
        print(f"dig4 :{dig4}, dig 3 : {digitNum[0]}, dig 2 : {digitNum[1]}, dig 3 : {digitNum[2]}")            
        if message1 == 'g':
            dig4 = convertion_dict('g')
            print(f"dig4 :{dig4}, dig 3 : {digitNum[0]}, dig 2 : {digitNum[1]}, dig 3  {digitNum[2]}")   
    else:
        print(' invalid input')

    return dig4, digitNum         


if __name__ == "__main__":

    # board = pymata4.Pymata4() TODO
    #tries to find polling data infomation
    # try:
    #     intersectionData
    # except NameError:
    #     intersectionData = {"timeRecord":[], "distToVehicleRecord":[], "pedCountRecord":[], "pedCounterReset":""}

    # Pin assignments for 7 seg display
    # pin on 7 seg +2 = pin on arduino
    segE = 1+2
    segD = 2+2
    DP = 3+2
    segC = 4+2
    segG = 5+2
    dig4 = 6+2
    segB = 7+2
    dig3 = 8+2
    dig2 = 9+2
    segF = 10+2
    segA = 11+2
    dig1 = 12+2
    segments = [segA, segB,segC,segD,segE,segG]
    digits = [dig4,dig3,dig2,dig1]

    # message = 4455
    # validated, listMessage = valid_7seg(message)
    # if  validated != 'valid':
    #     print("nope terminate")
    #     # break
    # print(f"returns from valid {valid_7seg(message)}")
    # value = valid_7seg('c')
    # print(value)

    [dig4, digitNum] = sevenSeg('c', 345)
    # print(f"dig4 :{dig4}, dig 3 2 1 : {digitNum}")
    
    
    # now we want to start messing with the LEDs
    # board.shutdown()


    

