#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

for i in "$@"
do
case $i in
    -l=*|--locales=*)
    LOCALES="${i#*=}"
    shift # past argument=value
    ;;
    -v=*|--version=*)
    VERSIONS="${i#*=}"
    shift # past argument=value
    ;;
    -c=*|--channel=*)
    CHANNEL="${i#*=}"
    shift # past argument=value
    ;;
    *)
          # unknown option
    ;;
esac
done

if [[ -n "$LOCALES" ]] && [[ -n "$VERSIONS" ]]; then
    for (( i = 1; i <= 20; i++ ));
    do
        locale=$(echo -e ${LOCALES} | sed "s/,/ /g" | awk "{print $"${i}"}")
        version=$(echo -e ${VERSIONS} | sed "s/,/ /g" | awk "{print $"${i}"}")

        if [[ -n "$locale" ]] && [[ -n "$version" ]]; then
            echo -e "\n\n${GREEN}Starting MANUAL update test: ${NC}\n"

            echo -e "LOCALE = $locale"
            echo -e "FIREFOX VERSION = $version"
            echo -e "CHANNELS = $CHANNEL\n\n"
            pipenv run iris -l ${locale} -f ${version} -e ${CHANNEL} -t manual_update -o

            echo -e "\n\n${GREEN}Starting BACKGROUND update test: ${NC}\n"

            echo -e "LOCALE = $locale"
            echo -e "FIREFOX VERSION = $version"
            echo -e "CHANNELS = $CHANNEL\n\n"

            pipenv run iris -l ${locale} -f ${version} -e ${CHANNEL} -t background_update -o
        fi
    done
else
    echo -e "\n\n${RED}The Firefox version and locale has not been specified. ${NC}\n"
fi
