#!/usr/bin/python
# -*- coding:utf-8 -*-

import serial
import RPi.GPIO as GPIO

TXDEN_1 = 27
TXDEN_2 = 22

# dev = "/dev/ttySC0"

class config(object):
    def __init__(ser, Baudrate = 9600, dev = "/dev/ttyS0"):
        #print (dev)
        ser.dev = dev
        ser.serial = serial.Serial(ser.dev, Baudrate)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TXDEN_1, GPIO.OUT)
        GPIO.setup(TXDEN_2, GPIO.OUT)

        GPIO.output(TXDEN_1, GPIO.HIGH)
        GPIO.output(TXDEN_2, GPIO.HIGH)
        
    def Uart_SendByte(ser, value): 
        ser.serial.write(value) 

    def Uart_ReceiveByte(ser): 
        return ser.serial.read(7)

    def Uart_Set_Baudrate(ser, Baudrate):
         ser.serial = serial.Serial(ser.dev, Baudrate)
         
class windSpeedandDirection():
    @property
    def speed(self):
        ser = config(dev = "/dev/ttySC1")
        data = bytes.fromhex('FA 03 00 00 00 01 91 81')
        
        GPIO.output(TXDEN_2, GPIO.HIGH) #send
        ser.Uart_SendByte(data)
        GPIO.output(TXDEN_2, GPIO.LOW) #receive

        wind_speed = str(ser.Uart_ReceiveByte().hex())
        wind_speed = int(wind_speed[6:10], 16) / 10

        return wind_speed
        
    @property
    def direction(self):
        ser = config(dev = "/dev/ttySC0")
        data = bytes.fromhex('FA 03 00 00 00 01 91 81')
        
        GPIO.output(TXDEN_1, GPIO.HIGH) #send
        ser.Uart_SendByte(data)
        GPIO.output(TXDEN_1, GPIO.LOW) #receive

        wind_direction = str(ser.Uart_ReceiveByte().hex())
        wind_direction = int(wind_direction[6:10], 16) / 10

        return wind_direction
        