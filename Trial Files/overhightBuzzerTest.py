from pymata4 import pymata4
import time, threading



board = pymata4.Pymata4()
pin = 8
board.set_pin_mode_digital_output(pin)
print("on")
board.digital_write(pin,1)
time.sleep(2)
print("off")
board.digital_write(pin,0)
board.shutdown()
# # print("on")
# # timeNow = time.time()

# # board.digital_write(7,1)
# # board.digital_write(8,1)
# # currentTime = timeNow-time.time()
# # time.sleep(1)
# # board.digital_write(7,0)
# # board.digital_write(8,1)

# def turn_off(pin):
#     print("################\noff\n###########")
#     board.digital_write(pin, 0)

# # Function to trigger the output
# def trigger_output():
#     # Turn on the output
#     output_pin = 7
#     print("on")
#     board.digital_write(output_pin, 1)
#     # Schedule turning off the output after 10 seconds
#     threading.Timer(5, turn_off, args=[output_pin]).start()

# # Call the function to trigger the output

# trigger_output()


# # # board.digital_write(7,0)
# # print("#############################")
# # print("off\n\n\n\n\n\n")


# board.shutdown()