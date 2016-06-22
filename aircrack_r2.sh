#!/bin/bash

##
# aircrack-ng current version install script
# Script by: th3gr1m 
##

# Updating the system
echo "[+] Updating the system..."
apt-get update && apt-get -y upgrade && apt-get -y dist-upgrade

# Install dependencies
echo "[+] Installing dependencies..."
apt-get -y install libssl-dev pkg-config libsqlite3-dev libnl-dev libpcap-dev libpcre3-dev

# Install the newest version of Aircrack and tools
echo "[+] Installing aircrack-ng and tools..."
cd ~/Tools
wget http://download.aircrack-ng.org/aircrack-ng-1.2-rc4.tar.gz
tar -xzf aircrack-ng-1.2-rc4.tar.gz
rm aircrack-ng-1.2-rc4.tar.gz
mv aircrack-ng-1.2-rc4 aircrack
cd aircrack
make sqlite=true experimental=true pcre=true
make sqlite=true experimental=true pcre=true install
cd ..

# update OUI File
echo "[+] Updating OUI File..."
airodump-ng-oui-update

echo "[+] aircrack-ng installed was successful!!"

exit 0
