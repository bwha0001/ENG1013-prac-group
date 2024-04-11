import pymata4.pymata4
import module_scripts as mod
import numpy as np
import math as mth
import pymata4
import polling_loop as pl
import to_7_segment_display as to_7_seg
import traffic_light_sequence as TLS
import time


# board = pymata4.pymata4
def normal_operating(intersectionData, changeableConditions):
    """collectes data

    Args:
        changeableConditions: changeableConditions['trafficStage]
        changeableConditions: changeableConditions['pollingRate]
    """
    pollingRate = changeableConditions['pollingRate']
    trafficStage = changeableConditions['trafficStage']
    while True:
        [distToVehicle, pedCount, pollingTime] = pl.polling_loop(intersectionData, changeableConditions)
        TLS.traffic_light_sequence()
        to_7_seg.sevenSeg('n', pedCount)
        time.sleep(pollingTime)




# board.shutdown()
