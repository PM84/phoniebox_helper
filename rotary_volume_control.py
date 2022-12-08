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
from threading import Timer

import evdev
import select
import os
import subprocess

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
devices = {dev.fd: dev for dev in devices}
global recentVolFile
recentVolFile = "/home/pi/phoniebox_rotary_control/recentvolume"

global maxVol
global bootVol
global volStep
maxVol = -1
bootVol = -1
volStep = -1

def readVolume():
    global recentVolFile
    f = open(recentVolFile, "r")
    recentVol = int(f.read())
    f.close()
    if recentVol > 0:
        return recentVol
    else:
        value = os.popen("sudo $(echo -e status\\nclose | nc -w 1 localhost 6600 | grep -o -P '(?<=volume: ).*')").read()
        return value
def getBootVolume():
    global bootVol
    if bootVol > 0:
        return bootVol
    else:
        bootVol = int(os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getbootvolume").read())
        return bootVol
def getVolumeStep():
    global volStep
    if volStep > 0:
        return volStep
    else:
        volStep = int(os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getvolstep").read())
        return volStep
def getMaxVolume():
    global maxVol
    if maxVol>0:
        return maxVol
    else:
        maxVol = int(os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getmaxvolume").read())
        return maxVol
def setVolume(volume, volume_step):
    global recentVolFile
    maxVol = getMaxVolume()
    recentVol = min(maxVol, max(0, volume + volume_step))
    f = open(recentVolFile, "w")
    f.write(recentVol);
    f.close()
    subprocess.popen("sudo /home/pi/phoniebox_rotary_control/scripts/controller/subprocess_setVolume.sh")
    return recentVol
def MuteUnmuteAudio():
    if readVolume() > 1:
        os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=mute")
    else:
        os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=setvolume -v="+str(getBootVolume()))

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def checkForConfigurationChange():
    getVolumeStep()
    getMaxVolume()
    getBootVolume()

rt = RepeatedTimer(60, checkForConfigurationChange)
try:
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
finally:
    rt.stop()