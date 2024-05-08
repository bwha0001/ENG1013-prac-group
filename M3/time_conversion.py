#Convert time  in seconds or minuites to minuites and seconds
#Author: Caitlin Macdonald
#Last Edit: 5 May 2024
#Version: 1

def time_conversion(timeInput, inputUnit):
    """
    Convert from minuites or seconds to minuites and seconds
            
    Args:
        timeInput: time to convert
        inputUnit: "min" or "sec"
    
    Returns: 
        mins: convertion minutes term
        secs: convertion seconds term

    """    

    #Acceptable Units 
    inputUnits = ["min", "sec"]

    #Verify input is float, if no return error message
    try:
        time = float(timeInput)
    except ValueError:
        #print error message
        print(f"Input({timeInput}) to time conversion not valid. Input must be a number in an numerical data type or string.")
        return
    
    #Verify inputUnit
    if inputUnit in inputUnits:
        pass
    elif inputUnit not in inputUnits:
        print(f"Invalid input unit, the accepted units are: {inputUnits}")

    #Convert to minuites if required
    if inputUnit == "sec":
        #Divide by 60 and overwrite time
        time = time/60
    
    #extract minuites term, use interger conversion to drop decimal places and not round up
    min = int(time)

    #extract the remaining seconds, multuply by 60 to get seconds
    sec = round(time%1*60,2)

    #Export time on mins and seconds
    return min, sec