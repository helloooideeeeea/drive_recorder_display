import serial
import os, re
import RPi.GPIO as GPIO


class UPS:

    def __init__(self):
        self.ser = serial.Serial(os.getenv('UPS_DEVICE'), 9600)

    def get_data(self, nums):
        while True:
            count = self.ser.inWaiting()
            if count != 0:
                recv = self.ser.read(nums)
                return recv

    def decode_uart(self):

        uart_string = self.get_data(100)
        data = uart_string.decode('ascii', 'ignore')
        pattern = r'\$ (.*?) \$'
        result = re.findall(pattern, data, re.S)

        tmp = result[0]

        version = re.findall(r'SmartUPS (.*?),', tmp)
        vin = re.findall(r',Vin (.*?),', tmp)
        batcap = re.findall(r'BATCAP (.*?),', tmp)
        vout = re.findall(r',Vout (.*)', tmp)

        return version[0], vin[0], batcap[0], vout[0]

    def close(self):
        self.ser.close()