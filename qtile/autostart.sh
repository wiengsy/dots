#!/usr/bin/bash
xinput --set-prop "15" "libinput Accel Profile Enabled" 0 1 0
xrandr --output HDMI-A-0 --mode 1920x1080 --rate 144
xset r rate 250 25
kitty --hold fastfetch &
#picom --daemon &
