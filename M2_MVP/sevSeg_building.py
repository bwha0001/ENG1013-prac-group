# testing file for to_7_seg to make it work on the arduino

from pymata4 import pymata4 
segE = 1+2
segD = 2+2
DP = 3+2
segC = 4+2
segG = 5+2
dig3 = 6+2
segB = 7+2
dig2 = 8+2
dig1 = 9+2
segF = 10+2
segA = 11+2
dig0 = 12+2
segs = [segA, segB,segC,segD,segE,segG, DP]
digs = [dig3,dig2,dig1, dig0]

board = pymata4.Pymata4()
for i in range(0,len(segs)):
        board.set_pin_mode_digital_output(segs[i])


segments = [['00011010'],['11110010'],['10110110'], ['11111100']]
# for i in segments[0]:
#     if segments[0][i] is not '0':
#         # board.ditigal_write(segs[0][i], 1)
#         segments[0][i] = segs[0][i]
#     else:
#          segments[0][i] = 0

# segments already in 0 and 1's so just need to point to pin in segs and apply int(segments value
