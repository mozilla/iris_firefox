#!/bin/bash
# Windows bootstrap

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
CWD=$(powershell -Command "(Get-Location).Path")

echo -e "\n${RED}##### Starting Windows bootstrap #####${NC}\n"

echo -e "${GREEN}  --->  Installing Scoop package management #####${NC}\n"
if command -v scoop &>/dev/null; then
    echo -e "${GREEN}  --->  Skipping Scoop library management install. Already found in directory --> C:\Users\$(user_name)\scoop\shims\scoop${NC}\n"
else
    powershell -Command "Set-ExecutionPolicy RemoteSigned -scope CurrentUser"
    powershell -Command "iex (new-object net.webclient).downloadstring('https://get.scoop.sh')" | grep 'Scoop is already installed.' &> /dev/null
    if [ $? != 0 ]; then
        echo -e "\n${RED} --->  Scoop package management installed. You need to restart the terminal and run the bootstrap.sh again.${NC}\n"
        sleep 20
        exit
    fi
fi

powershell -Command "scoop bucket add versions"

echo -e "\n${GREEN}  --->  Updating Scoop package management #####${NC}\n"
if [[ $(scoop status) =~ "WARN  Scoop is out of date." ]]; then
    powershell -Command "scoop update"
else
    echo -e "${GREEN}  --->  Skipping Scoop update. Already latest version. ${NC}\n"
fi


echo -e "\n${GREEN}  --->  Installing Git #####${NC}\n"
if [[ $(scoop list | grep git) =~ git ]]; then
    echo -e "${GREEN}  --->  Skipping Git install. Already installed. ${NC}\n"
    powershell -Command "scoop update git"
    powershell -Command "scoop update openssh"
else
    powershell -Command "scoop install git"
    powershell -Command "scoop install openssh"
fi

echo -e "\n${GREEN}  --->  Installing Wget #####${NC}\n"
if [[ $(scoop list | grep wget) =~ wget ]]; then
    echo -e "${GREEN}  --->  Skipping Wget install. Already installed. ${NC}\n"
     powershell -Command "scoop update wget"
else
    powershell -Command "scoop install wget"
fi

echo -e "\n${GREEN}  --->  Installing 'which' & 'sudo' #####${NC}\n"
echo -e "\n${GREEN}  --->  Installing which #####${NC}\n"
if [[ $(scoop list | grep which) =~ which ]]; then
    echo -e "${GREEN}  --->  Skipping which install. Already installed. ${NC}\n"
    powershell -Command "scoop update which"
else
    powershell -Command "scoop install which"
fi
echo -e "\n${GREEN}  --->  Installing sudo #####${NC}\n"
if [[ $(scoop list | grep sudo) =~ sudo ]]; then
    echo -e "${GREEN}  --->  Skipping sudo install. Already installed. ${NC}\n"
    powershell -Command "scoop update sudo"
else
    powershell -Command "scoop install sudo"
fi


echo -e "\n${GREEN}--->  Installing/updating 7zip #####${NC}\n"
if [[ $(scoop list | grep 7zip) =~ 7zip ]]; then
    echo -e "${GREEN}  --->  Skipping 7zip install. Already installed. ${NC}\n"
    powershell -Command "scoop update 7zip"
else
    powershell -Command "scoop install 7zip"
fi


echo -e "\n${GREEN} --->  Installing Tesseract 3 ${NC} \n"
if command -v tesseract &>/dev/null; then
    echo -e "${GREEN}  --->  Tesseract already installed. ${NC}\n"
    # No need to update to latest Tesseract, due to https://github.com/mozilla/iris/issues/2864
else
    powershell -Command "scoop install tesseract3"
fi

echo -e "\n${GREEN}  --->  Installing Python 2.7.15 #####${NC}\n"
if [[ $(scoop list |grep 'python2715') =~ 2715 ]]; then
    echo -e "${GREEN}  --->  Skipping Python 2.7.15 install. Already installed. ${NC}\n"
else
    echo -e "\n${GREEN}  --->  Install Python 2.7.15 #####${NC}\n"
    powershell -Command "scoop install "${CWD}"\bootstrap\python2715.json"
    if [ $? != 0 ]; then
       echo -e "\n${RED} --->  Python 2.7.15 now installed. You need to restart the terminal 2nd time and run the bootstrap.sh again to complete the install.${NC}\n"
       sleep 20
       exit
    fi
fi

echo -e "\n${GREEN}  --->  installing/upgrading pip ${NC}\n"
if command -v pip &>/dev/null; then
    powershell -Command "python -m pip install --upgrade pip"
else
    powershell -Command "curl https://bootstrap.pypa.io/get-pip.py -o bootstrap\get-pip.py"
    if [ $? != 0 ]; then
        echo -e "\n${RED} --->  Pip package management installed. You need to restart the terminal and run the bootstrap.sh again.${NC}\n"
        sleep 20
        exit
    fi
    echo -e "\n${GREEN}  --->  installing pip ${NC}\n"
    powershell -Command "python "${CWD}"\bootstrap\get-pip.py"
    powershell -Command "python -m pip install --upgrade pip"
fi

echo -e "\n${GREEN}  --->  installing/upgrading pipenv ${NC}\n"
if command -v pipenv &>/dev/null; then
    powershell -Command "python -m pip install --upgrade pip"
    powershell -Command "python -m pip install --upgrade pipenv"
else
    powershell -Command "python -m pip install pipenv"
fi

# Create download files
echo -e "\n${GREEN}  --->  Create download files ${NC}\n"
mkdir iris/local_web/thinkbroadband/thinkbroadband_files/downloaded_archives
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