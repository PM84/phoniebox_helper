# KY-040 Rotary Encoder Support for Phoniebox

This script allows the use of a KY-040 Rotary Encoder with Linux on a Raspberry Pi to control the volume of a Phoniebox (https://github.com/MiczFlor/RPi-Jukebox-RFID).

There is a one-line installer for this script, created by Splitti (https://github.com/splitti/phoniebox_rotary_control), which sets up a service that monitors input in the background.

## Features:

Volume is adjusted when rotating by the step size entered in the Phoniebox UI.

Pressing the knob mutes the audio.
Pressing the knob again sets the volume to the boot volume (cf. Phoniebox UI)

## Materials required:

* KY-040 Rotary encoder (e.g. https://amzn.to/3ITAzuR)
* Jumper Wire Cable Female2Female (F2F) (e.g. https://amzn.to/30BBte7)
* Raspberry Pi (3; 4) (e.g. https://amzn.to/3GOBElJ)


## Install:

Add to **/boot/config.txt** three lines to the end of the file:
```
# enable rotary encoder
dtoverlay=rotary-encoder,pin_a=5,pin_b=6,relative_axis=1
dtoverlay=gpio-key,gpio=13,keycode=28,label="ENTER"
```

pin_a and pin_b mean the GPIO Pins and NOT the physical pins. Adjust these values to your needs.

Reboot your Pi:
```
sudo reboot
```

Go to the directory with rotary_control.py and run the script by
```
python3 rotary_control.py
```
The script itself does not provide any direct output. The output that can be seen is from the Phoniebox. 
Check the functionality by observing the volume setting in the Phoniebox UI. 

## Hardware Setup
![20211217_133906](https://user-images.githubusercontent.com/7900120/146546416-24b9c812-90a5-49e3-a687-e497caf94bb8.jpg)

![20211217_133722](https://user-images.githubusercontent.com/7900120/146546368-8f4df24d-c556-412e-b913-08a820b77a4c.jpg)

## Installation Process:

Insert the One-Line-Installer from https://github.com/splitti/phoniebox_rotary_control: (Stand: 17.12.2021)
```
cd; rm prc_installer.sh; wget https://raw.githubusercontent.com/splitti/phoniebox_rotary_control/master/scripts/install/prc_installer.sh; chmod +x prc_installer.sh; ./prc_installer.sh
```
![image](https://user-images.githubusercontent.com/7900120/146546938-25b71229-8333-4d69-ab8a-e4d8d1b9554b.png)

**Hit Enter**

![image](https://user-images.githubusercontent.com/7900120/146546979-81f25d52-3e11-4d21-bdeb-a568bada1857.png)

**Type => 1**

![image](https://user-images.githubusercontent.com/7900120/146547084-6a8e5f72-e593-4212-ba1a-f7e3d10cf52d.png)

**Type => 1** to reboot the pi

Check if the service is running:
```
sudo service phoniebox-rotary-control status
```

![image](https://user-images.githubusercontent.com/7900120/146547397-39d0074b-4330-4f54-8a06-52f1a70fb325.png)
