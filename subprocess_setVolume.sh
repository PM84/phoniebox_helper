#!/bin/bash
# The absolute path to the folder which contains all the scripts.
# Unless you are working with symlinks, leave the following line untouched.
PATHDATA="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#############################################################
# Debug-Konfiguration
DEBUG="FALSE"  # Kann auf TRUE gesetzt werden für Debug-Ausgaben

while getopts v: attribute
do
    case "${attribute}" in
        v) volume=${OPTARG};;
    esac
done

# Validierung des Lautstärkewerts
if [ -z "${volume}" ] || ! [[ "${volume}" =~ ^[0-9]+$ ]]; then
    echo "Fehler: Ungültiger Lautstärkewert: '${volume}'"
    exit 1
fi

# Begrenzung auf gültigen Bereich
if [ "${volume}" -lt 0 ]; then
    volume=0
elif [ "${volume}" -gt 100 ]; then
    volume=100
fi

echo "Setze Lautstärke auf: ${volume}%"

# Fallback-Konfiguration wenn VOLUMEMANAGER nicht gesetzt ist
if [ -z "${VOLUMEMANAGER}" ]; then
    VOLUMEMANAGER="mpd"  # Standard auf mpd setzen
fi

# set volume level in percent
if [ "${VOLUMEMANAGER}" == "amixer" ]; then
  # volume handling alternative with amixer not mpd (2020-06-12 related to ticket #973)
  # Fallback für AUDIOIFACENAME wenn nicht gesetzt
  if [ -z "${AUDIOIFACENAME}" ]; then
      AUDIOIFACENAME="PCM"  # Standard Audio Interface
  fi
  amixer sset "${AUDIOIFACENAME}" ${volume}%
else
  # manage volume with mpd
  echo -e setvol $volume\\nclose | nc -w 1 localhost 6600
fi
