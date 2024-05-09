# translates the temperature from voltage to temperature.

# Double check formulas, rearanged values from
# thermistor reference
import math as mth

#voltage divider with a 1k resistor
def thermistor_resistance(resistance, voltage):
    thermRes = resistance * (voltage / (5.0 - voltage))
    return thermRes

def temperature(thermRes):
    if thermRes>4.59:
        #need to check constants
        #tempCelcius = -21.21*mth.log((0.0331335)*(-100+100/tempVoltage))
        tempCelcius = -21.21 * mth.log(thermRes) + 72.203
    elif thermRes<=4.59:
        #tempCelcius = -7.015*mth.log((0.00284784)*(-100+500/tempVoltage))
        tempCelcius = -7.071 * mth.log(thermRes) + 41.128
    return tempCelcius

def temp_read(board, changeableConditions, intersectionData):
    #TODO analog read then other function calls
    voltage = board.analog_read(changeableConditions["arduinoPins"]["temperaturePin"])
    thermRes = thermistor_resistance(resistance, voltage)
    #TODO which resistance is this refering to, the other resistor in tbe circut not LDR?
    tempCelcius = temperature(thermRes)
    intersectionData['temperatureRecord'].append(tempCelcius)
    return tempCelcius