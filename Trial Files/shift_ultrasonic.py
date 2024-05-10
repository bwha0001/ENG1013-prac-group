#Week 10 Lab Task 2
from pymata4 import pymata4
board = pymata4.Pymata4()
import time


triggerPin = 10
echoPin = 11
ser = 5
rclk = 6
srclk = 7

board.set_pin_mode_digital_output(ser)
board.set_pin_mode_digital_output(rclk)
board.set_pin_mode_digital_output(srclk)
board.set_pin_mode_sonar(triggerPin, echoPin)

shiftLights = {
    "red":[1, 0, 0, 0, 0, 0, 0, 0],
    "yellow":[0, 1, 0, 0, 0, 0, 0, 0],
    "green": [0, 0, 1, 0, 0, 0, 0, 0]
    }

board.digital_pin_write(rclk, 1)
board.digital_pin_write(rclk, 0) 


for i  in range(0,len(shiftLights["red"])):
    board.digital_pin_write(ser, 1)
    board.digital_pin_write(srclk, 0)
    time.sleep(0.0005)
    board.digital_pin_write(srclk, 1)
    time.sleep(0.0005)

board.digital_pin_write(rclk, 0)
time.sleep(0.0005)
board.digital_pin_write(rclk, 1) 
time.sleep(2)

while True:
    try:
        time.sleep(2)
        result, recordTime = board.sonar_read(triggerPin)

        if result > 15:
            code = shiftLights["red"]
        elif  10 <= result <= 15:
            code = shiftLights["yellow"]
        elif result < 10:
            code = shiftLights["green"]
        
        for i in range(0,len(code)):
            board.digital_pin_write(ser, code[i])
            board.digital_pin_write(srclk,0)
            time.sleep(0.005)
            board.digital_pin_write(srclk,1)
            time.sleep(0.005)

        board.digital_pin_write(rclk, 0)
        time.sleep(0.005)
        board.digital_pin_write(rclk, 1)
        time.sleep(0.001)
        print(result)
    except KeyboardInterrupt:
        board.shutdown()
        quit()