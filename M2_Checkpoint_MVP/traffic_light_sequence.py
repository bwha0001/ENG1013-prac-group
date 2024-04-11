import time
from pymata4 import pymata4
def traffic_light_sequence():
    trafficStage = []

    stage1 = {
            'mainRoad': "green",
            'sideRoad': "red",
            'pedestrianLights': 'red'
        }

    stage2 = {
            'mainRoad': "yellow",
            'sideRoad': "red",
            'pedestrianLights': 'red'
        }

    stage3 = {
            'mainRoad': "red",
            'sideRoad': "red",
            'pedestrianLights': 'red'
        }

    stage4 = {
            'mainRoad': "red",
            'sideRoad': "green",
            'pedestrianLights': 'green'
        }

    stage5 = {
            'mainRoad': "red",
            'sideRoad': "yellow",
            'pedestrianLights': 'flashing green' #flashing at 2-3 Hz
        }

    stage6 = {
            'mainRoad': "red",
            'sideRoad': "red",
            'pedestrianLights': 'red'
        }


    while True:
        trafficStage.append('stage1')
        if 'stage1' in trafficStage:
            print('Current stage: stage 1')
            print(f" {stage1}")
            time.sleep(30)
        trafficStage.pop(0)
        trafficStage.append('stage2')
        return trafficStage
        

        if 'stage2' in trafficStage:
            print('Current stage: stage 2')
            print(f" {stage2}")
            time.sleep(3)
        trafficStage.pop(0)
        trafficStage.append('stage3')
        return trafficStage


        if 'stage3' in trafficStage:
            print('Current stage: stage 3')
            print(f" {stage3}")
            time.sleep(3)
        trafficStage.pop(0)
        trafficStage.append('stage4')
        return trafficStage


        if 'stage4' in trafficStage:
            print('Current stage: stage 4')
            print(f"{stage4}")
            time.sleep(30)
        trafficStage.pop(0)
        trafficStage.append('stage5')
        return trafficStage


        if 'stage5' in trafficStage:
            print('Current stage: stage 5')
            print(f"{stage5}")
            time.sleep(3)
        trafficStage.pop(0)
        trafficStage.append('stage6')
        return trafficStage


        if 'stage6' in trafficStage:
            print('Current stage: stage 6')
            print(f"{stage6}")
            time.sleep(3)
        trafficStage.pop(0)
        trafficStage.append('stage1')
        return trafficStage
    
    
##figure out how to use the time module for having the colours 'print' for the correct amount of time 
##need to figure out how to conect the colour name to the LEDs in reality (and how to do the FLASHING)
##i think it needs to go into a while loop so that it can continue to run... might need more if statements?
##do i need to import pymata4? probably...