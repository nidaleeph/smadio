import serial
import requests
import struct
import time
import sys
import settings

windportno = 0 #windows port no initial 0
portno = 0 #raspberry port no initial 0
usb_port="/dev/ttyUSB0" # usb uart for for linux
from requests.exceptions import ConnectionError

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

def serialconnect(ser):
    while(1):
        try:
            bytes = ser.readline()
            byte_arr=repr(bytes).split('\\') #repr for backlash splitting
            if bytes == b'':
                continue
            print("Initial Bytes")
            print(byte_arr)
            if byte_arr[1] == "x00'":
                print("Device Connected")
            if byte_arr[1] == "x88" or byte_arr[1] == "x89" or byte_arr[1] == "x87": #command 1st byte
                if byte_arr[1] == "x88":
                    command = "Call"  
                elif byte_arr[1] == "x89":
                    command = "Cancel"
                elif byte_arr[1] == "x87":
                    command = "Bill"         
                user_code = byte_arr[2]
                if user_code == "x01":
                    user_code = "Currently Not Used"
                bell_group_no = byte_arr[3]
                if 'A' in bell_group_no:
                    bell_group_no = bell_group_no.replace('A', '')
                    byte_arr.append(byte_arr[6])
                    byte_arr[6] = 'A'
                    byte_arr[3] = bell_group_no
                elif 'B' in bell_group_no:
                    bell_group_no = bell_group_no.replace('B', '')
                    byte_arr.append(byte_arr[6])
                    byte_arr[6] = 'B'
                    byte_arr[3] = bell_group_no
                elif 'C' in bell_group_no:
                    bell_group_no = bell_group_no.replace('C', '')
                    byte_arr.append(byte_arr[6])
                    byte_arr[6] = 'C'
                    byte_arr[3] = bell_group_no
                elif 'D' in bell_group_no:
                    bell_group_no = bell_group_no.replace('D', '')
                    byte_arr.append(byte_arr[6])
                    byte_arr[6] = 'D'
                    byte_arr[3] = bell_group_no                                                                      
                elif 'E' in bell_group_no:
                    bell_group_no = bell_group_no.replace('E', '')
                    byte_arr.append(byte_arr[6])
                    byte_arr[6] = 'E'
                    byte_arr[3] = bell_group_no
                elif 'F' in bell_group_no:
                    bell_group_no = bell_group_no.replace('F', '')
                    byte_arr.append(byte_arr[6])
                    byte_arr[6] = 'F'
                    byte_arr[3] = bell_group_no
                elif 'H' in bell_group_no:
                    bell_group_no = bell_group_no.replace('H', '')
                    byte_arr.append(byte_arr[6])
                    byte_arr[6] = 'H'
                    byte_arr[3] = bell_group_no
                elif 'L' in bell_group_no:
                    bell_group_no = bell_group_no.replace('L', '')
                    byte_arr.append(byte_arr[6])
                    byte_arr[6] = 'L'
                    byte_arr[3] = bell_group_no
                elif 'N' in bell_group_no:
                    bell_group_no = bell_group_no.replace('N', '')
                    byte_arr.append(byte_arr[6])
                    byte_arr[6] = 'N'
                    byte_arr[3] = bell_group_no
                elif 'O' in bell_group_no:
                    bell_group_no = bell_group_no.replace('O', '')
                    byte_arr.append(byte_arr[6])
                    byte_arr[6] = 'O'
                    byte_arr[3] = bell_group_no
                elif 'P' in bell_group_no:
                    bell_group_no = bell_group_no.replace('P', '')
                    byte_arr.append(byte_arr[6])
                    byte_arr[6] = 'P'
                    byte_arr[3] = bell_group_no
                elif 'Q' in bell_group_no:
                    bell_group_no = bell_group_no.replace('Q', '')
                    byte_arr.append(byte_arr[6])
                    byte_arr[6] = 'Q'
                    byte_arr[3] = bell_group_no
                new_bellgroup = "\\" + bell_group_no
                encodedbell = new_bellgroup.encode('utf-8')
                doubleencodedbell = encodedbell.decode('unicode-escape').encode('ISO-8859-1')
                new_bellgroupno = int.from_bytes(doubleencodedbell, byteorder=sys.byteorder)
                bell_group_no = str(new_bellgroupno)
                print("BellGroupNo: "+bell_group_no)
                character_code = byte_arr[4]
                hundreds = byte_arr[5]
                tens = byte_arr[6]
                if tens == "x00" or tens == "x01" or tens == "x02" or tens == "x03" or tens == "x04" or tens == "x05" or tens == "x06" or tens == "x07" or tens == "x08" or tens == "x09" or tens == "t":
                    new_tens = "\\" + tens
                    encodedtens = new_tens.encode('utf-8')
                    doubleencodedtens = encodedtens.decode('unicode-escape').encode('ISO-8859-1')
                    newtens = int.from_bytes(doubleencodedtens, byteorder=sys.byteorder)
                    tens = str(newtens)
                ones = byte_arr[7]
                if "'" in ones:
                    ones = ones.replace("'", '')
                    new_ones = "\\" + ones
                    encodedones = new_ones.encode('utf-8')
                    doubleencodedones = encodedones.decode('unicode-escape').encode('ISO-8859-1')
                    newones = int.from_bytes(doubleencodedones, byteorder=sys.byteorder)
                    ones = str(newones)
                else:
                    new_ones = "\\" + ones
                    encodedones = new_ones.encode('utf-8')
                    doubleencodedones = encodedones.decode('unicode-escape').encode('ISO-8859-1')
                    newones = int.from_bytes(doubleencodedones, byteorder=sys.byteorder)
                    ones = str(newones)
                counter = (tens+""+ones)
                print("Counter is: "+counter)
                print("Final Bytes")
                print(byte_arr)
                
                #API ENDPOINT IP AND PORT
                API_ENDPOINT = settings.NODE_ENDPOINT+"/8FvqTo7XYr/smadio" #IP & PORT 
                
                # data to be sent to api
                data = {
                    'command': command,
                    'user_code': user_code,
                    'counter': counter,
                    'bellGroupNo' : bell_group_no, 
                    'port_used': usb_port,
                    'serialNo': getserial()                
                }
                # sending post request and saving response as response object
                r = requests.post(url=API_ENDPOINT, json=data)
                #r2 = requests.post(url=API_ENDPOINT2, json=data)

                # extracting response text
                response = r.text
                #response2 = r2.text
                print("response: " + response)
                #print("response: " + response + "response2 :" + response2)
        except (serial.SerialException):
            print("Serial Error")
            break
        except :
            print("Can't connect to API")
                    
while (1):
    try: 
        #enabled serial communication in usb port
        ser = serial.Serial(port=usb_port, baudrate=9600, bytesize=8, parity='N',stopbits=1, timeout=0.1)
        ser.rts = 0 #off to disable RTS control flow
        ser.xonxoff = 0
        ser.dts = 0        
        serialconnect(ser)
    #Find what port is used in raspberry or windows                   
    except (serial.SerialException): 
        print("Cant Detect a usb com port")
        print(usb_port)
        if portno < 33:
            strportno = str(portno)
            usb_port = "/dev/ttyUSB" +strportno
            portno = portno + 1
        elif portno >= 33:
            strwindportno = str(windportno)
            usb_port = "COM" +strwindportno 
            windportno = windportno + 1
            if windportno > 20:
                windportno = 0
                portno = 0