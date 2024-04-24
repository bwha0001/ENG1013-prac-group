import time
import math as mth
#from pymata4 import pymata4 


def adder(a ,b):
    
    c = a + b
    return c


        

def Validate(list1 = [], list2= []):
    """tells you you inputs are the correct data type

    Args:
        list1 (list, each thing you want to validate): e.g int 5. Defaults to [].
        list2 (list, an example of each things data type): e.g int 100 will validate as correct as they are both integers. Defaults to [].
    """
    length1 = range(len(list1))
    length2 = range(len(list2))
    if(length1!=length2):
        print("list length is not the same")
        

    for i in length1:
        if(type(list1[i])!=type(list2[i])):
            print(f'value type in index {i} is not the same')
            
    
    print("function was run correctly, if no ouput above this then values are valid")            
        

def arduino_setup(myBoard, action:str,  wait: int, pin = []):
    """Speed set up of arduino including board set up and pin set ups

    Args:
        myBoard (pymata4.Pymata4): put board in here (in pymata description its "Self")
        action (str): enter "digital write" or "digital read" or 'analogue read'
        wait (int): wait time for digital write on and off
        pin (list, optional): enter a list of the pins that you want to be actioned. Defaults to [].

    Returns:
        list: pins that are analogue and digital read
    """
    myBoard = pymata4.Pymata4

    digiRead = []
    anaRead = []
    for i in pin:
        if(action == 'digital write'):
            # This will sequentially set each pin specified in the list to activate high, wait 
            # a specified time, then return to low
            # So if there is a known sequence of outputs
            myBoard.set_pin_mode_digital_output(pin[i])
            # myBoard.digital_pin_write(pin[i], 1)
            # time.sleep(wait)
            # myBoard.digital_pin_write(pin[i],0)

        if(action == 'digital read'):
            myBoard.set_pin_mode_digital_input(pin[i])
            digiRead.append(myBoard.digital_read(myBoard,pin[i]))
            

        if(action == 'analogue read'):
            myBoard.set_pin_mode_analog_input(pin[i])
            anaRead.append(myBoard.analog_read(myBoard, pin[i]))
            
            

    return digiRead, anaRead
# note this does not shut down the board, all pins should remain active

if __name__ == "__main__":
    from pymata4 import pymata4



    

        
            
