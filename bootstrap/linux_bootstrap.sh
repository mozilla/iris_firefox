#!/bin/bash
# Ubuntu linux bootstrap

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "\n${RED}##### Starting Linux OS bootstrap #####${NC} \n"

echo -e "${GREEN}  --->  sudo apt-get update #####${NC} \n"
sudo apt-get update


echo -e "\n${GREEN}  --->  installing/updating Python 2.7 #####${NC}\n"
if command -v python2 &>/dev/null; then
    echo -e "\n${GREEN} --->  Skipping Python 2.7 install. Already installed. ${NC}\n"
else
    sudo apt-get -y install python2.7
fi

echo -e "\n${GREEN}  --->  installing/upgrading pip #####${NC}\n"
if command -v pip &>/dev/null; then
    pip install --upgrade pip
else
    sudo apt-get -y install python-pip
fi

# Installing library dependencies
echo -e "\n${GREEN}  --->  installing/upgrading scrot #####${NC}\n"
sudo apt-get -y install scrot

echo -e "\n${GREEN}  --->  installing/upgrading xsel #####${NC}\n"
sudo apt-get -y install xsel

echo -e "\n${GREEN}  --->  installing/upgrading p7zip-full #####${NC}\n"
sudo apt-get -y install p7zip-full

echo -e "\n${GREEN}  --->  installing/upgrading libopencv-dev #####${NC}\n"
sudo apt-get -y install libopencv-dev

echo -e "\n${GREEN}  --->  installing/upgrading autoconf automake libtool #####${NC}\n"
sudo apt-get -y install autoconf automake libtool

echo -e "\n${GREEN}  --->  installing/upgrading autoconf-archive #####${NC}\n"
sudo apt-get -y install autoconf-archive

echo -e "\n${GREEN}  --->  installing/upgrading pkg-config #####${NC}\n"
sudo apt-get -y install pkg-config

echo -e "\n${GREEN}  --->  installing/upgrading libpng-dev #####${NC}\n"
sudo apt-get -y install libpng-dev

echo -e "\n${GREEN}  --->  installing/upgrading libjpeg8-dev #####${NC}\n"
sudo apt-get -y install libjpeg8-dev

echo -e "\n${GREEN}  --->  installing/upgrading libtiff5-dev #####${NC}\n"
sudo apt-get -y install libtiff5-dev

echo -e "\n${GREEN}  --->  installing/upgrading zlib1g-dev #####${NC}\n"
sudo apt-get -y install zlib1g-dev

echo -e "\n${GREEN}  --->  installing/upgrading libicu-dev #####${NC}\n"
sudo apt-get -y install libicu-dev

echo -e "\n${GREEN}  --->  installing/upgrading libpango1.0-dev #####${NC}\n"
sudo apt-get -y install libpango1.0-dev

echo -e "\n${GREEN}  --->  installing/upgrading  libcairo2-dev #####${NC}\n"
sudo apt-get -y install libcairo2-dev

echo -e "\n${GREEN}  --->  installing/upgrading firefox #####${NC}\n"
sudo apt-get -y install firefox

echo -e "\n${GREEN}  --->  installing/upgrading wmctrl #####${NC}\n"
sudo apt-get -y install wmctrl

echo -e "\n${GREEN}  --->  installing/upgrading xdotool #####${NC}\n"
sudo apt-get -y install xdotool

echo -e "\n${GREEN}  --->  installing/upgrading python-tk #####${NC}\n"
sudo apt-get -y install python-tk


echo -e "\n${GREEN}  --->  installing/upgrading pipenv #####${NC}\n"
if command -v pipenv &>/dev/null; then
    pip install --upgrade pipenv
else
    pip install pipenv
fi


echo -e "\n${GREEN}  --->  installing/upgrading Leptonica #####${NC}\n"
if [[ $(tesseract -v | grep "leptonica-1.76") ]]; then
    echo -e "\n${GREEN} --->  Skipping Leptonica install. Already installed. ${NC}\n"
else
    cd ~
    if [ ! -f leptonica-1.76.0.tar.gz ]; then
        echo "\n${GREEN}  --->  Downloading leptonica-1.76.0.tar.gz ${NC}\n"
        wget http://www.leptonica.org/source/leptonica-1.76.0.tar.gz
    fi

    if [ ! -d leptonica-1.76.0 ]; then
        if [ -f leptonica-1.76.0.tar.gz ]; then
            tar xopf leptonica-1.76.0.tar.gz
        else
            echo -e "\n${RED}  --->  Archive leptonica-1.76.0.tar.gz not found! Maybe download failed. ${NC}\n" && exit 0
        fi
    fi

    if [ ! -d leptonica-1.76.0 ]; then
        echo "\n${RED}  --->  leptonica-1.76.0 directory not found! Maybe the extraction failed. ${NC}\n" && exit 0
    else
        cd leptonica-1.76.0
    fi

    if [[ $(pwd | grep "leptonica-1.76.0") ]]; then
        sudo ./configure &&\
        sudo make &&\
        sudo make install
    fi
fi


echo -e "\n${GREEN}  --->  installing/upgrading Tesseract #####${NC}\n"
if [[ $(tesseract -v | grep "tesseract 4.") ]]; then
    echo -e "\n${GREEN} --->  Skipping Tesseract v4 install. Already installed. ${NC}\n"
else
    cd ~
    if [ ! -f 4.0.0.tar.gz ]; then
        echo "\n${GREEN}  --->  Downloading Tesseract archive 4.0.0.tar.gz ${NC}\n"
        wget https://github.com/tesseract-ocr/tesseract/archive/4.0.0.tar.gz
    fi

    if [ ! -d tesseract-4.0.0 ]; then
        if [ -f 4.0.0.tar.gz ]; then
            tar xopf 4.0.0.tar.gz
        else
            echo -e "\n${RED}  --->  Tesseract archive 4.0.0.tar.gz not found! Maybe download failed. ${NC}\n" && exit 0
        fi
    fi

    if [ ! -d tesseract-4.0.0 ]; then
        echo "\n${RED}  --->  tesseract-4.0.0 directory not found! Maybe the extraction failed. ${NC}\n" && exit 0
    else
        cd tesseract-4.0.0
    fi

    if [[ $(pwd | grep "tesseract-4.0.0") ]]; then
        sudo ./autogen.sh &&\
        ./configure --enable-debug &&\
        LDFLAGS="-L/usr/local/lib" CFLAGS="-I/usr/local/include" make &&\
        sudo make install &&\
        sudo make install -langs &&\
        sudo ldconfig
    fi
fi


echo -e "\n${GREEN}  --->  Downloading and installing Tesseract data #####${NC}\n"
if  [ ! -f /usr/local/share/tessdata/afr.traineddata ]; then
    cd ~
    if [ ! -f 4.0.0.zip ]; then
        echo "\n${GREEN}   --->  Downloading Tessdata archive 4.0.0.zip ${NC}\n"
        wget https://github.com/tesseract-ocr/tessdata/archive/4.0.0.zip
    fi

    if [ -f 4.0.0.zip ]; then
        if [[ $(find 4.0.0.zip -type f -size +490000000c 2>/dev/null) ]]; then
            echo -e "\n${GREEN}  --->  Download finished. Unziping Tessdata archive 4.0.0.zip ${NC}\n"
            unzip 4.0.0.zip
        else
            echo -e "\n${RED}  --->  Tessdata archive 4.0.0.zip is not the correct size. Maybe download was stopped or did not completely finish. ${NC}\n"
            echo -e "${RED}        Please delete the file and restart the process. ${NC}\n" && exit 0
        fi
    else
        echo -e "\n${RED}  --->  Tessdata archive 4.0.0.zip not found! Maybe download failed. ${NC}\n" && exit 0
    fi

    if [ ! -d tessdata-4.0.0 ]; then
        echo "\n${RED}  --->  tessdata-4.0.0 directory not found! Maybe the extraction failed. ${NC}\n" && exit 0
    else
        cd tessdata-4.0.0
    fi

    if [[ $(pwd | grep "tessdata-4.0.0") ]]; then
        if [ ! -d /usr/local/share/tessdata/ ]; then
            sudo mkdir /usr/local/share/tessdata/
        fi
        sudo mv * /usr/local/share/tessdata/
    fi

else
    echo -e "\n${GREEN}  --->  Skipping Tesseract tessdata install. Already found in directory --> /usr/local/share/tessdata/${NC}\n"
fi


# Create download files
mkdir -p iris/local_web/thinkbroadband/thinkbroadband_files/downloaded_archives
cd iris/local_web/thinkbroadband/thinkbroadband_files/downloaded_archives

dd if=/dev/zero of=1GB.zip bs=1024 count=1024000
dd if=/dev/zero of=512MB.zip bs=1024 count=524000
dd if=/dev/zero of=200MB.zip bs=1024 count=205000
dd if=/dev/zero of=100MB.zip bs=1024 count=102400
dd if=/dev/zero of=50MB.zip bs=1024 count=51200
dd if=/dev/zero of=20MB.zip bs=1024 count=20500
dd if=/dev/zero of=10MB.zip bs=1024 count=10200
dd if=/dev/zero of=5MB.zip bs=1024 count=5100

cd ../../../../../
