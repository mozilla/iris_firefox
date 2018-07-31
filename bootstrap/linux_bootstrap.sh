#!/bin/bash
# Ubuntu linux bootstrap
sudo apt-get update
sudo apt-get remove \
    tesseract-ocr* \
    libleptonica-dev

sudo apt-get autoclean
sudo apt-get autoremove --purge

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
    xdotool \
    python-tk

# install pipenv
pip install --user pipenv

# Install Leptonica
cd ~
wget http://www.leptonica.com/source/leptonica-1.75.3.tar.gz
tar xopf leptonica-1.75.3.tar.gz
cd leptonica-1.75.3
./configure
sudo make
sudo make install
cd ~

# Install Tesseract
wget https://github.com/tesseract-ocr/tesseract/archive/3.05.00.tar.gz
tar xopf 3.05.00.tar.gz
cd tesseract-3.05.00
./autogen.sh
./configure --enable-debug
LDFLAGS="-L/usr/local/lib" CFLAGS="-I/usr/local/include" make
sudo make install
sudo make install-langs
sudo ldconfig
cd ~

# Install Tesseract data
wget https://github.com/tesseract-ocr/tessdata/archive/3.04.00.zip
unzip 3.04.00.zip
cd tessdata-3.04.00
sudo mv * /usr/local/share/tessdata/
cd ~
