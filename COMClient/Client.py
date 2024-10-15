import serial
import time

ser = serial.Serial('/tmp/ttyV1', 9600)
time.sleep(2)

try:
    while True:
        ser.write(("Hello, Server" + '\n').encode())
        time.sleep(0.1)

        response = ser.readline().decode().strip()
        print("Received from server:", response)

except KeyboardInterrupt:
    print("Close the Program.")

finally:
    ser.close() 