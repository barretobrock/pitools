# pitools
A Python package of Raspberry Pi specific routines primarily focused around home automation.

## Raspberry Pi Setup
### SD Card prep
 - Find Card 
    `lsblk`
 - Unmount the card
    `umount /dev/mmcblk0`
 - Wipe SD card (if not new)
    `sudo dd if=/dev/zero of=/dev/mmcblk0 bs=8192 status=progress`
 - Load Raspberry Pi image
    `sudo dd if=~/Documents/distros/2019-07-10-raspbian-buster-lite.img of=/dev/mmcblk0 conv=fsync status=progress bs=4M`
### Initial run
 - Make configurations (change pw, hostname, locale, enable SSH, etc)
    `sudo raspi-config`
    - change pw, set network, locale, enable ssh
 - Edit .bashrc to enforce locale changes
    `echo -e "\nLC_ALL=en_US.UTF-8\nLANG=en_US.UTF-8\nLANGUAGE=en_US.UTF-8" | tee -a sudo nano .bashrc`
### Environment Setup with Script
_Note: This is to prepare a Raspberry Pi device for installation of this package. This is now to supplement the requirements put in the `setup.py` file._ 

 - Install git and other requirements
```bash
# Install support components
sudo apt install git git-core python3-pip python3-dev python3-pandas python3-mysqldb python3-rpi.gpio mosquitto-clients
# Make directories for storing things
mkdir data keys logs extras
# Add in kavalkilu repo
cd ~/extras && git clone https://github.com/barretobrock/kavalkilu.git
cd ~/extras && git clone https://github.com/barretobrock/pitools.git
```
## Troubleshooting
 - ssh slow to respond
    `echo "IPQoS 0x00" | sudo tee -a /etc/ssh/sshd_config`
 - some strange error about not able to use pandas due to Import Error with `numpy`
    - This seems to only happen to the older raspis (revision 2)
    `sudo apt-get install libatlas-base-dev`
    
## Future Development & Testing
### Porting SSH & Wifi Configurations straight from SD card after writing
_Note: This was tested and failed to produce results. Will be revisited at some point._
 - card in `/media/${USER}`
 - add `/boot/wpa_supplicant.conf`:
    - setup:
    ```
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=US
    
    network={
        ssid=""
        psk=""
        key_mgmt=WPA-PSK
    }
    ```
 - add "IPQoS 0x00" to /etc/ssh/sshd_config (if possible)
 - add `/boot/ssh`
     - empty file    
### Saving configs from one card & duplicating to others
_Note: This might be abandoned, as writing to the card writes the entire card, regardless of empty space._
 - Save a compressed img from the SD card for easier distribution among all RasPis
    `sudo dd if=/dev/mmcblk0 bs=32M status=progress | gzip -c > ~/Documents/distros/2019-08-18-raspi-with-config.img.gz`
 - When duplicating to another card, use this:
    `gzip -cd < ~/Documents/distros/2019-08-18-raspi-with-config.img.gz | sudo dd of=/dev/mmcblk0 bs=32M status=progress`
 