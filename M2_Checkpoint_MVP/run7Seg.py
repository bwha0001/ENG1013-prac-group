import time
import math as mth
from pymata4 import pymata4 
import module_scripts as ms
import to_7_segment_display as sevSeg


board = pymata4.Pymata4()


digDisplay, mode, pedCounter = sevSeg.sevenSeg(board, 'c', '001')

sevSeg.to_arduino(board, digDisplay, mode, pedCounter)




