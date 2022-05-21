import os
from loguru import logger


class Wifi:

    def __init__(self):
        self.interface_name = "wlan0"

    def search(self):
        # sudo iwlist wlan0 scan | grep -ioE 'ssid:(.*)'
        command = """sudo iwlist {} scan | grep -ioE 'ssid:(.*)'"""
        result = os.popen(command.format(self.interface_name))
        result = list(result)
        if "Device or resource busy" in result:
            raise Exception()
        ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]
        return ssid_list

    def connection(self, ssid, password):
        cmd = "iwconfig {} password {} iface {}".format(ssid, password, self.interface_name)
        if os.system(cmd) != 0:
            logger.info("Couldn't connect to ssid:{}".format(ssid))
            raise Exception()
        logger.info("Successfully connected to {}".format(ssid))
