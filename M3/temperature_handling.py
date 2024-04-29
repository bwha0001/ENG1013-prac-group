# translates the temperature from voltage to temperature.

# Double check formulas, rearanged values from
# https://learning.monash.edu/course/view.php?id=7529&section=5
# thermistor reference
import math as mth
def temperature(tempVoltage):
    if tempVoltage>4.59:
        resistance = -21.21*mth.log((0.0331335)*(-100+100/tempVoltage))
    if tempVoltage<=4.59:
        temperature = -7.015*mth.log((0.00284784)*(-100+500/tempVoltage))

    # Hayley, sorry I got side tracked with the voltage. If you do a voltage dividor with a 1k resistor
    # before the thermistor and take voltage across thermistor the formul
    return temperature