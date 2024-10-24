import serial

# Open the serial port (adjust the '/dev/ttyACM0' if it's different)
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

# Continuously read and print data from Pico
while True:
    try:
        data = ser.readline().decode('utf-8').rstrip()  # Read and decode the data
        if data:
            print(f"Received: {data}")  # Display the received data
    except serial.SerialException as e:
        print(f"Error reading from UART: {e}")
