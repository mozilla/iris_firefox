#!/bin/bash
# Ubuntu linux bootstrap

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "\n${RED}##### Starting Linux OS bootstrap #####${NC} \n"

echo -e "${GREEN}##### sudo apt-get update #####${NC} \n"
sudo apt-get update
echo -e "\n${GREEN}##### Removing Tesseract, if installed #####${NC}\n"
sudo apt-get -y remove --auto-remove tesseract-ocr
echo -e "\n${GREEN}##### Removing Leptonica, if installed #####${NC}\n"
sudo apt-get -y remove --auto-remove libleptonica-dev

echo -e "\n${GREEN}##### apt-get autoclean #####${NC}\n"
sudo apt-get autoclean
echo -e "\n${GREEN}##### apt-get autoremove --purge #####${NC}\n"
sudo apt-get autoremove --purge

echo -e "\n${GREEN}##### installing Python 2.7 #####${NC}\n"
sudo apt-get -y install python2.7
echo -e "\n${GREEN}##### installing pip #####${NC}\n"
sudo apt-get -y install python-pip
echo -e "\n${GREEN}##### installing scrot #####${NC}\n"
sudo apt-get -y install scrot
echo -e "\n${GREEN}##### installing xsel #####${NC}\n"
sudo apt-get -y install xsel
echo -e "\n${GREEN}##### installing p7zip-full #####${NC}\n"
sudo apt-get -y install p7zip-full
echo -e "\n${GREEN}##### installing libopencv-dev #####${NC}\n"
sudo apt-get -y install libopencv-dev
echo -e "\n${GREEN}##### installing autoconf automake libtool #####${NC}\n"
sudo apt-get -y install autoconf automake libtool
echo -e "\n${GREEN}##### installing autoconf-archive #####${NC}\n"
sudo apt-get -y install autoconf-archive
echo -e "\n${GREEN}##### installing pkg-config #####${NC}\n"
sudo apt-get -y install pkg-config
echo -e "\n${GREEN}##### installing libpng-dev #####${NC}\n"
sudo apt-get -y install libpng-dev
echo -e "\n${GREEN}##### installing libjpeg8-dev #####${NC}\n"
sudo apt-get -y install libjpeg8-dev
echo -e "\n${GREEN}##### installing libtiff5-dev #####${NC}\n"
sudo apt-get -y install libtiff5-dev
echo -e "\n${GREEN}##### installing zlib1g-dev #####${NC}\n"
sudo apt-get -y install zlib1g-dev
echo -e "\n${GREEN}##### installing libicu-dev #####${NC}\n"
sudo apt-get -y install libicu-dev
echo -e "\n${GREEN}##### installing libpango1.0-dev #####${NC}\n"
sudo apt-get -y install libpango1.0-dev
echo -e "\n${GREEN}##### installing libcairo2-dev #####${NC}\n"
sudo apt-get -y install libcairo2-dev
echo -e "\n${GREEN}##### installing firefox #####${NC}\n"
sudo apt-get -y install firefox
echo -e "\n${GREEN}##### installing wmctrl #####${NC}\n"
sudo apt-get -y install wmctrl
echo -e "\n${GREEN}##### installing xdotool #####${NC}\n"
sudo apt-get -y install xdotool
echo -e "\n${GREEN}##### installing python-tk #####${NC}\n"
sudo apt-get -y install python-tk
#echo -e "\n${GREEN}##### installing tesseract-ocr #####${NC}\n"
#sudo apt-get -y install tesseract-ocr
#sudo apt-get -y install libtesseract-dev

# Install Pipenv
echo -e "\n${GREEN}##### installing pipenv #####${NC}\n"
pip install pipenv
pip install --upgrade pipenv

echo -e "\n${GREEN}##### installing Leptonica #####${NC}\n"
cd ~
wget http://www.leptonica.com/source/leptonica-1.76.0.tar.gz
tar xopf leptonica-1.76.0.tar.gz
cd leptonica-1.76.0
./configure
sudo make
sudo make install
cd ~
rm leptonica-1.76.0.tar.gz

echo -e "\n${GREEN}##### installing Tesseract #####${NC}\n"
wget https://github.com/tesseract-ocr/tesseract/archive/3.05.02.tar.gz
tar xopf 3.05.02.tar.gz
cd tesseract-3.05.02
./autogen.sh
./configure --enable-debug
LDFLAGS="-L/usr/local/lib" CFLAGS="-I/usr/local/include" make
sudo make install
sudo make install-langs
sudo ldconfig
cd ~
rm 3.05.02.tar.gz

echo -e "\n${GREEN}##### installing Tesseract data #####${NC}\n"
wget https://github.com/tesseract-ocr/tessdata/archive/3.04.00.zip
unzip 3.04.00.zip
cd tessdata-3.04.00
sudo mv * /usr/local/share/tessdata/
cd ~
rm 3.04.00.zip
