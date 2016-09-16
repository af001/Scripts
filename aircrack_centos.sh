#!/bin/bash

##
# aircrack-ng current version install script for centos
# Script by: th3gr1m 
##

# Updating the system
echo "[+] Updating the system..."
yum update 

# Install dependencies
echo "[+] Installing dependencies..."
yum install libnl3 libnl3-devel openssl-devel openssl openssl-libs sqlite-devel gcc-c++

# Install the newest version of Aircrack and tools
echo "[+] Installing aircrack-ng..."

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
