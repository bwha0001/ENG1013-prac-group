# # translates the temperature from voltage to temperature.

# # Double check formulas, rearanged values from
# # thermistor reference
# import math as mth

# #voltage divider with a 1k resistor
# # def thermistor_resistance(resistance, voltage):
# #     thermRes = resistance * (voltage / (5.0 - voltage))
# #     return thermRes

# def temperature(thermRes):
#     if thermRes>4.59:
#         #need to check constants
#         #tempCelcius = -21.21*mth.log((0.0331335)*(-100+100/tempVoltage))
#         tempCelcius = -21.21 * mth.log(thermRes) + 72.203
#     elif thermRes<=4.59:
#         #tempCelcius = -7.015*mth.log((0.00284784)*(-100+500/tempVoltage))
#         tempCelcius = -7.071 * mth.log(thermRes) + 41.128
#     return tempCelcius

# def temp_read(board, changeableConditions, intersectionData):
#     """
#     Takes reading from themistor and hence calculates temprature
#     Args:
#         board: Arduino Set Up
#         intersectionData (dictonary): Data collected about the interesection
#         changeableConditions (dictonary): Anything related to the system that changes

#     Returns:
#         tempCelcius(interger/float?): temprature mesured as per themistor
#     """
#     voltage = board.analog_read(changeableConditions["arduinoPins"]["temperaturePin"])
#     # thermRes = thermistor_resistance(resistance, voltage)
#     #TODO which resistance is this refering to, the other resistor in tbe circut not LDR?
#     # tempCelcius = temperature(thermRes)
#     return tempCelcius


import math as mth

def temp_calculation(voltage):
    #insert code
    # resistance = ((5 *100)/voltage) -100 # fix this in a second
    resistance = -10*voltage/(-5+voltage)
    temperature = -21.21*mth.log(resistance)+72.203
    # eqn1 = -7.017*mth.log(resistance) + 41.128
    # eqn2 = -21.21*mth.log(resistance) + 72.203
    # if voltage>2.14: # arbitary value     
    # #     temperature = eqn1
    # # else:
    # #     temperature = eqn2
    return temperature


def temperature(myBoard, changeableConditions):
    tempPin = changeableConditions["arduinoPins"]["temperaturePin"]
    voltage, time = myBoard.analog_read(tempPin)
    trueVoltage =  0.0049 * voltage
    temp = temp_calculation(trueVoltage)
    print(f"debugging purposes, temperature is: {temp}")
    return temp
    

