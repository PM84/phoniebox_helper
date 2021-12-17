# KY-040 Rotary Encoder Support for Phoniebox

This script allows the use of a KY-040 Rotary Encoder with Linux on a Raspberry Pi to control the volume of a Phoniebox (https://github.com/MiczFlor/RPi-Jukebox-RFID).

There is a one-line installer for this script, created by Splitti (https://github.com/splitti/phoniebox_rotary_control), which sets up a service that monitors input in the background.

## Functions:

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

Run the script py
```
python3 rotary_control.py
```
