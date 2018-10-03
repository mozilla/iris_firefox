#!/bin/bash
# Mac bootstrap

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "\n${RED}##### Starting OS X bootstrap #####${NC} \n"

echo -e "${GREEN}##### Check to see if Homebrew is installed, and install it if it is not #####${NC} \n"
command -v brew >/dev/null 2>&1 || { echo >&2 "Installing Homebrew Now"; \
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"; }

echo -e "\n${GREEN}##### Installing Python 2.7 #####${NC} \n"
brew install python@2
brew link python@2
export PATH=/usr/local/share/python:$PATH
echo -e "\n${GREEN}##### Installing Tesseract #####${NC} \n"
brew install tesseract
echo -e "\n${GREEN}##### Installing p7zip #####${NC} \n"
brew install p7zip
echo -e "\n${GREEN}##### Installing xquartz #####${NC} \n"
brew cask install xquartz
echo -e "\n${GREEN}##### Installing pipenv #####${NC} \n"
brew install pipenv

# Exporting settings to .bash_profile or .zshrc
grep -q -F 'export LC_ALL=en_US.UTF-8' ~/.bash_profile || echo 'export LC_ALL=en_US.UTF-8' >> ~/.bash_profile
grep -q -F 'export LANG=en_US.UTF-8' ~/.bash_profile || echo 'export LANG=en_US.UTF-8' >> ~/.bash_profile
grep -q -F 'export LC_ALL=en_US.UTF-8' ~/.zshrc || echo 'export LC_ALL=en_US.UTF-8' >> ~/.zshrc
grep -q -F 'export LANG=en_US.UTF-8' ~/.zshrc || echo 'export LANG=en_US.UTF-8' >> ~/.zshrc
