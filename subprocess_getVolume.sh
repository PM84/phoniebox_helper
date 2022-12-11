#!/bin/bash
# The absolute path to the folder which contains all the scripts.
# Unless you are working with symlinks, leave the following line untouched.
PATHDATA="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#############################################################
# $DEBUG TRUE|FALSE
# Read debug logging configuration file
. ${PATHDATA}/../settings/debugLogging.conf

if [ "${VOLUMEMANAGER}" == "amixer" ]; then
    # volume handling alternative with amixer not mpd (2020-06-12 related to ticket #973)
    volume=`amixer sget \'$AUDIOIFACENAME\' | grep -Po -m 1 '(?<=\[)[^]]*(?=%])'`
else
    # manage volume with mpd
    volume=$(echo -e status\\nclose | nc -w 1 localhost 6600 | grep -o -P '(?<=volume: ).*')
fi

echo $volume
