#!/usr/bin/env python
from __future__ import print_function

import evdev
import select
import os

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
devices = {dev.fd: dev for dev in devices}

global vol
vol = 1
print("Volume: {0}".format(vol))


def readVolume():
    value = os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getvolume").read()
    return int(value)
def getBootVolume():
    bootvol = os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getbootvolume").read()
    return int(bootvol)
def getVolumeStep():
    volStep = os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getvolstep").read()
    return int(volStep)
def setVolume(volume, volume_step):
    os.system("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=setvolume -v="+str(min(100, max(0, volume + volume_step))))
    return min(100, max(0, volume + volume_step))
def MuteAudio():
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
                vol = setVolume(readVolume(), event.event.value * getVolumeStep())
                print("Volume: {0}".format(vol))
            elif isinstance(event, evdev.events.KeyEvent):
                if event.keycode == "KEY_ENTER" and event.keystate == event.key_up:
                    MuteAudio()
                    print("Mute-Button gedrückt")
