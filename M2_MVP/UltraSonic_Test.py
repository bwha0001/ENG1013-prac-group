#Ultrasonic Sensor

from pymata4 import pymata4
import time

pollingRate = 2
changeableConditions = {
    'arduinoPins' : {
        "mainRed": 2,
        "mainYellow": 3,
        "mainGreen": 4,
        "sideRed": 5,
        "sideYellow": 6,
        "sideGreen": 7,
        "pedestrianRed": 8,
        "pedestrianGreen": 9,
        "triggerPin":13,
        "echoPin":12
        },
    'trafficStage' : 1,
    'pollingRate' : pollingRate,
    'pedCounterReset' : ""
}

trafficStage = 1   

#Set up arduino
board = pymata4.Pymata4()

#set arduino pins
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainRed"])
board.set_pin_mode_pwm_output(changeableConditions["arduinoPins"]["mainYellow"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["mainGreen"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideRed"])
board.set_pin_mode_pwm_output(changeableConditions["arduinoPins"]["sideYellow"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["sideGreen"])
board.set_pin_mode_digital_output(changeableConditions["arduinoPins"]["pedestrianRed"])
board.set_pin_mode_pwm_output(changeableConditions["arduinoPins"]["pedestrianGreen"])
# Configure pin to sonar
board.set_pin_mode_sonar(changeableConditions["arduinoPins"]["triggerPin"], changeableConditions["arduinoPins"]["echoPin"], timeout=20000)

try:
    while True:
        reading, timeStamp = board.sonar_read(changeableConditions["arduinoPins"]["triggerPin"])
        print(reading)
        time.sleep(1)
except KeyboardInterrupt:
    board.shutdown()