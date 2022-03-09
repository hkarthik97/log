import requests
class SnifferData:
    def __init__(self, MACAddress, DeviceID, RSSI):
        self.MACAddress = MACAddress
        self.DeviceID = DeviceID
        self.RSSI = RSSI

    
    def json(self):
        return{
            "MACAddress":self.MACAddress,
            "DeviceID":self.DeviceID,
            "RSSI":self.RSSI
        }
    
    def pushData(data):
        print("Pushing data")
        print(data)
        r = requests.post(url = "https://zig-web.com/ZIGSFirmware/api/FirmwareV2/AddMACAdress", data = data,timeout = 5)
        payload = r.json()
        print(payload)
