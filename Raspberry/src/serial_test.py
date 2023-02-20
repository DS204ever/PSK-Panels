#!/usr/bin/python

import serial

ser = serial.Serial("/dev/ttyACM0",9600)

ser.write("1".encode())
print("teste")

while True:
    readedText = ser.readline().decode()
    print(readedText)
ser.close()