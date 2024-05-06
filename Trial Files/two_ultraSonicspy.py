from pymata4 import pymata4
import time

board = pymata4.Pymata4()

changeableConditions = {
    'arduinoPins' : {
        "pedButton":5,
        "triggerPin":2,
        "echoPin":3,
        "triggerPin2":4
        }}

board.set_pin_mode_sonar(changeableConditions['arduinoPins']['triggerPin'], changeableConditions['arduinoPins']['echoPin'])

read1 = board.sonar_read(changeableConditions["arduinoPins"]["triggerPin"])
print(f"read1 {read1}")
time.sleep(1)
read1 = board.sonar_read(changeableConditions["arduinoPins"]["triggerPin2"])
print(f"read1 {read1}")

board.set_pin_mode_sonar(changeableConditions['arduinoPins']['triggerPin2'], changeableConditions['arduinoPins']['echoPin'])

while True:
    try:
        read1 = board.sonar_read(changeableConditions["arduinoPins"]["triggerPin"])
        print(f"read1 {read1}")
        time.sleep(1)
        read2 = board.sonar_read(changeableConditions["arduinoPins"]["triggerPin2"])
        print(f"read2 {read2}")
        time.sleep(1)
    except KeyboardInterrupt:
        board.shutdown()
        quit()


#read2 = board.set_pin_mode_sonar(changeableConditions["arduinoPins"]["triggerPin"], changeableConditions["arduinoPins"]["echoPin2"], timeout=200000)
#print(read2)
