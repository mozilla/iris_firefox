#!/bin/bash
# Windows bootstrap

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "\n${RED}##### Starting Windows bootstrap #####${NC}\n"

echo -e "${GREEN}##### Installing Scoop package management #####${NC}\n"
powershell -Command "Set-ExecutionPolicy RemoteSigned -scope CurrentUser"
powershell -Command "iex (new-object net.webclient).downloadstring('https://get.scoop.sh')" | grep 'Scoop is already installed.' &> /dev/null
if [ $? != 0 ]; then
   echo -e "\n${RED} --->  Scoop package management installed. You need to restart the terminal and run the bootstrap.sh again.${NC}\n"
   sleep 10
   exit
fi

echo -e "\n${GREEN}##### Installing 'which' & 'sudo' admin package #####${NC}\n"
powershell -Command "scoop install sudo"
powershell -Command "scoop install which"

echo -e "\n${GREEN}##### Installing Tesseract #####${NC}\n"
powershell -Command "scoop install tesseract"

echo -e "\n${GREEN}##### Installing 7zip #####${NC}\n"
powershell -Command "scoop install 7zip"

echo -e "\n${GREEN}##### Installing Python 2.7 #####${NC}\n"
powershell -Command "scoop bucket add versions; scoop install python27" | grep 'bucket already exists.' &> /dev/null
if [ $? != 0 ]; then
   echo -e "\n${RED} --->  Python 2.7 now installed. You need to restart the terminal and run the bootstrap.sh again to complete the install.${NC}\n"
   sleep 10
   exit
fi

echo -e "\n${GREEN}##### Installing Pipenv #####${NC}\n"
powershell -Command "pip install pipenv"
