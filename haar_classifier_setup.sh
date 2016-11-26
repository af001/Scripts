#!/bin/bash

# Custom image classifier for OpenCV. 
# By Anton
# References: http://coding-robin.de/2013/07/22/train-your-own-opencv-haar-classifier.html
#             http://docs.opencv.org/2.4/opencv_tutorials.pdf

# Download tools
git clone https://github.com/mrnugget/opencv-haar-classifier-training

# Download dependencies 
apt-get update && apt-get install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng12-dev libtiff5-dev libjasper-dev libdc1394-22-dev

# Download and compile opencv
wget https://github.com/Itseez/opencv/archive/2.4.13.zip
unzip 2.4.13.zip
rm 2.4.13.zip

cd opencv-2.4.13
mkdir release
cd release
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
make
make install

# Download and unzip positive and negative images
cd /root/opencv-haar-classifier-training/positive_images
wget http://xxx.xxx.xxx.xxx/positives.zip
unzip positives.zip
cp positives/* .
rm -rf positives
rm positives.zip
cd ../negative_images
wget http://xxx.xxx.xxx.xxx/negatives.zip
unzip negatives.zip
cp negatives/* .
rm -rf negatives
rm negatives.zip

# Compile positive and negative images into text files 
cd /root/opencv-haar-classifier-training
find ./positive_images -iname "*.png" > positives.txt
find ./negative_images -iname "*.png" > negatives.txt

# Generate samples
perl bin/createsamples.pl positives.txt negatives.txt samples 1500 "opencv_createsamples -bgcolor 0 -bgthresh 0 -maxxangle 1.1 -maxyangle 1.1 maxzangle 0.5 -maxidev 40 -w 80 -h 40"

# Merge .vec files 
python ./tools/mergevec.py -v ./samples -o samples.vec

# Train the classifier: Adjust number of positive below sample size, change neg to number of negative images, and adjust RAM to use
opencv_traincascade -data classifier -vec samples.vec -bg negatives.txt -numStages 20 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numPos 1000 -numNeg 600 -w 80 -h 40 -mode ALL -precalcValBufSize 1024 -precalcIdxBufSize 1024

# Output should be classifier.xml file to be used
