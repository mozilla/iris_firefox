#!/bin/bash
# Windows bootstrap

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "\n${RED}##### Starting Windows bootstrap #####${NC} \n"

echo -e "${GREEN}##### Installing Pipenv #####${NC} \n"
pip install pipenv==2018.6.25