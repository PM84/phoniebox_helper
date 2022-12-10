#!/bin/bash

recentVolPath="/home/pi/phoniebox_rotary_control/recentvolume.txt"

# while getopts c:v attribute

# do
#     case "${attribute}" in
#         v) volume=${OPTARG};;
#     esac
# done

recentVol=$(</home/pi/phoniebox_rotary_control/recentvolume.txt)
recentVol=$(($recentVol + 0))
sleep 0.5
recentVol2=$(</home/pi/phoniebox_rotary_control/recentvolume.txt)
recentVol2=$(($recentVol2 + 0))

if [[ $recentVol==$recentVol2 ]]
then
  echo "" > $recentVolPath
  sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=setvolume -v=$recentVol
fi