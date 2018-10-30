#!/bin/bash
# Mac bootstrap

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "\n${RED}##### Starting OS X bootstrap #####${NC} \n"

echo -e "${GREEN}   --->   Check and install Homebrew${NC} \n"
command -v brew >/dev/null 2>&1 || { echo >&2 "Installing Homebrew Now"; \
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"; }

echo -e "\n${GREEN}  --->  installing/updating Python 2.7 ${NC} \n"

if command -v python2 &>/dev/null; then
    echo -e "\n${GREEN}  --->  Skipping Python 2.7 install. Already installed. ${NC}\n"
else
    brew install python@2
    brew link python@2
    export PATH=/usr/local/share/python:$PATH
fi

echo -e "\n${GREEN} --->  Installing Tesseract ${NC} \n"
if command -v tesseract -v >/dev/null 2>&1; then
    echo -e "\n${GREEN}  --->  Skipping Tesseract install. Already installed. ${NC}\n"
else
    brew install tesseract
fi

echo -e "\n${GREEN}  --->  installing/updating p7zip ${NC} \n"
brew install p7zip

echo -e "\n${GREEN}  --->  installing/updating xquartz ${NC} \n"
brew cask install xquartz

echo -e "\n${GREEN}  --->  installing/upgrading pipenv ${NC}\n"
if command -v pipenv &>/dev/null; then
    brew upgrade pipenv
else
    brew install pipenv
fi

# Exporting settings to .bash_profile or .zshrc
grep -q -F 'export LC_ALL=en_US.UTF-8' ~/.bash_profile || echo 'export LC_ALL=en_US.UTF-8' >> ~/.bash_profile
grep -q -F 'export LANG=en_US.UTF-8' ~/.bash_profile || echo 'export LANG=en_US.UTF-8' >> ~/.bash_profile
grep -q -F 'export LC_ALL=en_US.UTF-8' ~/.zshrc || echo 'export LC_ALL=en_US.UTF-8' >> ~/.zshrc
grep -q -F 'export LANG=en_US.UTF-8' ~/.zshrc || echo 'export LANG=en_US.UTF-8' >> ~/.zshrc
