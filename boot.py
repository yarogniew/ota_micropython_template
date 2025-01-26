# from ota import OTAUpdater
# # import machine
# import os
# import credentials

# # SSID = credentials.WIFI_SSID
# # PASSWORD = credentials.WIFI_PASSWORD

import network
import machine
import os
import utime
import ota
import credentials

# Nazwa urządzenia (unikalna dla każdego mikroprocesora)
DEVICE_NAME = "device_1"

# Konfiguracja Wi-Fi
WIFI_SSID = credentials.WIFI_SSID
WIFI_PASSWORD = credentials.WIFI_PASSWORD

# Adres serwera Flask z OTA
OTA_SERVER_URL = "http://192.168.1.111:8080"

def connect_to_wifi():
    """Funkcja łącząca mikroprocesor z siecią Wi-Fi."""
    print("Łączenie z siecią Wi-Fi...")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    
    retries = 10
    while not sta_if.isconnected() and retries > 0:
        print(".", end="")
        utime.sleep(1)
        retries -= 1
    
    if sta_if.isconnected():
        print("\nPołączono z Wi-Fi!")
        print(f"Konfiguracja sieci: {sta_if.ifconfig()}")
        return True
    else:
        print("\nNie udało się połączyć z Wi-Fi.")
        return False

def main():
    """Główna funkcja inicjalizacji."""
    if connect_to_wifi():
        try:
            # Inicjalizacja OTA i sprawdzanie aktualizacji
            # updater = ota.OTAUpdater(WIFI_SSID, WIFI_PASSWORD, f"{OTA_SERVER_URL}/ota_files/{DEVICE_NAME}/")
            updater = ota.OTAUpdater(WIFI_SSID, WIFI_PASSWORD, OTA_SERVER_URL, DEVICE_NAME)

            updater.download_and_install_update_if_available()
        except Exception as e:
            print(f"Błąd aktualizacji OTA: {e}")

    # Jeśli połączenie z serwerem Flask się nie powiedzie, uruchom plik main.py
    if "main.py" in os.listdir():
        print("Uruchamianie pliku main.py...")
        import main
    else:
        print("Nie znaleziono pliku main.py. Zatrzymanie urządzenia.")
        machine.reset()

main()






# def main():
#     # Skonfiguruj parametry Wi-Fi oraz URL serwera Flask
#     SSID = credentials.WIFI_SSID
#     PASSWORD = credentials.WIFI_PASSWORD
#     server_url = 'http://192.168.1.111:8080'  # URL do lokalnego serwera Flask

#     try:
#         # Inicjalizacja aktualizatora OTA
#         updater = OTAUpdater(SSID, PASSWORD, server_url)
        
#         # Sprawdzenie dostępności aktualizacji i jej ewentualne pobranie
#         updater.download_and_install_update_if_available()

#     except Exception as e:
#         print(f"Nie udało się połączyć z serwerem OTA: {e}")
#         print("Uruchamianie lokalnego pliku main.py...")
        
#         # Sprawdź, czy plik main.py istnieje
#         if 'main.py' in os.listdir():
#             import main  # Importuje i uruchamia plik main.py
#         else:
#             print("Brak pliku main.py na urządzeniu!")

# # Uruchom funkcję main()
# main()
