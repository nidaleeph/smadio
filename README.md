# Raspberry Installation
Step 1. Download and Install Raspberry PI imager
Download link: https://downloads.raspberrypi.org/imager/imager_latest.exe

Step 2. Under Operating System Click Choose Os button Then Locate Erase to format your SD card to Fat32

Step 3. Select Choose Os button and locate Raspberry Pi OS (Other) and download Raspberry Pi OS full (32 Bit Version)

-optional or Choose Use custom .Img from your computer by downloading the latest Rasbian OS

Download link: https://downloads.raspberrypi.org/raspios_full_armhf/images/raspios_full_armhf-2022-04-07/2022-04-04-raspios-bullseye-armhf-full.img.xz

# Disabling the Raspberry GUI for faster Reload
Step 1. Using the Terminal. Type sudo raspi-config

Step 2. Go to 1. system options -> s5. Boot/auto login -> And Select B2. Console Autologin then click finish and wait for boot. Or Manualy Reboot by typing sudo reboot

# Downloading all python library needed. Run this command Below
sudo apt install update
sudo apt-get install bluez-tools
sudo apt-get install git

sudo pip install rarfile
sudo pip install wget
sudo apt-get install unrar-free

sudo su
pip install rarfile
pip install wget
apt-get install unrar-free

# Then reboot the raspberry
sudo reboot

# Cloning the smadio repository 
Step 1. Go to /home/pi directoy

Step 2. Type 
git clone https://git.teratomo.com/bkarlo/smadio.git

Step 3. Grant all permission to your smadio folder. go back to /home/pi directory and type 
sudo chmod 777 -R smadio 

# Automate the python Script Using Crontab
Step 1. make a directory for log file by typing 
mkdir /home/pi/logs

Step 2. allow all permission to the logs folder by typing
sudo chmod 777 -R /home/pi/logs

Step 3. Edit Crontab by typing
crontab -e

# add this commannds to the last line
@reboot sleep 10 && sudo python /home/pi/smadio/update_firmware.py > /home/pi/logs/update.txt 2>&1
@reboot sudo python /home/pi/smadio/heartbeat.py > /home/pi/logs/heartbeat.txt 2>&1
@reboot sudo python /home/pi/smadio/main.py > /home/pi/logs/main.txt 2>&1

Step 4. Then Reboot Rasbperry PI


# Renaming of raspberry pi to Teraiot 
Step 1. sudo nano  /etc/hostname 
edit name from raspberrypi to Teraiot 
# sudo nano /etc/hosts
edit host to from rasbperrypi to Teraiot

# Then Reboot Rasberry PI
sudo reboot

# To get Rasbperry Serial Run This code by typing
sudo python /home/pi/smadio/getserial.py



# For Bluetooth Development [STILL UNDER WORKING PROGRESS]
# make /etc/systemd/system/bt-agent.service and add the codes bleow
[Unit]
Description=Bluetooth Auth Agent
After=bluetooth.service
PartOf=bluetooth.service

[Service]
Type=simple
ExecStart=/usr/bin/bt-agent -c NoInputNoOutput -p /home/pi/smadio/bluetoothpin.conf

[Install]
WantedBy=bluetooth.target

# automate systemd bt-agent on boot by typing this commands
sudo systemctl daemon-reload
sudo systemctl enable bt-agent
sudo systemctl restart bt-agent
sudo systemctl status bt-agent.service 
#
# add to /home/pi/.bashrc last line
/bin/sleep 10 && sudo hciconfig hci0 piscan && sudo hciconfig hci0 sspmode 0 && echo "Bluetooth Enable"

