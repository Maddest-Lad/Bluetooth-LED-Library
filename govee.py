import json
from typing import List
from urllib.parse import urljoin

import requests

BASE_URL = "https://developer-api.govee.com"
DEVICE_LIST = "/v1/devices"
CONTROL = "/v1/devices/control"
API_KEY = open("api_key", 'r').read()


class Device:  # DataClass For Govee Devices

    def __init__(self, json_dict: dict):
        self.mac_address: str = json_dict["device"]
        self.model: str = json_dict["model"]
        self.deviceName: str = json_dict["deviceName"]
        self.retrievable: bool = json_dict["retrievable"]  # Query-ability of the Device
        self.commands: list = json_dict["supportCmds"]

        # Current State (Slowly Filled In)
        self.state = None
        self.color = None
        self.brightness = None

    def to_string(self) -> str:
        return f"{self.deviceName} \n " \
               f"Mac Address: {self.mac_address} \n " \
               f"Model: {self.model} \n " \
               f"Retrievable: {self.retrievable} \n " \
               f"Commands: {self.commands}"

    def turn_on(self):
        url = urljoin(BASE_URL, CONTROL)

        command = {"device": self.mac_address, "model": self.model, "cmd": {"name": "turn", "value": "on"}}

        requests.put(url=url, headers={'Govee-API-Key': API_KEY}, data=command)

    def turn_off(self):
        url = urljoin(BASE_URL, CONTROL)

        command = {"device": self.mac_address, "model": self.model, "cmd": {"name": "turn", "value": "off"}}

        requests.put(url=url, headers={'Govee-API-Key': API_KEY}, data=command)

    # RGB is from 0-255
    def set_color(self, r, g, b):
        url = urljoin(BASE_URL, CONTROL)

        command = {"device": self.mac_address, "model": self.model,
                   "cmd": {"name": "color", "value": {"r": r, "b": b, "g": g}}}

        requests.put(url=url, headers={'Govee-API-Key': API_KEY}, data=command)

    # Brightness is From 0-100
    def set_brightness(self, brightness):
        url = urljoin(BASE_URL, CONTROL)

        command = {"device": self.mac_address, "model": self.model, "cmd": {"name": "brightness", "value": brightness}}

        requests.put(url=url, headers={'Govee-API-Key': API_KEY}, data=command)


def get_my_devices() -> List[Device] or None:
    url = urljoin(BASE_URL, DEVICE_LIST)
    response = requests.get(url=url, headers={'Govee-API-Key': API_KEY})

    devices = []

    if response.status_code == 200:

        device_dict = json.loads(response.text)["data"]["devices"]

        for device in device_dict:
            if device["controllable"]:
                devices.append(Device(device))

        return devices

    return None
