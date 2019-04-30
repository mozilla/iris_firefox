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
else
    powershell -Command "scoop install 7zip"
fi


echo -e "\n${GREEN} --->  Installing Tesseract  v4.1.0.20190314 ${NC} \n"
if command -v tesseract &>/dev/null; then
    echo -e "${GREEN}  --->  Tesseract already installed. ${NC}\n"
    echo -e "${GREEN}    --->  Checking Tesseract version. ${NC}\n"
    if [[ $(tesseract -v | grep "tesseract v4.0.0.20190314") =~ v4.0.0.20190314 ]]; then
        tesseract -v | grep "tesseract v4.0.0.20190314"
        echo -e "${GREEN}    --->  Tesseract is the correct version. ${NC}\n"
    else
        echo -e "${RED}  --->  You don't have Tesseract 20190314 version, removing and installing Tesseract 4.1.0.20190314.${NC}\n"
        powershell -Command "scoop uninstall tesseract" # If Scoop does not recognize tesseract3 command
        powershell -Command "scoop uninstall tesseract3"
        powershell -Command "scoop install "${CWD}"\bootstrap\tesseract20190314.json"
    fi
else
    powershell -Command "scoop install "${CWD}"\bootstrap\tesseract20190314.json"
fi



echo -e "\n${GREEN}  --->  Installing Python 3.7 #####${NC}\n"
if command -v python3 &>/dev/null; then
    echo -e "${GREEN}  --->  Skipping Python 3.7 install. Already installed. ${NC}\n"
else
    powershell -Command "scoop install python" | grep 'bucket already exists.' &> /dev/null
    if [ $? != 0 ]; then
       echo -e "\n${RED} --->  Python 3.7 now installed. You need to restart the terminal 2nd time and run the bootstrap.sh again to complete the install.${NC}\n"
       sleep 20
       exit
    fi
fi


echo -e "\n${GREEN}  --->  installing/upgrading pipenv ${NC}\n"
if command -v pipenv &>/dev/null; then
    powershell -Command "pip3 install --upgrade pip"
    powershell -Command "pip3 install --upgrade pipenv"
else
    powershell -Command "pip3 install pipenv"
fi
