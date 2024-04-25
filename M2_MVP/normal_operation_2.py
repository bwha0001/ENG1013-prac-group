import numpy as np
import math as mth
#from pymata4 import pymata4
import polling_loop as pl
import to_7_segment_display as to_7_seg
import traffic_light_sequence as TLS
import time


# board = pymata4.pymata4
def normal_operating(board, board2, intersectionData, changeableConditions):
    """collectes data

    Args:
        changeableConditions: changeableConditions['trafficStage]
        changeableConditions: changeableConditions['pollingRate]
    """
    pollingRate = changeableConditions['pollingRate']
    trafficStage = changeableConditions['trafficStage']
    while True:
        [intersectionData, changeableConditions] = pl.polling_loop(board, board2, intersectionData, changeableConditions)

        distToVehicle = intersectionData['distToVehicleRecord'][-1]
        pedCount = intersectionData['pedCountRecord'][-1]
        pollingTime = changeableConditions['pollingRate']
#        to_7_seg.sevenSeg(board2, 'n', pedCount)
        TLS.traffic_light_sequence(changeableConditions)
        
        




# board.shutdown()
