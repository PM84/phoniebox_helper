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
from subprocess import Popen

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
devices = {dev.fd: dev for dev in devices}

global maxVol
global bootVol
global volStep
maxVol = -1
bootVol = -1
volStep = -1

def readVolume():
    try:
        # Versuche zunächst amixer (direkter Zugriff)
        value = os.popen("amixer get PCM | grep -o '[0-9]*%' | head -1 | tr -d '%'").read().strip()
        if value and value.isdigit():
            return int(value)

        # Fallback auf mpd
        value = os.popen("mpc volume | grep -o '[0-9]*%' | tr -d '%'").read().strip()
        if value and value.isdigit():
            return int(value)

        # Letzter Fallback auf original script
        value = os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getvolume").read().strip()
        if value and value.isdigit():
            return int(value)
        else:
            print(f"Ungültiger Lautstärkewert gelesen: '{value}'")
            return 50  # Standardwert falls der gelesene Wert ungültig ist
    except Exception as e:
        print(f"Fehler beim Lesen der Lautstärke: {e}")
        return 50
def getBootVolume():
    global bootVol
    if bootVol > 0:
        return bootVol
    else:
        try:
            value = os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getbootvolume").read().strip()
            if value and value.isdigit():
                bootVol = int(value)
            else:
                print(f"Ungültiger Boot-Lautstärkewert: '{value}'")
                bootVol = 75  # Standardwert
            return bootVol
        except Exception as e:
            print(f"Fehler beim Lesen der Boot-Lautstärke: {e}")
            bootVol = 75
            return bootVol
def getVolumeStep():
    global volStep
    if volStep > 0:
        return volStep
    else:
        try:
            value = os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getvolstep").read().strip()
            if value and value.isdigit():
                volStep = int(value)
            else:
                print(f"Ungültiger Lautstärke-Schritt-Wert: '{value}'")
                volStep = 3  # Standardwert
            return volStep
        except Exception as e:
            print(f"Fehler beim Lesen des Lautstärke-Schritts: {e}")
            volStep = 3
            return volStep
def getMaxVolume():
    global maxVol
    if maxVol > 0:
        return maxVol
    else:
        try:
            value = os.popen("sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=getmaxvolume").read().strip()
            if value and value.isdigit():
                maxVol = int(value)
            else:
                print(f"Ungültiger Max-Lautstärkewert: '{value}'")
                maxVol = 100  # Standardwert
            return maxVol
        except Exception as e:
            print(f"Fehler beim Lesen der maximalen Lautstärke: {e}")
            maxVol = 100
            return maxVol
def setVolume(volume, volume_step):
    try:
        maxVol = getMaxVolume()
        # Validierung der Eingabewerte
        if not isinstance(volume, (int, float)) or not isinstance(volume_step, (int, float)):
            print(f"Ungültige Werte: volume={volume}, volume_step={volume_step}")
            return volume

        # Berechnung des neuen Lautstärkewerts
        recentVol = min(maxVol, max(0, int(volume + volume_step)))

        # Zusätzliche Validierung des berechneten Werts
        if not (0 <= recentVol <= 100):
            print(f"Lautstärkewert außerhalb des gültigen Bereichs: {recentVol}")
            recentVol = max(0, min(100, recentVol))

        # Primärer Versuch: Lokales subprocess_setVolume.sh verwenden (ohne Bash-Fehler)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess_script = os.path.join(script_dir, "subprocess_setVolume.sh")

        if os.path.exists(subprocess_script):
            try:
                result = subprocess.run([subprocess_script, '-v', str(recentVol)], check=True, capture_output=True, text=True)
                print(f"Lautstärke erfolgreich mit lokalem Script gesetzt auf: {recentVol}")
                if result.stdout:
                    print(f"Script-Output: {result.stdout.strip()}")
            except subprocess.CalledProcessError as e:
                print(f"Lokales Script fehlgeschlagen: {e}")
                print(f"Versuche Fallback auf playout_controls.sh...")

                # Fallback: Original playout_controls.sh (mit möglichen Bash-Fehlern)
                cmd = f"sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=setvolume -v={recentVol}"
                result = os.system(cmd)
                if result == 0:
                    print(f"Lautstärke mit Fallback-Script gesetzt auf: {recentVol}")
                else:
                    print(f"Auch Fallback fehlgeschlagen (Code: {result})")
        else:
            print(f"Lokales Script nicht gefunden: {subprocess_script}")
            print(f"Verwende Original playout_controls.sh als Fallback...")
            cmd = f"sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=setvolume -v={recentVol}"
            result = os.system(cmd)
            if result == 0:
                print(f"Lautstärke mit Original-Script gesetzt auf: {recentVol}")
            else:
                print(f"Original-Script fehlgeschlagen (Code: {result})")

        return recentVol
    except Exception as e:
        print(f"Fehler beim Setzen der Lautstärke: {e}")
        return volume
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
                    current_vol = readVolume()
                    vol_step = getVolumeStep()
                    vol_change = event.event.value * vol_step
                    print(f"Volume change: current={current_vol}, step={vol_step}, change={vol_change}")
                    setVolume(current_vol, vol_change)
                elif isinstance(event, evdev.events.KeyEvent):
                    if event.keycode == "KEY_ENTER" and event.keystate == event.key_up:
                        print("Mute/Unmute triggered")
                        MuteUnmuteAudio()
finally:
    rt.stop()