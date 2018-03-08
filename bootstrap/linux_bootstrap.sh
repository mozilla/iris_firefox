#!/bin/bash
# Ubuntu linux bootstrap
sudo apt-get update
sudo apt-get -y install \
    default-jre \
    python-dev \
    python-pip \
    xvfb \
    p7zip-full \
    libopencv-dev \
    tesseract-ocr \
    firefox \
    wmctrl \
    xdotool

# The virtualenv package is not consistently named across distros
sudo apt-get -y install virtualenv \
	|| sudo apt-get -y install python-virtualenv

# sudo python -m pip install --upgrade --force pip

# This is needed but causes the shell to hang
Xvfb :99