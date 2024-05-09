#instaneous speed
import plotting_function
import matplotlib.pyplot as plt

def velocity(point1, point2, time1, time2):
    if time1 or time2 or point1 or point2 == 0 or None:
        print("Ultrasonic sensors are diconnected")
        speed = 999 #error value
    else:
        speed = (point2-point1)/(time2-time1)
    return speed