#!/usr/bin/env python3
import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB2', 9600, timeout=1)
    ser.flush()

    while True:
        ser.write(b"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffrffffffffffffffffffffffffffffffff\n")
        line = ser.readline().decode('ascii').rstrip()
        print("-----------transmitted data---------")
        print(line)
        #ser.flush()
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print("--------received data-------")
            print(line)
            #ser.flush()

        time.sleep(1)
