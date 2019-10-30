#!/bin/bash
# Windows bootstrap

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
CWD=$(powershell -Command "(Get-Location).Path")

install_tesseract () {
    powershell -Command "scoop install "${CWD}"\bootstrap\tesseract.json"
}

echo -e "\n${RED}##### Starting Windows bootstrap #####${NC}\n"

echo -e "${GREEN}  --->  Installing Scoop package management #####${NC}\n"
if command -v scoop &>/dev/null; then
    echo -e "${GREEN}  --->  Skipping Scoop library management install. Already found in directory --> C:\Users\$(user_name)\scoop\shims\scoop${NC}\n"
else
    powershell -Command "Set-ExecutionPolicy RemoteSigned -scope CurrentUser"
    powershell -Command "iex (new-object net.webclient).downloadstring('https://get.scoop.sh')" | grep 'Scoop is already installed.' &> /dev/null
    if [ $? != 0 ]; then
        echo -e "\n${RED} --->  Scoop package management installed. You need to restart the terminal and run the bootstrap.sh again.${NC}\n"
        echo -e "\n${RED} --->  First out of 2 restarts. Needed in order to use 'scoop' ${NC}\n"
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

echo -e "\n${GREEN}--->  Installing/updating 7zip #####${NC}\n"
if [[ $(scoop list | grep "7zip") =~ 7zip ]]; then
    echo -e "${GREEN}  --->  Skipping 7zip install. Already installed. ${NC}\n"
else
    powershell -Command "scoop install 7zip"
fi

powershell -Command "scoop bucket add extras"

echo -e "\n${GREEN}  --->  Installing Firefox #####${NC}\n"
if [[ $(scoop list | grep "firefox") =~ firefox ]]; then
    echo -e "${GREEN}  --->  Skipping firefox install. Already installed. Update Firefox ${NC}\n"
    powershell -Command "scoop update firefox"
else
    powershell -Command "scoop install firefox"
fi

echo -e "\n${GREEN}  --->  Installing Git #####${NC}\n"
if [[ $(scoop list | grep "git") =~ git ]]; then
    echo -e "${GREEN}  --->  Skipping Git install. Already installed. Update git and openssh ${NC}\n"
    powershell -Command "scoop update git"
    powershell -Command "scoop update openssh"
else
    powershell -Command "scoop install git"
    powershell -Command "scoop install openssh"
fi


echo -e "\n${GREEN}  --->  Installing which #####${NC}\n"
if [[ $(scoop list | grep "which") =~ which ]]; then
    echo -e "${GREEN}  --->  Skipping which install. Already installed. Update which ${NC}\n"
    powershell -Command "scoop update which"
else
    powershell -Command "scoop install which"
fi

echo -e "\n${GREEN}  --->  Installing sudo #####${NC}\n"
if [[ $(scoop list | grep "sudo") =~ sudo ]]; then
    echo -e "${GREEN}  --->  Skipping sudo install. Already installed. Update sudo${NC}\n"
    powershell -Command "scoop update sudo"
else
    powershell -Command "scoop install sudo"
fi

echo -e "\n${GREEN} --->  Installing Tesseract 4 ${NC} \n"
if command -v tesseract &>/dev/null; then
    echo -e "${GREEN}  --->  Tesseract already installed. ${NC}\n"
    echo -e "${GREEN}    --->  Checking Tesseract version. ${NC}\n"
    if [[ $(tesseract -v | grep "tesseract 3.05") =~ 3 ]]; then
        echo -e "${RED}  --->  You have Tesseract 3, removing and installing Tesseract 4.${NC}\n"
        powershell -Command "scoop uninstall tesseract" # If Scoop does not recognize tesseract3 command
        powershell -Command "scoop uninstall tesseract3"
        install_tesseract
    else
        echo -e "${GREEN}    --->  Tesseract is the correct version. ${NC}\n"
    fi
else
    install_tesseract
fi

echo -e "\n${GREEN}  --->  installing/updating Python 3.7 #####${NC}\n"
if command -v python3 &>/dev/null; then
    if [[ $(python3 --version | grep "Python 3.7") =~ 3.7 ]]; then
         echo -e "\n${GREEN} --->  Skipping Python 3.7 install. Already installed. ${NC}\n"
    elif command -v python3.7 &>/dev/null; then
        echo -e "\n${GREEN} ---> Verified for specific python3.7. Skipped install. Already installed. ${NC}\n"
    else
        echo -e "${GREEN}  --->  Update to Python 3.7 . ${NC}\n"
        powershell -Command "scoop update python37" | grep 'bucket already exists.' &> /dev/null
    fi
else
    echo -e "\n${GREEN}  --->  Installing Python 3.7 #####${NC}\n"
    powershell -Command "scoop install python37" | grep 'bucket already exists.' &> /dev/null
    if [ $? != 0 ]; then
       echo -e "\n${RED} --->  Python 3.7 now installed. You need to restart the terminal one more time and run the bootstrap.sh again to complete the install.${NC}\n"
       echo -e "\n${RED} --->  Last restart needed in order to use 'python3' and install python3 dependent packages ${NC}\n"
       sleep 20
       exit
    fi
fi

echo -e "\n${GREEN}  --->  installing/upgrading pipenv ${NC}\n"
if command -v pipenv &>/dev/null; then
    powershell -Command "pip install --upgrade pip"
    powershell -Command "pip install --upgrade pipenv"
else
    powershell -Command "pip install pipenv"
fi

# Create download files
echo -e "\n${GREEN}  --->  Create download files ${NC}\n"
mkdir -p targets/firefox/local_web/thinkbroadband/thinkbroadband_files/downloaded_archives
mkdir -p targets/nightly/local_web/thinkbroadband/thinkbroadband_files/downloaded_archives
cd targets/firefox/local_web/thinkbroadband/thinkbroadband_files/downloaded_archives

dd if=/dev/zero of=1GB.zip bs=1024 count=1024000
dd if=/dev/zero of=512MB.zip bs=1024 count=524000
dd if=/dev/zero of=200MB.zip bs=1024 count=205000
dd if=/dev/zero of=100MB.zip bs=1024 count=102400
dd if=/dev/zero of=50MB.zip bs=1024 count=51200
dd if=/dev/zero of=20MB.zip bs=1024 count=20500
dd if=/dev/zero of=10MB.zip bs=1024 count=10200
dd if=/dev/zero of=5MB.zip bs=1024 count=5100
cp -R * ../../../../../nightly/local_web/thinkbroadband/thinkbroadband_files/downloaded_archives

cd ../../../../../../