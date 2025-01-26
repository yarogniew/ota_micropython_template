import network
import urequests
import os
import json
import machine
from time import sleep

class OTAUpdater:
    def __init__(self, ssid, password, server_url, device_name):
        self.ssid = ssid
        self.password = password
        # Usuń zbędne ukośniki
        self.server_url = f"{server_url.rstrip('/')}/ota_files/{device_name.strip('/')}/"
        self.version_url = f"{self.server_url}version.json"
        self.firmware_url = f"{self.server_url}main.py"
        self.device_name = device_name

        # Wczytaj aktualną wersję oprogramowania z pliku
        if 'version.json' in os.listdir():
            with open('version.json') as f:
                self.current_version = int(json.load(f)['version'])
        else:
            self.current_version = 0
            with open('version.json', 'w') as f:
                json.dump({'version': self.current_version}, f)

    
    def connect_wifi(self):
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(self.ssid, self.password)
        while not sta_if.isconnected():
            print('.', end="")
            sleep(0.25)
        print(f'Connected to WiFi, IP is: {sta_if.ifconfig()[0]}')

    def fetch_latest_code(self):
        response = urequests.get(self.firmware_url)
        if response.status_code == 200:
            self.latest_code = response.text
            return True
        else:
            print(f'Firmware not found - {self.firmware_url}')
            return False

    def update_no_reset(self):
        with open('latest_code.py', 'w') as f:
            f.write(self.latest_code)
        self.current_version = self.latest_version
        with open('version.json', 'w') as f:
            json.dump({'version': self.current_version}, f)
        self.latest_code = None

    def update_and_reset(self):
        os.rename('latest_code.py', 'main.py')
        print('Restarting device...')
        machine.reset()

    def check_for_updates(self):
        self.connect_wifi()
        response = urequests.get(self.version_url)
        data = json.loads(response.text)
        self.latest_version = int(data['version'])
        return self.current_version < self.latest_version

    def download_and_install_update_if_available(self):
        if self.check_for_updates():
            if self.fetch_latest_code():
                self.update_no_reset()
                self.update_and_reset()
        else:
            print('No new updates available.')
