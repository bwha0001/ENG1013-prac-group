#seven segment display with shift register
#Authors: Kayla Robinson
#Version: 6
#Dates Edited: 16 May 2024

from pymata4 import pymata4
board = pymata4.Pymata4()
import time

mode = "common_annode"

def globals():
    serPin = 8 #data pin
    srclk = 12 #clock pin
    rclk = 13 #also called the latch
    return serPin, srclk, rclk


def seg_reset(reset):
    global mode
    serPin = 8 #data pin
    srclk = 12 #clock pin
    rclk = 13 #also called the latch

    board.set_pin_mode_digital_output(serPin)
    board.set_pin_mode_digital_output(srclk)
    board.set_pin_mode_digital_output(rclk)

    board.digital_write(rclk, 0)

    for i in range(8): ##################
        board.digital_write(serPin, 0)
        board.digital_write(srclk, 1)
        board.digital_write(srclk, 0)

    board.digital_write(rclk, 1)
    return reset

def seg_setup_with_shift(serPin, srclkPin, rclkPin, ser, segs, digits):
        serPin = 8, #data pin
        srclkPin = 12 #clock pin
        rclkPin = 13 #also called the latch
        board.set_pin_mode_digital_output(serPin)
        board.set_pin_mode_digital_output(srclkPin)
        board.set_pin_mode_digital_output(rclkPin)
        D1 = int("1000")
        D2 = int("0100")
        D3 = int("0010")
        D4 = int("0001")
        digits = [D1, D2, D3, D4]
        segs = ["10000000", "01000000", "00100000", "00010000", "00001000", "00000100", "00000010", "00000001"]
        ser = {
            0:"11111100",
            1:"01100000",
            2:"11011010",
            3:"11110010",
            4:"01100110",
            5:"10110110",
            6:"10111110",
            7:"11100000",
            8:"11111110",
            9:"11110110",
            10:"00000000", #all off
            11:"11111111", #all on
            'a' : '111011000',
            'n' : '001010100',
            'm' : '000110100',
            'd' : '011110100', 
            'c' : '000110100',
            'g' : '101111100', 
            'p' : '110011100'
        }
        return serPin, srclkPin, rclkPin, ser, digits, segs

segs = ["10000000", "01000000", "00100000", "00010000", "00001000", "00000100", "00000010", "00000001"]
ser = {
            0:"11111100",
            1:"01100000",
            2:"11011010",
            3:"11110010",
            4:"01100110",
            5:"10110110",
            6:"10111110",
            7:"11100000",
            8:"11111110",
            9:"11110110",
            10:"00000000", #all off
            11:"11111111", #all on
            'a' : '111011000',
            'n' : '001010100',
            'm' : '000110100',
            'd' : '011110100', 
            'c' : '000110100',
            'g' : '101111100', 
            'p' : '110011100'
        }

D1 = int("1000")
D2 = int("0100")
D3 = int("0010")
D4 = int("0001")
#digits = [D1, D2, D3, D4]

def print_digit(chara, digitPort):
    seg_reset()
    character = -1
    charsInDict = 19
    board.digital_write(digitPort, mode)
    for i in range(charsInDict):
        if chara == segs[i][8]:
            character = i
    if character == -1:
        board.digital_write("00000001",not mode)
    else:
        for i in range(8):
            if mode == "common_annode":
                board.digital_write(segs[i], not ser[character][i])
            elif mode == "common cathod":
                board.digital_write(segs[i], ser[character][i])
    return

def print_display(phrase, pause):
    char1 = phrase[0]
    char2 = phrase[1]
    char3 = phrase[2]
    char4 = phrase[3]
    char1Num = 0
    char2Num = 0
    char3Num = 0
    char4Num = 0
    stringLength = len(phrase)
    if stringLength < 5:
        for i in range(int(pause/8)+1):
            if 1 > stringLength:
                char1 = ' '
            else: 
                char1 = phrase[0]
            if 2 > stringLength:
                char2 = ' '
            else:
                char2 = phrase[1]
            if 3 > stringLength:
                char3 = ' '
            else:
                char3 = phrase[2]
            if 4 > stringLength:
                char4 = ' '
            else:
                char4 = phrase[3]
            board.digital_write(char1, D1)
            time.sleep(0.002)
            board.digital_write(char2, D2)
            time.sleep(0.002)
            board.digital_write(char3, D3)
            time.sleep(0.002)
            board.digital_write(char4, D4)
            time.sleep(0.002)
        else:
            for t in range(stringLength + 1):
                for ti in range(int(pause/8) + 1):
                    board.digital_write(char1, D1)
                    time.sleep(0.002)
                    board.digital_write(char2, D2)
                    time.sleep(0.002)
                    board.digital_write(char3, D3)
                    time.sleep(0.002)
                    board.digital_write(char4, D4)
                    time.sleep(0.002)
                if t + 1 > stringLength:
                    char1 = ' '
                else:
                    char1 = phrase[t]
                if t + 2 > stringLength:
                    char2 = ' '
                else:
                    char2 = phrase[t + 1]
                if t + 3 > stringLength:
                    char3 = ' '
                else:
                    char3 = phrase[t + 2]
                if t + 4 > stringLength:
                    char4 = ' '
                else:
                    char4 = phrase[t + 3]
    return


serPin = 8 #data pin
srclk = 12 #clock pin
rclk = 13 #also called the latch

def seg_loop():
    while True:
        try:
            choice = int(input(": "))
            for i in range(8):
                board.digital_write(serPin, int(ser[choice][7-i]))
                board.digital_write(srclk, 1)
                board.digital_write(srclk, 0)
            board.digital_write(rclk, 1)
            time.sleep(2)
            board.digital_write(rclk, 0)
        except KeyboardInterrupt:
            break

    for i in range(8):
        board.digital_write(serPin, 0)
        board.digital_write(srclk, 1)
        board.digital_write(srclk, 0)
    board.digital_write(rclk, 1)



time.sleep(0.5)
board.shutdown()
