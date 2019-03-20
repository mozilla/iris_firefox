#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# TEST STRINGS
SEARCH_CODE_TESTS='default_search_code_baidu,default_search_code_google,default_search_code_yandex'
MANUAL_UPDATE_TESTS='manual_update,'$SEARCH_CODE_TESTS
BACKGROUND_UPDATE_TESTS='background_update,'$SEARCH_CODE_TESTS

for i in "$@"
do
case $i in
    -u=*|--channel=*)
    CHANNEL="${i#*=}"
    shift # past argument=value
    ;;
    -t=*|--tests=*)
    TESTS="${i#*=}"
    shift # past argument=value
    ;;
    -b=*|--builds=*)
    BUILDS="${i#*=}"
    shift # past argument=value
    ;;
    *)
          # unknown option
    ;;
esac
done

if [[ -n "$BUILDS" ]]; then
    COUNT=$(grep -o "," <<<"$BUILDS" | wc -l)

    for (( i = 1; i <= $((COUNT + 1)); i++ ));
    do
        build=$(echo -e ${BUILDS} | sed "s/,/ /g" | awk "{print $"${i}"}")
        version=$(echo -e ${build} | sed "s/_/ /g" | awk "{print $"1"}")
        locale=$(echo -e ${build} | sed "s/_/ /g" | awk "{print $"2"}")
        tests=$(echo -e ${TESTS} | sed "s/,/ /g" | awk "{print $"${i}"}")

        if [[ -n "$locale" ]] && [[ -n "$version" ]]; then
            if [[ -n "$tests" ]]; then
                MANUAL_UPDATE_TESTS=${MANUAL_UPDATE_TESTS}","${TESTS}
                BACKGROUND_UPDATE_TESTS=${BACKGROUND_UPDATE_TESTS}","${TESTS}
            fi
            echo -e "\n\n${GREEN}Starting MANUAL update test: ${NC}\n"

            echo -e "LOCALE = $locale"
            echo -e "FIREFOX VERSION = $version"
            echo -e "CHANNEL = $CHANNEL\n\n"

            pipenv run iris -l ${locale} -f ${version} -u ${CHANNEL} -t ${MANUAL_UPDATE_TESTS} -o

            echo -e "\n\n${GREEN}Starting BACKGROUND update test: ${NC}\n"

            echo -e "LOCALE = $locale"
            echo -e "FIREFOX VERSION = $version"
            echo -e "CHANNEL = $CHANNEL\n\n"

            pipenv run iris -l ${locale} -f ${version} -u ${CHANNEL} -t ${BACKGROUND_UPDATE_TESTS} -o
        fi
    done
else
    echo -e "\n\n${RED}A Firefox build has not been specified. ${NC}\n"
fi