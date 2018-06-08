#!/bin/bash
# Mac bootstrap

brew install tesseract
brew install p7zip
brew cask install xquartz

# Installing these here to avoid conflicts with other things
# we install in setup.py

pip install pyobjc
pip install pyobjc-core
