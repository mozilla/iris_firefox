#!/bin/bash

RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Install requirements based on platform

echo -e "\n${CYAN}Installing project dependencies based on OS type ${NC} \n"

if [[ "$OSTYPE" == "linux-gnu" ]]; then
	echo -e "${CYAN}Bootstrapping for Linux OS ${NC} \n"
	echo -e "${RED}Administrator password required!${NC} \n"
	sudo $(dirname "$0")/linux_bootstrap.sh
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${CYAN}Bootstrapping for Mac OS X ${NC} \n"
	$(dirname "$0")/osx_bootstrap.sh
else
    echo -e "${CYAN} Bootstrapping for Windows OS ${NC} \n"
	$(dirname "$0")/win_bootstrap.sh
fi
