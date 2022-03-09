import json
import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
from pytz import timezone
import requests
import random
from json.decoder import JSONDecodeError
from _thread import start_new_thread
import smtplib
from gpsData import logData,gpsParamData
import time


curr_time = time.localtime()
curr_clock = time.strftime("%H:%M:%S", curr_time)
from Sniffer import SnifferData
import itertools
threadId = 1 # thread counter
waiting = 2 # 2 sec. waiting time

MQTT_SERVER = "mqtt.zig-web.com"
MQTT_PATH1 = "/lora/temp"
MQTT_PATH2 = "/zed/barcode"
MQTT_PATH3 = "/zed/validate/nfc"
MQTT_PATH4 = "/zed/validate/barcode"
MQTT_PATH5 = "/test/mail"
LOG_DATA = "/zed/logData"
GPS_DATA = "/zed/gpsdata"
Sniffer = "Sniffer"
Sniffer2 = "/zed/Sniffer"
STATUS = "/zed/validate/status"
# format = "%Y-%m-%dT%H:%M"
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Us/Eastern'))
print(now_asia)
dateString = str(now_asia)
ada = dateString[:10]+"T"+dateString[11:]
datee = ada[:19]
print (datee)
# MQTT_PATH3 = "/zed/validate/nfc"
# MQTT_PATH4 = "/zed/validate/barcode"
# format = "%Y-%m-%dT%H:%M"
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Us/Eastern'))
print(now_asia)
dateString = str(now_asia)
ada = dateString[:10]+"T"+dateString[11:]
datee = ada[:19]
print (datee)
# print (ada)
print(MQTT_SERVER)
# conn = psycopg2.connect(database = "karthik", user = "karthik", password = "karthikkaran", host = "127.0.0.$
# # mydb = mysql.connector.connect(
# #   host="127.0.0.1",
# #   user="root",
# #   passwd="password",
# #   database="messages"
# # )

conn = sqlite3.connect('data.db')

token = "3Y1QwEDfikGni1PPouV7aw=="

def jsonFix(jsondata):
    js = jsondata
    js= js+"}"
    js1 = js.split("{\"MAC\":")
    result = ""
    js1 = js1[1:]
    for s in js1:
            result += "," + "{\"MAC\":" + s
    result = result.strip(",")
    result = "[" + result + "]"
    result = result.replace("'", '')
    # fd = json.loads(result)
    return result
def nfcTicketData(ticketId,cardId,deviceId,Tickettype,TicketStatus):
    data = {
        "Deviceid":deviceId,
        "Tickettype":Tickettype,
        "Ticketid":ticketId,
        "Usermac":cardId,
        "Message":TicketStatus
    }
    print("posting data in  mutlithread")
    r = requests.post(url = "https://zig-web.com/ZIGSmartIOT/api/Inspector/Addvalidator", data = data,timeout = 5)
    ticketDetails = r.json()
    print(ticketDetails)
    print(data)

def barcodeTicketData(barcode,deviceId,userId,Tickettype):
    print("posting data in  mutlithread")
    data = {
        "Deviceid":deviceId,
        "Tickettype":Tickettype,
        "Ticketid":barcode,
        "Userid":userId,
        "Message":"IN"
    }
    print("posting data in  mutlithread")
    r = requests.post(url = "https://zig-web.com/ZIGSmartIOT/api/Inspector/Addvalidator", data = data,timeout = 5)
    ticketDetails = r.json()
    print(ticketDetails)
    print(data)



def nfc():
    now_utc = datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Us/Eastern'))
    dateString = str(now_asia)
    ada = dateString[:10]+"T"+dateString[11:]
    datee = ada[:19]
    print (datee)
    print("inside transaction")
    random_number = random.randint(1000000000000000, 9999999999999999)
    print (random_number)
    data1  = {
            "Token": "ac23fb78-53f9-49c8-8d19-fc2b5efaf376",
            "FromAddress": "S 6th @ W Liberty",
            "DestinationAddress": "Iroquois Park Loop",
            "TransactionDate": datee,
            "currentlocation": "true",
            "departattime": datee,
            "TotalAmount": "1.50",
            "PlaceId": "123456",
            "Tickets": [
                {
                    "Amount": "1.50",
                    "RouteId": "Single Ride",
                    "TripId": "4",
                    "ProfileId": 0,
                    "FromAddress": "S 6th @ W Liberty ",
                    "DestinationAddress": "Iroquois Park Loop",
                    "Fareid": "9",
                    "Tickettype": 0
                }
            ],
            "Message": "Ticket Take in NFC App",
            "TransactionId": "2"+str(random_number),
            "Userid": 10504
    }
    json_data1 = json.dumps(data1,indent=2)
    print(json_data1)
    headers = {'Content-type': 'application/json'}
    r = requests.post(url = "https://zig-web.com/ZIGSmartIOT/api/Tickets/Addnew", data = json_data1,headers=headers,timeout = 15)
    ticketDetails = r.json()
    #
    print(ticketDetails)
    print(r)

def nfcValidate(cardId,topic,deviceID):
    print("inside function")
    nfcUrl = "https://zig-web.com/ZIGSmartIOT/api/Inspector/PurchaseticketfromwalletHWnew?TokenID=3Y1QwEDfikGni1PPouV7aw==&PhysicalID={}&wallettype=0".format(cardId)
    print(nfcUrl)
    r = requests.post(url = nfcUrl,timeout=5)
    response = r.json()
    status=response["Status"]
    print(status)
    print("above is status")
    ticketId = response["Ticketid"]
    if(status):
        ret= client.publish(topic,"1")
        start_new_thread(nfcTicketData, (ticketId,cardId,deviceID,0,"IN"))
    else:
        ret= client.publish(topic,"3")
        start_new_thread(nfcTicketData, (0,cardId,deviceID,0,"Illegal"))
        # start_new_thread(test, (ticketId, ))

# the following function is for Beverage validation
def validateBeverage(userId, deviceId):
    print("Inside  Beverage Validation")
    r = requests.get(url = "https://zig-web.com/ZIGSmartIOT/api/Application/SendBeverageStatus?Userid="+userId+"&DeviceID="+deviceId)
    getData = r.json()
    try:
        message = getData["Message"]
    except:
        pass
    print(getData)
    if(message == "Ok"):
        print("beverage true")
        return True
    else:
        print("beverage false")
        return False
# the following function does the queue validation
def getQueueTicket(ticketId):
    print("Inside Queue validation")
    r = requests.get(url  = "https://zig-web.com/ZIGSFirmware/api/FirmwareV2/UpdateAnonymousUserRideInfo?userid="+ticketId)
    getData = r.json()
    
    try:
        message = getData["Message"]
        ticketStatus = getData["bStatus"]
    except:
        pass
    print(getData)
    if(ticketStatus):
        return True
    else:
        return False

def getTicket(barcode,DeviceId):
    print(barcode)
    data = {
        "TicketId":barcode,
        "Token":token,
        "Blnvalidate":"true",
        "Whichdevice":2
    }

    # r = requests.post(url = "https:// lookdigitalsoftware.com/ZIGSTARCTEST/api/Firmware/Firmwareticketstatus", data = data,timeout = 5)
    r = requests.post(url = "https://zig-web.com/ZIGSmartIOT/api/Firmware/Firmwareticketstatus", data = data,timeout = 5)
    ticketDetails = r.json()
    print(data)
    if(str(r) != "<Response [500]>"):
        print(ticketDetails)
        ticketStatus = ticketDetails['Result']['Status']
        userID = ticketDetails['Result']['Userid']
        ticketCount = ticketDetails['Result']['Ticketcount']
        print(ticketStatus)
        print ("Ticket Count = "+str(ticketCount))
        c = "{0:0=3d}".format(ticketCount)
        ticketMsg = "201"+str(c)
        print(userID)
        if(ticketStatus == 1 or ticketStatus == 2 ):
            print("Ticket validated")
            start_new_thread(barcodeTicketData, (barcode,DeviceId,userID,1))
            return ticketMsg
        elif(ticketStatus == 3):
            c = "{0:0=3d}".format(ticketCount)
            ticketMsg = "301"+str(c)
            print("Not a valid ticket")
            # start_new_thread(barcodeTicketData, (barcode,DeviceId,1,1))
            return ticketMsg
            # start_new_thread(barcodeTicketData, (barcode,DeviceId,1,1))
        
        else:
            print("debug")
            return 3
    else:
        print ("Invalid Ticket")
        return 301

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH1)
    client.subscribe(MQTT_PATH2)
    client.subscribe(MQTT_PATH3)
    client.subscribe(MQTT_PATH4)
    client.subscribe(MQTT_PATH5)
    client.subscribe(GPS_DATA)
    client.subscribe(LOG_DATA)
    client.subscribe(Sniffer)
    client.subscribe(Sniffer2)
    client.subscribe(STATUS)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    now_utc = datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Us/Eastern'))
    print(now_asia)
    dateString = str(now_asia)
    ada = dateString[:10]+"T"+dateString[11:]
    datee = ada[:19]


    #print(msg.topic+" "+str(msg.payload))

    print("success")
    topic = msg.topic
    print(type(topic))

    if (topic==MQTT_PATH1):
        y = json.loads(msg.payload)
        print(y["mac_id"])
        cur = conn.cursor()
        mac_id = y["mac_id"]
        temperature= y["temperature"]
        air_quality = y["air_quality"]

        # sql = "INSERT INTO lorasensordata (mac_id, temperature, air_quality, addedDateTime) VALUES (%s, %s,$
        # val = (y["mac_id"], y["temperature"],y["air_quality"],now_asia)
        sql = "INSERT INTO lorasensordata (mac_id, temperature, air_quality,addeDateTime) VALUES (?, ?, ?, ?)"
        val = (mac_id, temperature,air_quality,datetime.now())
        cur.execute(sql,val)
        conn.commit()
        print(cur.rowcount, "record inserted.")
    elif(msg.topic==MQTT_PATH4): #Qr validation
        print("inside p4")
        y = json.loads(msg.payload)
        try:
            ticketId = y["ticketId"]
            DeviceId = y["DeviceId"]
        except:
            pass
        topic = "3C:71:BF:F9:D7:70"+"/nfc"
        topicc = DeviceId+"/nfc"
        singleticket = ticketId.split("\r")
        print(DeviceId)
        print(topic)
        print(singleticket[0])
        ticketLength = len(singleticket[0])
        if(ticketLength >= 4 and ticketLength <= 6):
            print("Queue ticket")
            # status = getQueueTicket(singleticket[0])
            status = validateBeverage(singleticket[0],DeviceId)
            if(status):
                ret= client.publish(topic,"201")
                ret= client.publish(topicc,"201")
            else:
                ret= client.publish(topic,"301")
                ret= client.publish(topicc,"301")
        
        elif(ticketLength > 5):
            
            print("gng to api")
            data = getTicket(singleticket[0],DeviceId)

            ret= client.publish(topicc,str(data))
            # print(data)
            # if(data==1 or data==2 ):
            #     print(topic)
            #     ret= client.publish(topic,"1")
            #     ret= client.publish(topicc,"1")
            # elif(data==3):
            #     ret= client.publish(topic,"3") # this shld be 3
            #     ret= client.publish(topicc,"3") # this shld be 3
            # elif(data==0):
            #     print("data 0")
            #     ret= client.publish(topic,"0")
            #     ret= client.publish(topicc,"0")
        else:
            print("Invalid data")
            ret= client.publish(topicc,"301")
    elif(msg.topic==MQTT_PATH3):
        print("inside p3")
        print(msg.payload)
        payload = msg.payload

        try:
            print("Inside try")
            y = json.loads(payload)
            print("test1123")
            cardId = y["cardId"]
            DeviceId = y["DeviceId"]
            topic = DeviceId+"/nfc"
            print(DeviceId)
            print(cardId)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print ('Decoding JSON has failed')
        except JSONDecodeError as e:
            print("test 1" +e)
    # do whatever you want
        except TypeError as e:
            print("test 2" +e)
        if(cardId[2]!=":"):
            cardId="0"+cardId
            print(cardId)
            nfcValidate(cardId,topic,DeviceId)
        else:
            nfcValidate(cardId,topic,DeviceId)
    elif(msg.topic==LOG_DATA):
        print("Getting logdata")
        payload = msg.payload
        parse = json.loads(payload)
        try:
            error = parse["Error"]
            deviceId = parse["Deviceid"]
            status = parse["Status"]
            data = logData(error, status, deviceId)
            # logData.pushData(data.json())
            start_new_thread(logData.pushData,(data.json(),))
        except Exception as e:
            print(e)
            pass
    elif(msg.topic == GPS_DATA):
        print("receiving gps data")
        payload = msg.payload
        

        try:
            parse = json.loads(payload)
            Latitude = parse["Latitude"]
            Longitude = parse["Longitude"]
            Speed = parse["Speed"]
            Altitude = parse["Altitude"]
            Token = parse["Token"]
            Deviceid = parse["Deviceid"]
            Voltage = parse["Voltage"]
            Direction = parse["Direction"]
            Wifisignal = parse["Wifisignal"]
            Statellitecount = parse["Statellitecount"]

            data = gpsParamData(
                Latitude = Latitude , 
                Longitude = Longitude, 
                Speed = Speed, 
                Altitude = Altitude, 
                Token = Token, 
                Voltage = Voltage, 
                Direction = Direction,  
                Wifisignal = Wifisignal,
                Deviceid = Deviceid,
                Statellitecount = Statellitecount)

            # gpsParamData.pushData(data.json())
            start_new_thread(gpsParamData.pushData,(data.json(),))
        
        except Exception as e:
            print(e)
            pass
    elif(msg.topic == Sniffer2):
        print("receiving sniffer data")
        payload = msg.payload
        parse = json.loads(payload)
        try:
            DeviceId =  parse["DeviceId"]
            Mac = parse["MAC"]
            RSSI = parse["RSSI"]
            data = [{"MACAddress":mac,"DeviceID":DeviceId,"RSSI":rssi}  for (mac,rssi) in zip(Mac,RSSI )]
            print(data)
            finaldata = json.dumps(data)
            newHeaders = {'Content-type': 'application/json'}
            # SnifferData.pushData(data)
            r = requests.post(url = "https://zig-web.com/ZIGSFirmware/api/FirmwareV2/AddMACAdress", data = finaldata,headers = newHeaders)
            pay = r.json()
            print(r.status_code)
            print(pay)
        except Exception as e:
            print("Inside Exception")
            print(e)
    elif (msg.topic == Sniffer):
        print("receiving sniffer2 data")
        payload = msg.payload
        snifferData = jsonFix(str(payload))
        snifferData = json.loads(snifferData)
        # print(snifferData)
        for x in snifferData:
            parse = x
            print(parse["Macaddress"])
            try:
                DeviceId = parse["Macaddress"]
                Mac = parse["MAC"]
                RSSI = parse["RSSI"]
                data = [{"MACAddress": mac, "DeviceID": DeviceId, "RSSI": rssi} for (mac, rssi) in zip(Mac, RSSI)]
                print("Count")
                print(len(data))
                print(data)
                print(curr_clock)
                finaldata = json.dumps(data)
                newHeaders = {'Content-type': 'application/json'}
                # SnifferData.pushData(data)
                r = requests.post(url="https://zig-web.com/ZIGSFirmware/api/FirmwareV2/AddMACAdress", data=finaldata,
                                  headers=newHeaders)
                pay = r.json()
                print(r.status_code)
                print(pay)

            except Exception as e:
                print("execption")
                print(e)
    elif(msg.topic == STATUS):
        print("receiving status data")
        payload = msg.payload
        parse = json.loads(payload)
        try:
            deviceId = parse["DeviceId"]
            data = {"Beaconid" : deviceId}
            r = requests.post(url="https://zig-web.com/ZIGSmartIOT/api/Firmware/Addbeaconconnectdata", data = data)
            print(deviceId)
            pay = r.json()
            print(r.status_code)
            print(pay)
        except Exception as e:
            print(e)






client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect(MQTT_SERVER, 1883, 60)
client.username_pw_set(username="Device",password="Polgara12ZED2122")
client.connect("mqtt.zig-web.com", 1883, 60)
client.loop_forever()
