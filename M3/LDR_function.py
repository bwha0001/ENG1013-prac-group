import math as mth

# using threshold value of 6k from Hayley's "calibration"
def ldr(myBoard, changeableConditions):
    tempPin = changeableConditions["arduinoPins"]["ldrPin"]

    voltage, time = myBoard.analog_read(tempPin)

    if voltage>changeableConditions["dayNightTrigger"]:
        return "night"
    else:
        return "day"