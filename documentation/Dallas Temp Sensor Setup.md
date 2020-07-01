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
 - `sudo modprobe w1_gpio`
 - `sudo modprobe w1_therm`
 - `ls /sys/bus/w1/devices`
 
## Troubleshooting
 - If you get an error about `w1-gpio` not being found, add this in /boot/config.txt:
    `dtoverlay=w1-gpio,gpiopin=<your-data-pin-bcm>`

