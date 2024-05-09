import math as mth

# using threshold value of 6k from Hayley's "calibration"
def LDR(myBoard, changeableConditions):
    tempPin = changeableConditions["arduinoPins"]["ldrPin"]

    voltage, time = myBoard.analog_read(tempPin)

    if voltage>2.72:
        return "night"
    else:
        return "day"