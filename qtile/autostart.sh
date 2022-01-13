#!/bin/sh
echo "Hello this is q-tile tiling window-manager!" | festival --tts &
picom --experimental-backends --config ~/picom/picom.sample.conf &
nitrogen --restore &
conky &
nm-applet &
