import requests
import time
import settings

def getserial():
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial

while (1):
    try:
        API_ENDPOINT = settings.NODE_ENDPOINT+"/8FvqTo7XYr/smadio/heartbeat" #IP & PORT 
        # data to be sent to api
        data = {
            'serialNo': getserial()     
        }
        # sending post request and saving response as response object
        r = requests.post(url=API_ENDPOINT, json=data)
        #r2 = requests.post(url=API_ENDPOINT2, json=data)

        # extracting response text
        response = r.text
        #response2 = r2.text
        print("Heartbeat sent with response: " + response)

    except:
        print("Can't send heartbeat to: " + API_ENDPOINT)

    time.sleep(30)