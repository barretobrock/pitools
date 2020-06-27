#!/usr/bin/env bash

# RASPBERRY PI SETUP
# ---
# FILE PATHS

# VARIABLES
read -p "Enter the hostname of this machine: " NEWHOSTNAME

# Import common functions
source ./common.sh

# Configure agent for raspberry pi src:
# https://www.raspberrypi.org/forums/viewtopic.php?t=21632
sudo raspi-config nonint do_hostname ${NEWHOSTNAME} # Set hostname
#sudo raspi-config nonint do_expand_rootfs   # Expand filesystem
sudo raspi-config nonint do_boot_behaviour B1 # Boot into CLI
sudo raspi-config nonint do_ssh 0  # Set SHH on = 0
sudo raspi-config nonint do_memory_split 16 # Set mem to smallest amt
sudo raspi-config nonint do_wifi_country "yourcountry" # Set WiFi country
#sudo raspi-config nonint list_wlan_interfaces
# Change password
echo \"${SUDO_USER}:%s\" | chpasswd


# Allow for faster response in SSH
# Add "IPQoS 0x00" to /etc/ssh/sshd_config
echo "IPQoS 0x00" | sudo tee -a /etc/ssh/sshd_config

# Edit .bashrc to enforce locale changes
echo -e "\nLC_ALL=en_US.UTF-8\nLANG=en_US.UTF-8\nLANGUAGE=en_US.UTF-8" | sudo tee -a .bashrc

# Update packages
sudo apt update && sudo apt upgrade
# Install major python dependencies
sudo apt install git git-core python3-pip python3-dev python3-pandas python3-rpi.gpio \
    python3-serial wiringpi

# Create directories
mkdir data keys logs extras

# Clone kavalkilu to home dir
git clone https://github.com/barretobrock/pitools.git ~/extras/pitools/

# To run some of the scripts, bash is recommended over dash.
#   To reconfigure `sh` to point to bash, run this
sudo dpkg-reconfigure dash

# Locale fixing
echo -e "LANGUAGE=en_US.UTF-8\nLC_ALL=en_US.UTF-8\nLC_TIME=en_US.UTF-8\nLANG=en_US.UTF-8" | sudo tee /etc/default/locale
. /etc/default/locale

# Store git credentials to avoid prompt
#echo "Beginning git credential storage"
#git config --global credential.helper store
#cd kavalkilu && git pull

echo "Setup complete."