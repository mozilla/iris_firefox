#!/bin/bash
# Windows bootstrap

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "\n${RED}##### Starting Windows bootstrap #####${NC}\n"

echo -e "${GREEN}  --->  Installing Scoop package management #####${NC}\n"


if command -v scoop &>/dev/null; then
    echo -e "\n${GREEN}  --->  Skipping Scoop library management install. Already found in directory --> C:\Users\$(user_name)\scoop\shims\scoop${NC}\n"
else
    powershell -Command "Set-ExecutionPolicy RemoteSigned -scope CurrentUser"
    powershell -Command "iex (new-object net.webclient).downloadstring('https://get.scoop.sh')" | grep 'Scoop is already installed.' &> /dev/null
    if [ $? != 0 ]; then
        echo -e "\n${RED} --->  Scoop package management installed. You need to restart the terminal and run the bootstrap.sh again.${NC}\n"
        sleep 20
        exit
    fi
fi


echo -e "\n${GREEN} --->  Installing/updating 'which' & 'sudo' admin package #####${NC}\n"
powershell -Command "scoop install which"
powershell -Command "scoop install sudo"


echo -e "\n${GREEN}--->  Installing/updating 7zip #####${NC}\n"
powershell -Command "scoop install 7zip"


echo -e "\n${GREEN} --->  Installing Tesseract ${NC} \n"
if command -v tesseract -v >/dev/null 2>&1; then
    echo -e "\n${GREEN}  --->  Skipping Tesseract install. Already installed. ${NC}\n"
else
    powershell -Command "scoop install tesseract"
fi


echo -e "\n${GREEN}  --->  Installing Python 2.7 #####${NC}\n"
if command -v python2 &>/dev/null; then
    echo -e "\n${GREEN}  --->  Skipping Python 2.7 install. Already installed. ${NC}\n"
else
    powershell -Command "scoop bucket add versions; scoop install python27" | grep 'bucket already exists.' &> /dev/null
    if [ $? != 0 ]; then
       echo -e "\n${RED} --->  Python 2.7 now installed. You need to restart the terminal 2nd time and run the bootstrap.sh again to complete the install.${NC}\n"
       sleep 20
       exit
    fi
fi


echo -e "\n${GREEN}  --->  installing/upgrading pipenv ${NC}\n"
if [[ ! $(pipenv --version) ]]; then
    powershell -Command "pip install pipenv"
else
    powershell -Command "python -m pip install --upgrade pipenv"
fi
