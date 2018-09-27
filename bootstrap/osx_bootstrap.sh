#!/bin/bash
# Mac bootstrap

# Check to see if Homebrew is installed, and install it if it is not
command -v brew >/dev/null 2>&1 || { echo >&2 "Installing Homebrew Now"; \
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"; }

brew install tesseract
brew install p7zip
brew cask install xquartz
brew install pipenv

grep -q -F 'export LC_ALL=en_US.UTF-8' ~/.bash_profile || echo 'export LC_ALL=en_US.UTF-8' >> ~/.bash_profile
grep -q -F 'export LANG=en_US.UTF-8' ~/.bash_profile || echo 'export LANG=en_US.UTF-8' >> ~/.bash_profile
grep -q -F 'export LC_ALL=en_US.UTF-8' ~/.zshrc || echo 'export LC_ALL=en_US.UTF-8' >> ~/.zshrc
grep -q -F 'export LANG=en_US.UTF-8' ~/.zshrc || echo 'export LANG=en_US.UTF-8' >> ~/.zshrc
