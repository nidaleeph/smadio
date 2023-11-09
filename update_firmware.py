import json
import requests
import wget
import rarfile
import os
import time
import subprocess
import settings

update = True
newUpdate = False

def setstatus(status,type,flag):
    try:
        API_ENDPOINT = settings.API_ENDPOINT+"/set-status-updates" #IP & PORT 
        # data to be sent to api
        data = {
            'serial': getserial(),
            'status': status,
            'type': type,
            'flag': flag
        }
        # sending post request and saving response as response object
        r = requests.post(url=API_ENDPOINT, json=data)
        #r2 = requests.post(url=API_ENDPOINT2, json=data)

        # extracting response text
        response = r.text
        return response
        #response2 = r2.text

    except:
        print("Can't send to status endpoint")
        return -1

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

def checkupdate(serial,version):
    try:        
        API_ENDPOINT = settings.API_ENDPOINT+"/check-updates" #IP & PORT 
        # Data to be sent to api
        data = {
            'serial': serial,
            'version': version
        }

        # Sending post request and saving response as response object
        r = requests.post(url=API_ENDPOINT, json=data)   

        print('Request:' + API_ENDPOINT + ' Response: ' + r.text )

        # Extracting response text      
        return r.text       

    except:
        print("Failed to connect to: " +  API_ENDPOINT)
        return -1

def startupdate(firmware,flag):
    try:
        print(setstatus(0,1,flag))
        print(firmware['msg'])
        url = firmware['url']
        print(url)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        rarfile.UNRAR_TOOL = "unrar"

        if url:
            # Local path for downloaded versions
            firmware_dir = os.path.join(BASE_DIR, "firmware/versions")
            # Download link
            filename = wget.download(url,out=firmware_dir)
            if filename:
                print(setstatus(1,1,flag))
                print(filename)
                try:
                    r = rarfile.RarFile(filename)
                    r.extractall(path=BASE_DIR,pwd=firmware['rar_password'])
                    r.close()                   
                except:
                    print("Error in rar extraction")
                    return False
                print(setstatus(2,1,flag))
                print("Done update")
                global newUpdate
                newUpdate = True
                print(setstatus(3,1,flag))
                return False
            else:
                print("No file exist")
                return False
        return False

    except:
        print("Error updating")
        return True

def configure_wifi(ssid, psk, flag):
    try:
        print(setstatus(0,2,flag))
        wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
        sudo_mode = "sudo "

        with open(wpa_supplicant_conf, "r") as f:
            in_lines = f.readlines()  

        count = 0
        exist_ssid = False
        ssid_line = None
        network_line = None
        psk_line = None
        encryptedpsk_line = None
        print(setstatus(1,2,flag))
        for line in in_lines:
            if line.strip() == 'ssid="'+ssid+'"':
                print("SSID exists")
                exist_ssid = True
                network_line =  count - 1
                ssid_line = count
                psk_line = count + 1
                encryptedpsk_line = count + 2
                break
            count += 1
        
        if exist_ssid == True:
            print("Removing existing SSID")
            print([network_line,ssid_line,psk_line,encryptedpsk_line,encryptedpsk_line+1])
            with open(wpa_supplicant_conf, 'w') as f:
                # iterate each line
                for number, line in enumerate(in_lines):
                    # delete line 5 and 8. or pass any Nth line you want to remove
                    # note list index starts from 0
                    if number not in [network_line,ssid_line,psk_line,encryptedpsk_line,encryptedpsk_line+1]:
                        f.write(line)
                
        f.close()
        print(setstatus(2,2,flag))
        # write wifi config to file
        cmd = 'wpa_passphrase "{ssid}" "{psk}" | sudo tee -a {conf} > /dev/null'.format(
                ssid=str(ssid).replace('!', '\!'),
                psk=str(psk).replace('!', '\!'),
                conf=wpa_supplicant_conf
            )
        cmd_result = ""
        cmd_result = os.system(cmd)
        print (cmd + " - " + str(cmd_result))

        # reconfigure wifi
        cmd = sudo_mode + 'wpa_cli -i wlan0 reconfigure'
        cmd_result = os.system(cmd)
        print (cmd + " - " + str(cmd_result))

        time.sleep(10)  

        cmd = 'iwconfig wlan0'
        cmd_result = os.system(cmd)
        print (cmd + " - " + str(cmd_result))

        cmd = 'ifconfig wlan0'
        cmd_result = os.system(cmd)
        print (cmd + " - " + str(cmd_result))

        p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        out, err = p.communicate()

        if out:
            ip_address = out
        else:
            ip_address = "<Not Set>"

        print(ip_address)
        print(setstatus(3,2,flag))
        global newUpdate
        newUpdate = True
        return False

    except:
        print("Error configuring SSID")
        return True


def start():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # Opening JSON file
        f = open(os.path.join(BASE_DIR, 'version.json'))
        
        # returns JSON object as
        # a dictionary
        data = json.load(f)
        # Closing file
        f.close()
        # Iterating through the json
        # list
        version = data['version']
        serial = getserial()

        firmware = checkupdate(serial,version)
        url = None     

        if firmware != -1:
            firmware = json.loads(firmware)
            # -1  If there's an error, 1 Needs to be updated
            if firmware['update'] == 1:
                return startupdate(firmware,1)
            elif firmware['update'] == 2:
                return configure_wifi(firmware['ssid'],firmware['psk'],2)
            elif firmware['update'] == 3:
                if startupdate(firmware,3) == False:
                    if configure_wifi(firmware['ssid'],firmware['psk'],3) == False:
                        return False
                    else:
                        print("Error on SSID update.")
                        return True
                else:
                    print("Error on firmware update.")
                    return True
            else:
                print(firmware['msg'])
                return False
        else:  
            print("Check update failed")
            return True

    except:
        print("Error on start")
        return True


while update == True:
    update = start()
    time.sleep(5)

if newUpdate == True:
    time.sleep(5)
    print("Rebooting to implement changes...")
    os.system('sudo reboot')