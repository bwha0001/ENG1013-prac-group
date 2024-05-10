#Week 10 Lab Task 2
from pymata4 import pymata4
board = pymata4.Pymata4()
import time


triggerPin = 8
echoPin = 9
ser = 10
rclk = 11
srclk = 12

board.set_pin_mode_digital_output(ser)
board.set_pin_mode_digital_output(rclk)
board.set_pin_mode_digital_output(srclk)
board.set_pin_mode_sonar(triggerPin, echoPin)

shiftLights = {
    "red":[0, 0, 1],
    "green":[0, 1, 0],
    "blue": [1, 0, 0]
    }

board.digital_pin_write(rclk, 1)
board.digital_pin_write(rclk, 0) 


for i  in {1,2,3}:
    board.digital_pin_write(ser, 1)
    board.digital_pin_write(srclk, 1)
    time.sleep(0.0001)
    board.digital_pin_write(srclk, 0)

board.digital_pin_write(rclk, 0)
time.sleep(0.0001)
board.digital_pin_write(rclk, 1) 
time.sleep(2)

while True:
    try:
        time.sleep(0.5)
        result, recordTime = board.sonar_read(triggerPin)

        if result > 15:
            code = shiftLights["red"]
        elif  10 <= result <= 15:
            code = shiftLights["green"]
        elif result < 10:
            code = shiftLights["blue"]
        
        for i in range(0,len(code)):
            board.digital_pin_write(srclk,0)
            board.digital_pin_write(ser, code[i])
            time.sleep(0.001)
            board.digital_pin_write(srclk,1)

        board.digital_pin_write(rclk, 1)
        time.sleep(0.001)
        board.digital_pin_write(rclk, 0)
        time.sleep(0.001)

    except KeyboardInterrupt:
        board.shutdown()
        quit()