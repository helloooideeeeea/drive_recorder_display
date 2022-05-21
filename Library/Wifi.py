import os, time
from loguru import logger


class Wifi:

    DEFAULT_SSID = "YSiPhoneXR"
    HOUSE_SSID = "aterm-ba29a9-a"

    def __init__(self):
        self.interface_name = "wlan0"

    def search(self):
        command = """sudo iwlist {} scan | grep -ioE 'ssid:(.*)'"""
        result = os.popen(command.format(self.interface_name))
        result = list(result)
        if "Device or resource busy" in result:
            raise Exception()
        ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]
        return ssid_list

    def find_SSID(self, ssid):
        ssid_list = self.search()
        return ssid in ssid_list

    def connected_SSID(self):
        command = "wpa_cli -i {} status | grep -ioE '^ssid=(.+)'"
        result = os.popen(command.format(self.interface_name))
        ssid = list(result)[0][5:].strip()
        return ssid

    def is_connected_target_SSID(self, ssid):
        return self.connected_SSID() == ssid

    def is_connected_default_SSID(self):
        return self.is_connected_target_SSID(self.DEFAULT_SSID)

    def switch_network(self, ssid):
        switch_command = "wpa_cli -i {} select_network {}".format(self.interface_name, ssid)
        reboot_command = "wpa_cli -i {} reconfigure".format(self.interface_name)
        os.system(switch_command)
        time.sleep(1)
        os.system(reboot_command)
        time.sleep(2)
        os.system(switch_command)


