#!/bin/bash

# Install raspi-config to expand filesystem (20160619)
# Created By - Anton

# Update the sysatem and install dependencies
apt-get update && apt-get -y upgrade && apt-get  install libfftw3-double3 alsa-utils

wget http://http.us.debian.org/debian/pool/main/t/triggerhappy/triggerhappy_0.4.0-1_armhf.deb
wget http://http.us.debian.org/debian/pool/main/l/lua5.1/lua5.1_5.1.5-8_armhf.deb
wget http://archive.raspberrypi.org/debian/pool/main/r/raspi-config/raspi-config_20160506_all.deb

dpkg -i triggerhappy_0.4.0-1_armhf.deb
dpkg -i lua5.1_5.1.5-8_armhf.deb
dpkg -i raspi-config_20160506_all.deb

# Run raspi-config
raspi-config

exit 0