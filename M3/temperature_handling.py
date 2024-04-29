# translates the temperature from voltage to temperature.
import math as mth
def temperature(tempVoltage):
    if tempVoltage>26:
        temperature = -7.017*mth.log(tempVoltage) + 41.128
    if tempVoltage<=26:
        temperature = -21.21*mth.log(tempVoltage) + 72.203
    return temperature