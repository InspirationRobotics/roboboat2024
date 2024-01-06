#!/bin/bash

# Iterate through USB devices in /sys/bus/usb/devices/usb*/
for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
    (
        # Extract the system path by removing the trailing "/dev"
        syspath="${sysdevpath%/dev}"

        # Get the device name using udevadm info
        devname="$(udevadm info -q name -p $syspath)"

        # Check if the device name starts with "bus/"; if so, skip the iteration
        [[ "$devname" == "bus/"* ]] && exit

        # Export device properties using udevadm info
        eval "$(udevadm info -q property --export -p $syspath)"

        # Check if ID_PATH or ID_SERIAL is empty; if either is empty, skip the iteration
        [[ -z "$ID_PATH" || -z "$ID_SERIAL" ]] && exit

        # Print device information: /dev/$devname - $ID_PATH - $ID_SERIAL
        echo "/dev/$devname - $ID_PATH - $ID_SERIAL"
    )
done
