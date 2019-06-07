#!/bin/bash
# Ubuntu linux bootstrap

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


echo -e "\n${RED}##### Starting Linux OS bootstrap #####${NC} \n"

if [[ $(whoami | grep "root") =~ root ]]; then
    SUDO_USER=""
else
    SUDO_USER="sudo"
fi

install_python37 () {
    ${SUDO_USER} add-apt-repository -y ppa:deadsnakes/ppa
    ${SUDO_USER} apt-get update
    ${SUDO_USER} apt-get -y install python3.7
    echo -e "\n${GREEN}  --->  Python version #####${NC}\n"
    python3.7 -V
    echo -e "\n${GREEN}  --->  Python List All Modules #####${NC}\n"
    python3.7 -c "print( help('modules'))"
    echo -e "\n${GREEN}  --->  Python PIP version #####${NC}\n"
    python3.7 -m pip --version
}

echo -e "${GREEN}  --->  apt-get update #####${NC} \n"
${SUDO_USER} apt-get update

# Installing python library dependencies
echo -e "\n${GREEN}  --->  installing/upgrading python3.7-dev #####${NC}\n"
${SUDO_USER} apt-get -y install python3.7-dev


echo -e "\n${GREEN}  --->  installing/updating Python 3.7 #####${NC}\n"
if command -v python3 &>/dev/null; then
    if [[ $(python3 --version | grep "Python 3.7") =~ 3.7 ]]; then
        echo -e "\n${GREEN} --->  Skipping Python 3.7 install. Already installed. ${NC}\n"--version | grep "Python 3.7"
    elif command -v python3.7 &>/dev/null; then
        echo -e "\n${GREEN} ---> Verified for specific python3.7. Skipped install. Already installed. ${NC}\n"
    else
        echo -e "\n${GREEN}  --->  Installing Python 3.7 #####${NC}\n"
        install_python37
    fi
else
    echo -e "\n${GREEN}  --->  Installing Python 3.7 #####${NC}\n"
    install_python37
fi

echo -e "\n${GREEN}  --->  installing/upgrading python3-pip #####${NC}\n"
${SUDO_USER} apt-get -y install python3-pip

echo -e "\n${GREEN}  --->  installing/upgrading pip #####${NC}\n"
if [[ $(python3.7 -m pip --version | grep "pip") =~ pip ]]; then
    echo -e "\n${GREEN} --->  Skipping Python 3.7 PIP install. Already installed. ${NC}\n"
    python3.7 -m pip install --upgrade pip
fi

# Installing library dependencies
echo -e "\n${GREEN}  --->  installing/upgrading git #####${NC}\n"
${SUDO_USER} apt-get -y install git

echo -e "\n${GREEN}  --->  installing/upgrading scrot #####${NC}\n"
${SUDO_USER} apt-get -y install scrot

echo -e "\n${GREEN}  --->  installing/upgrading xsel #####${NC}\n"
${SUDO_USER} apt-get -y install xsel

echo -e "\n${GREEN}  --->  installing/upgrading p7zip-full #####${NC}\n"
${SUDO_USER} apt-get -y install p7zip-full

echo -e "\n${GREEN}  --->  installing/upgrading libopencv-dev #####${NC}\n"
${SUDO_USER} apt-get -y install libopencv-dev

echo -e "\n${GREEN}  --->  installing/upgrading autoconf automake libtool #####${NC}\n"
${SUDO_USER} apt-get -y install autoconf automake libtool

echo -e "\n${GREEN}  --->  installing/upgrading autoconf-archive #####${NC}\n"
${SUDO_USER} apt-get -y install autoconf-archive

echo -e "\n${GREEN}  --->  installing/upgrading pkg-config #####${NC}\n"
${SUDO_USER} apt-get -y install pkg-config

echo -e "\n${GREEN}  --->  installing/upgrading libpng-dev #####${NC}\n"
${SUDO_USER} apt-get -y install libpng-dev

echo -e "\n${GREEN}  --->  installing/upgrading libjpeg8-dev #####${NC}\n"
${SUDO_USER} apt-get -y install libjpeg8-dev

echo -e "\n${GREEN}  --->  installing/upgrading libtiff5-dev #####${NC}\n"
${SUDO_USER} apt-get -y install libtiff5-dev

echo -e "\n${GREEN}  --->  installing/upgrading zlib1g-dev #####${NC}\n"
${SUDO_USER} apt-get -y install zlib1g-dev

echo -e "\n${GREEN}  --->  installing/upgrading libicu-dev #####${NC}\n"
${SUDO_USER} apt-get -y install libicu-dev

echo -e "\n${GREEN}  --->  installing/upgrading libpango1.0-dev #####${NC}\n"
${SUDO_USER} apt-get -y install libpango1.0-dev

echo -e "\n${GREEN}  --->  installing/upgrading  libcairo2-dev #####${NC}\n"
${SUDO_USER} apt-get -y install libcairo2-dev

echo -e "\n${GREEN}  --->  installing/upgrading firefox #####${NC}\n"
${SUDO_USER} apt-get -y install firefox

echo -e "\n${GREEN}  --->  installing/upgrading wmctrl #####${NC}\n"
${SUDO_USER} apt-get -y install wmctrl

echo -e "\n${GREEN}  --->  installing/upgrading xdotool #####${NC}\n"
${SUDO_USER} apt-get -y install xdotool

echo -e "\n${GREEN}  --->  installing/upgrading python3.7-tk #####${NC}\n"
${SUDO_USER} apt-get -y install python3.7-tk


echo -e "\n${GREEN}  --->  installing/upgrading pipenv #####${NC}\n"
if [[ $(python3.7 -m pipenv --version | grep "pipenv") =~ pipenv ]];then
    pip3.7 install --upgrade pipenv
else
    pip3.7 install pipenv
fi

echo -e "\n${GREEN}  --->  installing/upgrading psutil #####${NC}\n"
if [[ $(python3.7 -m pip --list | grep "psutil") =~ psutil ]];then
    python3.7 -m pip install --upgrade psutil
else
    python3.7 -m pip install psutil
fi


echo -e "\n${GREEN}  --->  installing/upgrading Leptonica #####${NC}\n"
if [[ $(tesseract -v | grep "leptonica-1.76") ]]; then
    echo -e "\n${GREEN} --->  Skipping Leptonica install. Already installed. ${NC}\n"
else
    cd ~
    if [ ! -f leptonica-1.76.0.tar.gz ]; then
        echo "\n${GREEN}  --->  Downloading leptonica-1.76.0.tar.gz ${NC}\n"
        wget http://www.leptonica.com/source/leptonica-1.76.0.tar.gz
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
        ${SUDO_USER} ./configure &&\
        ${SUDO_USER} make &&\
        ${SUDO_USER} make install
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
        ${SUDO_USER} ./autogen.sh &&\
        ./configure --enable-debug &&\
        LDFLAGS="-L/usr/local/lib" CFLAGS="-I/usr/local/include" make &&\
        ${SUDO_USER} make install &&\
        ${SUDO_USER} make install -langs &&\
        ${SUDO_USER} ldconfig
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
        if [[ ! -d /usr/local/share/tessdata/ ]]; then
            ${SUDO_USER} mkdir /usr/local/share/tessdata/
        fi
        ${SUDO_USER} mv * /usr/local/share/tessdata/
    fi

else
    echo -e "\n${GREEN}  --->  Skipping Tesseract tessdata install. Already found in directory --> /usr/local/share/tessdata/${NC}\n"
fi

# Create download files
mkdir -p targets/firefox/local_web/thinkbroadband/thinkbroadband_files/downloaded_archives
cd targets/firefox/local_web/thinkbroadband/thinkbroadband_files/downloaded_archives

dd if=/dev/zero of=1GB.zip bs=1024 count=1024000
dd if=/dev/zero of=512MB.zip bs=1024 count=524000
dd if=/dev/zero of=200MB.zip bs=1024 count=205000
dd if=/dev/zero of=100MB.zip bs=1024 count=102400
dd if=/dev/zero of=50MB.zip bs=1024 count=51200
dd if=/dev/zero of=20MB.zip bs=1024 count=20500
dd if=/dev/zero of=10MB.zip bs=1024 count=10200
dd if=/dev/zero of=5MB.zip bs=1024 count=5100

cd ../../../../../