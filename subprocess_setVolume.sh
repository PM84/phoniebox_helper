#!/bin/bash

recentVolPath = "/home/pi/phoniebox_rotary_control/recentvolume"

# while getopts c:v attribute

# do
#     case "${attribute}" in
#         v) volume=${OPTARG};;
#     esac
# done

recentVol="`cat $recentVolPath`"
sleep 0.5
recentVol2="`cat $recentVolPath`"


if [[ $recentVol == recentVol2 ]]
then
  echo "" > $recentVolPath
  sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=setVolume -v=$recentVol
fi