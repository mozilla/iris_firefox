#!/bin/bash

# Install requirements based on platform

if [[ "$OSTYPE" == "linux-gnu" ]]; then
	echo "Bootstrapping for Linux / apt-get"
	echo "sudo required"
	sudo $(dirname "$0")/linux_bootstrap.sh
elif [[ "$OSTYPE" == "darwin"* ]]; then
	echo "Bootstrapping for Mac OS X / Homebrew"
	$(dirname "$0")/osx_bootstrap.sh
else
	echo "Bootstrapping for Windows"
	$(dirname "$0")/win_bootstrap.sh
fi
