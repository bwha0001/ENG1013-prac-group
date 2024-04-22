from pymata4 import pymata4

def debounce_analog_input(board, analog_pin, debounce_delay=50, threshold=500):
    """
    Debounces an analog input and counts how many times it's pressed.

    Parameters:
        board (pymata4.Pymata4): The pymata4 board object.
        analog_pin (int): The pin number of the analog input.
        debounce_delay (int): The debounce delay in milliseconds. Defaults to 50ms.
        threshold (int): The threshold value to consider as a button press. Defaults to 500.

    Returns:
        int: The counter value.
    """
    counter = 0  # Initialize counter
    
    # Initialize variables for debounce
    last_state = None
    last_time = 0
    
    def handle_analog_data(data):
        nonlocal counter, last_state, last_time
        
        # Check if debounce delay has passed since last state change
        current_time = board.get_elapsed_ms()
        if current_time - last_time < debounce_delay:
            return
        
        # Check if current data value crosses the threshold
        if data[1] > threshold:
            # Check if this is a new press (transition from not pressed to pressed)
            if last_state is False or last_state is None:
                counter += 1  # Increment counter
                print("Button pressed. Counter:", counter)
            last_state = True
        else:
            last_state = False
        
        # Update last time
        last_time = current_time

    # Add analog data event handler
    board.analog_data_event(analog_pin, handle_analog_data)
    
    # Return the counter value (not necessary if you want to just print it inside the function)
    return counter

# Example usage
def main():
    # Create pymata4 board object
    board = pymata4.Pymata4()
    
    # Define the analog pin
    analog_pin = 0
    
    # Run debounce function
    counter = debounce_analog_input(board, analog_pin)
    
    # Print final counter value
    print("Final Counter Value:", counter)
    
    # Cleanup
    board.shutdown()

if __name__ == "__main__":
    main()
