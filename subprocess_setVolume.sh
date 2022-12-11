#!/bin/bash
# The absolute path to the folder which contains all the scripts.
# Unless you are working with symlinks, leave the following line untouched.
PATHDATA="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#############################################################
# $DEBUG TRUE|FALSE
# Read debug logging configuration file
. ${PATHDATA}/../settings/debugLogging.conf

while getopts v: attribute

do
    case "${attribute}" in
        v) volume=${OPTARG};;
    esac
done

# set volume level in percent
if [ "${VOLUMEMANAGER}" == "amixer" ]; then
  # volume handling alternative with amixer not mpd (2020-06-12 related to ticket #973)
  amixer sset \'$AUDIOIFACENAME\' $volume%
else
  # manage volume with mpd
  echo -e setvol $volume\\nclose | nc -w 1 localhost 6600
fi
