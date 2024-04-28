#REDUNDANT -- updated normal operating mode and now uses traffic_state_change
#Traffic light sequence
#Authors: Hayley Dusting
#Version:  1
#Dates Edited: 12 April 2024

import time
import polling_loop as pl
def traffic_light_sequence(changeableConditions):
    """iterates through the traffic light sequences in normal operation mode

    Args:
        changeableConditions (dictionary): from changeable conditions we take
        pollingRate which is required to keep the code operating in time with the polling loop

    Returns:
        trafficStage: Feedback which stage the traffic lights are in to normal_operation
        which is requred for led_state to trigger the relevant LED's
    """
    pollingRate = changeableConditions['pollingRate']
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
    #each stage needs a time stamp
        trafficStage.append('stage1')
        if 'stage1' in trafficStage:
            print('Current stage: stage 1')
            print(f" {stage1}")
            # print(pl.polling_loop())
            time.sleep(pollingRate)
            trafficStage.pop(0)
            trafficStage.append('stage2')
        
        if 'stage2' in trafficStage:
            print('Current stage: stage 2')
            print(f" {stage2}")
            time.sleep(pollingRate)
            trafficStage.pop(0)
            trafficStage.append('stage3')

        if 'stage3' in trafficStage:
            print('Current stage: stage 3')
            print(f" {stage3}")
            time.sleep(pollingRate)
            trafficStage.pop(0)
            trafficStage.append('stage4')

        if 'stage4' in trafficStage:
            print('Current stage: stage 4')
            print(f"{stage4}")
            time.sleep(pollingRate)
            trafficStage.pop(0)
            trafficStage.append('stage5')

        if 'stage5' in trafficStage:
            print('Current stage: stage 5')
            print(f"{stage5}")
            time.sleep(pollingRate)
            trafficStage.pop(0)
            trafficStage.append('stage6')

        if 'stage6' in trafficStage:
            print('Current stage: stage 6')
            print(f"{stage6}")
            time.sleep(pollingRate)
            trafficStage.pop(0)
            trafficStage.append('stage1')
        return trafficStage
