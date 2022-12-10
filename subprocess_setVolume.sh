#!/bin/bash

recentVolPath="/home/pi/phoniebox_rotary_control/recentvolume.txt"

while getopts v: attribute

do
    case "${attribute}" in
        v) volume=${OPTARG};;
    esac
done

recentVol=$(</home/pi/phoniebox_rotary_control/recentvolume.txt)
if [[ $recentVol!=$volume ]]
then
  echo $volume > $recentVolPath
fi
recentVol=$(($volume + 0))
sleep 0.5
# recentVol2=$(</home/pi/phoniebox_rotary_control/recentvolume.txt)
recentVol2=$(($volume + 0))

if [[ $recentVol==$recentVol2 ]]
then
  echo "" > $recentVolPath
  sudo /home/pi/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=setvolume -v=$recentVol
fi