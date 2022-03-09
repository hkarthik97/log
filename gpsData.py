import requests

class logData:
    def __init__(self, error, status, deviceId):
        
        self.error = error
        self.status = status
        self.deviceId = deviceId
    
    def json(self):
        return{
            "Error":self.error,
            "Status":self.status,
            "Deviceid":self.deviceId,
        }

    def pushData(data):
        print("Pushing data")
        print(data)
        r = requests.post(url = "https://zig-web.com/ZIGSmartIOT/api/Firmware/Adddevicelog", data = data,timeout = 5)
        payload = r.json()
        print(payload)

class gpsParamData:

    def __init__(self, Latitude, Longitude, Speed, Altitude, Token, Deviceid, Voltage, Direction, Wifisignal, Statellitecount):
        self.Latitude = Latitude
        self.Longitude  = Longitude
        self.Speed = Speed
        self.Altitude = Altitude
        self.Token = Token
        self.Deviceid = Deviceid
        self.Voltage = Voltage
        self.Direction = Direction
        self.Wifisignal = Wifisignal
        self.Statellitecount = Statellitecount

    
    def json(self):
        return{
            "Latitude": self.Latitude,
            "Longitude": self.Longitude,
            "Speed": self.Speed,
            "Altitude": self.Altitude,
            "Token": self.Token,
            "Deviceid": self.Deviceid,
            "Voltage": self.Voltage,
            "Direction": self.Direction,
            "Wifisignal": self.Wifisignal,
            "Statellitecount": self.Statellitecount
        }
    
    def pushData(data):
        print("Pushing data")
        print(data)
        r = requests.post(url = "https://zig-web.com/ZIGSmartIOT/api/Firmware/Addgpsdata", data = data,timeout = 5)
        payload = r.json()
        print(payload)
