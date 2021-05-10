# https://github.com/YoshiRi/PyDMX

import serial
import time
import numpy as np


class PyDMX:
    def __init__(self, COM='COM8', Brate=250000, Bsize=8, StopB=2):
        self.ser = serial.Serial(COM, baudrate=Brate, bytesize=Bsize, stopbits=StopB)
        self.data = np.zeros([513], dtype='uint8')
        self.data[0] = 0  # StartCode
        self.sleepms = 44.0
        self.breakus = 176.0
        self.MABus = 16.0

    def set_random_data(self):
        self.data[1:513] = np.random.rand(512) * 255

    def set_data(self, id, data):
        self.data[id] = data

    def send(self):
        # Send Break : 88us - 1s
        self.ser.break_condition = True
        time.sleep(self.breakus / 1000000.0)

        # Send MAB : 8us - 1s
        self.ser.break_condition = False
        time.sleep(self.MABus / 1000000.0)

        # Send Data
        self.ser.write(bytearray(self.data))

    def sendzero(self):
        self.data = np.zeros([513], dtype='uint8')
        self.send()

    def __del__(self):
        print('Close serial server!')
        self.sendzero()
        self.ser.close()
