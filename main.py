import serial
import requests
import time
usb_port="/dev/ttyUSB0" # usb uart for for linux
from requests.exceptions import ConnectionError
def serialconnect(ser):
    while(1):
        try:
            bytes = ser.readline()
            byte_arr=repr(bytes).split('\\') #repr for backlash splitting
            if bytes == b'':
                continue
            if byte_arr[0] == "x00":
                command = "Booting"
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
                if bell_group_no == "x00": # bell group not yet defined
                    bell_group_no = "Default 0: Not Set"
                character_code = byte_arr[4]
                hundreds = byte_arr[5]
                tens = byte_arr[6]
                if tens == "x00":
                    tens = "0"
                elif tens == "x01":
                    tens = "1"
                elif tens == "x02":
                    tens = "2"
                elif tens == "x03":
                    tens = "3"
                elif tens == "x04":
                    tens = "4"
                elif tens == "x05":
                    tens = "5"
                elif tens == "x06":
                    tens = "6"
                elif tens == "x07":
                    tens = "7"
                elif tens == "x08":
                    tens = "8"
                elif tens == "x09":
                    tens = "9"
                ones = byte_arr[7]
                if ones == "x00'" or ones == "x00":
                    ones = "0"
                elif ones == "x01'" or ones ==  "x01":
                    ones = "1"
                elif ones == "x02'" or ones == "x02":
                    ones = "2"
                elif ones == "x03'" or ones == "x03":
                    ones = "3"
                elif ones == "x04'" or ones == "x04":
                    ones = "4"
                elif ones == "x05'" or ones == "x05":
                    ones = "5"
                elif ones == "x06'" or ones == "x06":
                    ones = "6"
                elif ones == "x07'" or ones == "x07":
                    ones = "7"
                elif ones == "x08'" or ones == "x08":
                    ones = "8"
                elif ones == "x09'" or ones == "x09":
                    ones = "9"

                counter = (tens+""+ones)
                #print(command + " " + user_code + " " + bell_group_no + " " + counter)
                API_ENDPOINT = "http://160.16.65.181:9191/8FvqTo7XYr/smadio"

                # data to be sent to api
                data = {
                    'command': command,
                    'user_code': user_code,
                    'counter': counter,
                    'Port Used': usb_port
                }

                # sending post request and saving response as response object
                r = requests.post(url=API_ENDPOINT, data=data)

                # extracting response text
                response = r.text
                print("response: " + response)
        except (serial.SerialException):
            print("Serial Error")
            break
        except :
            print("Can't connect to API")
                    
while (1):
    try: 
        #enabled serial communication in usb port
        ser = serial.Serial(port=usb_port, baudrate=9600, bytesize=8, parity='N',
                            stopbits=1, timeout=0.1)
        ser.rts = 0 #off to disable RTS control flow
        ser.xonxoff = 0
        ser.dts = 0
        
        serialconnect(ser)
                
                
    except (serial.SerialException): 
        print("Cant Detect a usb com port")
        print(usb_port)
        if usb_port=="/dev/ttyUSB0":
            usb_port = "/dev/ttyUSB1"
        elif usb_port=="/dev/ttyUSB1":
            usb_port = "/dev/ttyUSB2"
        elif usb_port=="/dev/ttyUSB2":
            usb_port = "/dev/ttyUSB3"
        elif usb_port=="/dev/ttyUSB3":
            usb_port = "/dev/ttyUSB4"
        elif usb_port=="/dev/ttyUSB4":
            usb_port = "/dev/ttyUSB5"
        elif usb_port=="/dev/ttyUSB5":
            usb_port = "/dev/ttyUSB6"
        elif usb_port=="/dev/ttyUSB6":
            usb_port = "/dev/ttyUSB7"
        elif usb_port=="/dev/ttyUSB7":
            usb_port = "/dev/ttyUSB8"
        elif usb_port=="/dev/ttyUSB8":
            usb_port = "/dev/ttyUSB9"
        elif usb_port=="/dev/ttyUSB9":
            usb_port = "/dev/ttyUSB10"
        elif usb_port=="/dev/ttyUSB10":
            usb_port = "/dev/ttyUSB11"
        elif usb_port=="/dev/ttyUSB11":
            usb_port = "/dev/ttyUSB12"
        elif usb_port=="/dev/ttyUSB12":
            usb_port = "/dev/ttyUSB13"
        elif usb_port=="/dev/ttyUSB13":
            usb_port = "/dev/ttyUSB14"
        elif usb_port=="/dev/ttyUSB14":
            usb_port = "/dev/ttyUSB15"
        elif usb_port=="/dev/ttyUSB15":
            usb_port = "/dev/ttyUSB16"
        elif usb_port=="/dev/ttyUSB16":
            usb_port = "/dev/ttyUSB17"
        elif usb_port=="/dev/ttyUSB17":
            usb_port = "/dev/ttyUSB18"
        elif usb_port=="/dev/ttyUSB18":
            usb_port = "/dev/ttyUSB19"
        elif usb_port=="/dev/ttyUSB19":
            usb_port = "/dev/ttyUSB20"
        elif usb_port=="/dev/ttyUSB20":
            usb_port = "/dev/ttyUSB21"
        elif usb_port=="/dev/ttyUSB21":
            usb_port = "/dev/ttyUSB22"
        elif usb_port=="/dev/ttyUSB22":
            usb_port = "/dev/ttyUSB23"
        elif usb_port=="/dev/ttyUSB23":
            usb_port = "/dev/ttyUSB24"
        elif usb_port=="/dev/ttyUSB24":
            usb_port = "/dev/ttyUSB25"
        elif usb_port=="/dev/ttyUSB25":
            usb_port = "/dev/ttyUSB26"
        elif usb_port=="/dev/ttyUSB26":
            usb_port = "/dev/ttyUSB27"
        elif usb_port=="/dev/ttyUSB27":
            usb_port = "/dev/ttyUSB28"
        elif usb_port=="/dev/ttyUSB28":
            usb_port = "/dev/ttyUSB29"
        elif usb_port=="/dev/ttyUSB29":
            usb_port = "/dev/ttyUSB30"
        elif usb_port=="/dev/ttyUSB30":
            usb_port = "/dev/ttyUSB31"
        elif usb_port=="/dev/ttyUSB31":
            usb_port = "/dev/ttyUSB32"
        elif usb_port=="/dev/ttyUSB32":
            usb_port = "COM4" #default first uart for windows
        elif usb_port=="COM4":
            usb_port = "COM9" #2nd uart for windows
        else:
            usb_port="/dev/ttyUSB0"
        

