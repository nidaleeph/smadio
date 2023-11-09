import os

# Delete the firmware files 
cmd = 'sudo rm -r /home/pi/smadio/firmware/versions/*'
os.system(cmd)

# Delete the log files 
cmd = 'sudo rm -r /home/pi/logs/*'
os.system(cmd)

