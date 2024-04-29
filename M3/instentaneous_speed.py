#instaneous speed
import plotting_function
import matplotlib.pyplot as plt

def velocity(point1, point2, time1, time2):
    speed = (point2-point1)/(time2-time1)
    return speed