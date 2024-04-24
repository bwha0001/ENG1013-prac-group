from pymata4 import pymata4
import time

# Define the pins for the ultrasonic sensor
trigger_pin = 13  # Pin connected to the trigger of the ultrasonic sensor
echo_pin = 12     # Pin connected to the echo of the ultrasonic sensor

# Set up arduino
board = pymata4.Pymata4()

# Configure the ultrasonic sensor with an increased timeout value
board.set_pin_mode_sonar(trigger_pin, echo_pin, timeout=40000)  # Increased timeout to 40,000 microseconds (40ms)

try:
    while True:
        # Read distance from the ultrasonic sensor
        distance, timestamp = board.sonar_read(trigger_pin)
        
        # Print the distance in centimeters
        print("Distance:", distance, "cm")
        
        # Wait for a short time before the next reading
        time.sleep(1)
        
except KeyboardInterrupt:
    # Close the connection to the Arduino board
    board.shutdown()
