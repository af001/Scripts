#!/bin/bash

##
# Wardriving script - Installs basic tools for BackBox Linux 4.0+
# Created by: th3gr1m
##

# Update the system
echo "Updating system..."
apt-get update && apt-get -y upgrade 

echo "Installing packages..."

# Install packages
apt-get -y install gpsd gpsd-clients python-imaging libosmgpsmap2 python-osmgpsmap python-pip parcellite cherrytree

# Install python packages
pip install wigle

# Install tools
cd
mkdir Tools
cd Tools/

# Install kisheat
git clone https://github.com/int03h/kisheat.git
cd kisheat/heatmap-1.0-kisheatpatch
python setup.py install
cd ..
cp kisheat.py /usr/bin
cd ..

# Install kismon
wget http://files.salecker.org/kismon/kismon-0.6.tar.gz
tar -xzf kismon-0.6.tar.gz
cd kismon-0.6
make install
cd ..
rm kismon-0.6.tar.gz

# Install wardriving tools
git clone https://github.com/peondusud/wardriving.git

# Done
echo "Installation complete!!"

exit 0 
