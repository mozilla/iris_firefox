#!/bin/bash
# Ubuntu linux bootstrap
sudo apt-get update
sudo apt-get -y install \
    python-dev \
    python-pip \
    scrot \
    xsel \
    p7zip-full \
    libopencv-dev \
    autoconf automake libtool \
    autoconf-archive \
    pkg-config \
    libpng12-dev \
    libjpeg8-dev \
    libtiff5-dev \
    zlib1g-dev \
    libicu-dev \
    libpango1.0-dev \
    libcairo2-dev \
    firefox \
    wmctrl \
    xdotool

# Not installing tesseract-ocr here, see Iris instructions on how to get this


# The virtualenv package is not consistently named across distros
sudo apt-get -y install virtualenv \
	|| sudo apt-get -y install python-virtualenv

# sudo python -m pip install --upgrade --force pip
