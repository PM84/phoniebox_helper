#!/usr/bin/env python

# Codebase from: https://blog.ploetzli.ch/2018/ky-040-rotary-encoder-linux-raspberry-pi/
# Adapted to Phoniebox Volume Control by Peter Mayer; https://github.com/PM84/phoniebox_helper.git

# === Install:
# Add to /boot/config.txt three lines:
# # enable rotary encoder
# dtoverlay=rotary-encoder,pin_a=23,pin_b=24,relative_axis=1
# dtoverlay=gpio-key,gpio=22,keycode=28,label="ENTER"
# 
# pin_a and pin_b mean the GPIO Pins and NOT the physical pins. Adjust these values to your needs.
#
# Reboot your Pi.
#
# Run the script py
# python3 rotary_control.py

from __future__ import print_function

import evdev
import select
import os

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
devices = {dev.fd: dev for dev in devices}

def readVolume():
    value = os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getvolume").read()
    return int(value)
def getBootVolume():
    bootvol = os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getbootvolume").read()
    return int(bootvol)
def getVolumeStep():
    volStep = os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getvolstep").read()
    return int(volStep)
def getMaxVolume():
    maxVol = os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getmaxvolume").read()
    return int(maxVol)
def setVolume(volume, volume_step):
    maxVol = getMaxVolume()
    os.system("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=setvolume -v="+str(min(maxVol, max(0, volume + volume_step))))
    return min(maxVol, max(0, volume + volume_step))
def MuteUnmuteAudio():
    if readVolume() > 1:
        os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=mute")
    else:
        os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=setvolume -v="+str(getBootVolume()))

done = False
while not done:
    r, w, x = select.select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
            event = evdev.util.categorize(event)
            if isinstance(event, evdev.events.RelEvent):
                setVolume(readVolume(), event.event.value * getVolumeStep())
            elif isinstance(event, evdev.events.KeyEvent):
                if event.keycode == "KEY_ENTER" and event.keystate == event.key_up:
                    MuteUnmuteAudio()