# Dallas Temp Sensor Setup
## Assembly
```
 _____
/     \ <- Rounded area pointing out, flat facing in
-------
|     |
_______
|  |  |
|  |  |
|  ****  <- 4.7K or 10K resistor
|  |  |
G  D  V
```
## Programming
 - `sudo nano /boot/config.txt`
    Add `dtoverlay=w1–gpio` to the bottom of the file
 - reboot the pi
 - Verify that 1-Wire kernel modules have been loaded on the next boot
    `lsmod | grep -i w1_`
 - `sudo modprobe w1–gpio`
 - `sudo modprobe w1-therm`
 - `cd /sys/bus/w1/devices`

