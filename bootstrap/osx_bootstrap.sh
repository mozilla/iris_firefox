#!/bin/bash
# Mac bootstrap

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "\n${RED}##### Starting OS X bootstrap #####${NC} \n"

echo -e "${GREEN}   --->   Check and install Homebrew${NC} \n"
command -v brew >/dev/null 2>&1 || { echo >&2 "Installing Homebrew Now"; \
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"; }

install_python37 () {
    brew install python3
    brew link --overwrite python3
    export PATH=/usr/local/share/python:$PATH
}

echo -e "\n${GREEN}  --->  installing/updating Python 3.7 ${NC} \n"

if command -v python3 &>/dev/null; then
    if [[ $(python3 --version | grep "Python 3.7") =~ 3.7 ]]; then
        echo -e "\n${GREEN} --->  Skipping Python 3.7 install. Already installed. ${NC}\n"--version | grep "Python 3.7"
    elif command -v python3.7 &>/dev/null; then
        echo -e "\n${GREEN} ---> Verified for specific python3.7. Skipped install. Already installed. ${NC}\n"--version | grep "Python 3.7"
    else
        echo -e "\n${GREEN}  --->  Installing Python 3.7 #####${NC}\n"
        install_python37
    fi
else
    echo -e "\n${GREEN}  --->  Installing Python 3.7 #####${NC}\n"
    install_python37
fi


echo -e "\n${GREEN} --->  Installing Tesseract ${NC} \n"
if command -v tesseract -v >/dev/null 2>&1; then
    echo -e "\n${GREEN}  --->  Skipping Tesseract install. Already installed. ${NC}\n"
    echo -e "${GREEN}    --->  Checking Tesseract version. ${NC}\n"
    if [[ $(tesseract -v | grep "tesseract 3.05") ]]; then
        echo -e "${RED}  --->  You have Tesseract 3, removing and installing Tesseract 4.${NC}\n"
        brew upgrade tesseract
    else
        echo -e "${GREEN}    --->  Tesseract is the correct version. ${NC}\n"
    fi
else
    brew install tesseract
fi

echo -e "\n${GREEN}  --->  installing/updating p7zip ${NC} \n"
brew install p7zip

echo -e "\n${GREEN}  --->  installing/updating xquartz ${NC} \n"
brew cask install xquartz

echo -e "\n${GREEN}  --->  installing/updating firefox ${NC} \n"
if [[ $(mdfind "kMDItemKind == 'Application'" | grep Firefox.app) =~ "Firefox.app" ]]; then
    echo -e "\n${GREEN} --->  Skipping Firefox install. Already installed. ${NC}\n"
else
    echo -e "\n${GREEN}  --->  installing Firefox ${NC}\n"
    brew cask install firefox
fi

echo -e "\n${GREEN}  --->  installing/upgrading pipenv ${NC}\n"
if command -v pipenv &>/dev/null; then
    brew upgrade pipenv
else
    echo -e "\n${GREEN}  --->  installing pipenv ${NC}\n"
    brew install pipenv
fi

echo -e "\n${GREEN}--->  Installing pyobjc library #####${NC}\n"
if [[ $(pip3.7 show pyobjc | grep Name:) =~ "pyobjc" ]]; then
    echo -e "${GREEN}  --->  Skipping pyobjc install. Already installed. ${NC}\n"
else
    pip3.7 install -U pyobjc
fi

echo -e "\n${GREEN}--->  Installing pyobjc-core library #####${NC}\n"
if [[ $(pip3.7 show pyobjc-core | grep Name:) =~ "pyobjc-core" ]]; then
    echo -e "${GREEN}  --->  Skipping pyobjc-core install. Already installed. ${NC}\n"
else
    pip3.7 install -U pyobjc-core
fi

# Exporting settings to .bash_profile or .zshrc
grep -q -F 'export LC_ALL=en_US.UTF-8' ~/.bash_profile || echo 'export LC_ALL=en_US.UTF-8' >> ~/.bash_profile
grep -q -F 'export LANG=en_US.UTF-8' ~/.bash_profile || echo 'export LANG=en_US.UTF-8' >> ~/.bash_profile
grep -q -F 'export LC_ALL=en_US.UTF-8' ~/.zshrc || echo 'export LC_ALL=en_US.UTF-8' >> ~/.zshrc
grep -q -F 'export LANG=en_US.UTF-8' ~/.zshrc || echo 'export LANG=en_US.UTF-8' >> ~/.zshrc

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