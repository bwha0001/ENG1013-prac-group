# translates the temperature from voltage to temperature.

# Double check formulas, rearanged values from
# thermistor reference
import math as mth

#voltage dividor with a 1k resistor to find voltage 
def thermistor_resistance(thermRes, voltIn):
    fixedRes = 1000
    tempVoltage = voltIn * (fixedRes/(thermRes+fixedRes)) 
    return tempVoltage

def temperature(tempVoltage):
    if tempVoltage>4.59:
        #need to check constants
        tempCelcius = -21.21*mth.log((0.0331335)*(-100+100/tempVoltage))
    if tempVoltage<=4.59:
        tempCelcius = -7.015*mth.log((0.00284784)*(-100+500/tempVoltage))

    return tempCelcius
