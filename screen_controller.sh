#!/bin/bash

# This file is an extension for the bash which contains the commands for
# turning the screen ond and off.
#
# $ screen on
#
# Source this file in your .bashrc to add the command permanently in your
# terminal.
#
# Copied from https://github.com/Dustin1358/Raspberry-Pi-Divera-Monitor/blob/
# 0aabfc50f5f9c01874b5b105bd9e57234da51169/.divera_commands.sh#L27-L56

# Turns the screen on and off.
function screen() {
    screen_regular $1

    # if not working, try other implementations by commenting the first version
    # and un-commenting one of the following lines

    # Version 2:
    # screen_quirky $1

    # Version 3: force HDMI port (e.g. 1 = HDMI1, 2 = HDMI2, ... )
    # screen_quirky $1 1
}

# Version 1: enables hdmi port after the screen was in standby
function screen_regular() {
       if [ $1 = on ]; then
           vcgencmd display_power 1 >/dev/null
    elif [ $1 = off ]; then
        vcgencmd display_power 0 >/dev/null
    else
        echo Unknown parameter
    fi
}

# Every screen is different and many are bad programmed. Thus, here are more
# ways for turning it on and off.
function screen_quirky() {
    if [ $1 = on ]; then
        # send cec-signal to the screen that he should wake up
        echo on 0 | cec-client -s -d 1

        if [ ! -z "$2" ]; then
            # Version 2b: if the screen turns on but at wrong input (e.g. AV1)
            # force it to switch to HDMI1 port. This works only if the screen
            # is on already therefore send it a few times in a row.

            # 4F:82:10:00 is HDMI1
            # 4F:82:20:00 is HDMI2
            # 4F:82:30:00 is HDMI3 and so on
            HDMI_port=$(( $2 * 10 ))
            HDMI=4F:82:$HDMI_port:00

            # Attention this is an unoffical cec-signal which may not work with
            # your screen.
            echo tx $HDMI | cec-client -s -d 1
            echo tx $HDMI | cec-client -s -d 1
            echo tx $HDMI | cec-client -s -d 1
            echo tx $HDMI | cec-client -s -d 1
            echo tx $HDMI | cec-client -s -d 1
            echo tx $HDMI | cec-client -s -d 1
        fi
    elif [ $1 = off ]; then
        echo standby 0 | cec-client -s -d 1
    else
        echo Unknown parameter
    fi
}
