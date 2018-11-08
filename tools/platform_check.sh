#!/bin/bash

chmod +x help_script.sh

# ----------------------------------
#       Defined variables
# ----------------------------------
#EDITOR=vim
#PASSWD=/etc/passwd
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
STD='\033[0;0;39m'
C='\u2714'
X='\u2716'
A='\u2192'


help_script(){

    if [[ "$OSTYPE" == "linux-gnu" ]]; then
            echo -e "\n${GREEN} ----- Linux support script called ----- ${STD}\n"

            echo -e "\n${GREEN}${A} You are running on : ${STD}\n"

            lsb_release -a
            hostnamectl

            echo -e "\n\n ${A} Checking type of Linux distribution \n"
            if [[ $(lsb_release -si) == 'Ubuntu' ]]; then
                echo -e "${GREEN}  --->  ${C} You are running on Ubuntu linux distribution. ${C} ${STD}\n"

                 echo -e "\n ${A} Checking Ubuntu version \n"
                if [[ $(lsb_release -sr) == '16.04' ]]; then
                    echo -e "${GREEN}  ---> ${C} Ubuntu is the correct version --> $(lsb_release -sr). ${C} ${STD}\n"
                else
                    echo -e "\n${RED}  ---> ${X} Error... Ubuntu $(lsb_release -sr) is NOT fully supported yet. ${X} ${STD}\n"
                fi
            else
                echo -e "\n${RED}  ---> ${X} Error... $(lsb_release -si) linux distribution is NOT supported. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Getting info on displays connected: \n"
            if [[ $(xrandr | grep -sw 'connected' | wc -l) > '1' ]]; then
                echo -e "${GREEN}  ---> ${C} You have multiple displays connected: ${STD} \n\n$(xrandr | grep -sw 'connected')\n"
            else
                echo -e "${GREEN}  ---> ${C} You have only one connected: ${STD} \n\n$(xrandr | grep -sw 'connected')\n"
            fi


            echo -e "\n ${A} Checking screen resolution. It should be greater than ${A} 1280x800. \n"
            if [[ $(xdpyinfo | grep dimensions | sed -r 's/^[^0-9]*([0-9]+x[0-9]+).*$/\1/') > '1280x800' ]]; then
                echo -e "${GREEN}  ---> ${C} Your screen resolution is $(xdpyinfo | grep dimensions | sed -r 's/^[^0-9]*([0-9]+x[0-9]+).*$/\1/') ${C} ${STD}\n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Your screen resolution is $(xdpyinfo | grep dimensions | sed -r 's/^[^0-9]*([0-9]+x[0-9]+).*$/\1/') ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if Python2 is installed \n"
            if command -v python2 &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Python 2.7 is installed. ${C} ${STD}\n"
                $(python --version)
                echo -e "\n  ---> Location: $(which python) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Python 2.7 is not installed. ${X} ${STD} Your Python default version is: $(python --version)\n"
            fi


            echo -e "\n ${A} Checking if Pip is installed \n"
            if command -v pip &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Pip is installed. ${C} ${STD} Version: $(pip --version)"
                echo -e "\n  ---> Location: $(which pip) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Pip not found. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if Pipenv is installed \n"
            if command -v pipenv &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Pipenv is installed. ${C} ${STD} Version: $(pipenv --version)"
                echo -e "\n  ---> Location: $(which pipenv) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Pipenv not installed. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if Virtualenv is installed \n"
            if command -v virtualenv &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Virtualenv is installed. ${C} ${STD} Version: $(virtualenv --version)"
                echo -e "\n  ---> Location: $(which virtualenv) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Virtualenv is not installed. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if Git is installed \n"
            if command -v git &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Git is installed. ${C} ${STD} Version: $(git --version)"
                echo -e "\n  ---> Location: $(which git) \n"
            else
                echo -e "\n${RED} ${X} --->  Error... Git not installed. Please install Git. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if Firefox is installed \n"
            if [[ $(which firefox) == '/usr/bin/firefox' ]]; then
                echo -e "${GREEN}  ---> ${C} Firefox is installed. ${C} ${STD}$ Version: $(firefox --version)"
                echo -e "\n  ---> Location: $(which firefox) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Firefox not installed. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if Tesseract is installed \n"
            if command -v tesseract &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Tesseract is installed. ${C} ${STD} Version: \n\n$(tesseract -v)"
                echo -e "\n  ---> Location: $(which tesseract) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Tesseract not found installed. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if 7zip is installed \n"
            if command -v p7zip &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} 7zip is installed. ${C} ${STD}"
                echo -e "\n  ---> Location: $(which p7zip) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... 7zip not found. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if Scrot library is installed \n"
            if command -v scrot --help &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Scrot is installed. ${C} ${STD} Version: $(scrot --version)"
                echo -e "\n  ---> Location: $(which scrot) \n"
            else
                echo -e "\n${RED} ${X} --->  Error... Scrot library not installed. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if Xsel library is installed \n"
            if command -v xsel --help &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Xsel is installed. ${C} ${STD} Version: $(xsel --version)"
                echo -e "\n  ---> Location: $(which xsel) \n"
            else
                echo -e "\n${RED} ${X} --->  Error... Xsel library not installed. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if wmctrl library is installed \n"
            if command -v wmctrl &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} wmctrl is installed. ${C} ${STD} Version: $(wmctrl --version)"
                echo -e "\n  ---> Location: $(which wmctrl) \n"
            else
                echo -e "\n${RED} ${X} --->  Error... wmctrl library not installed. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if xdotool library is installed \n"
            if command -v xdotool &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} xdotool is installed. ${C} ${STD} Version: $(xdotool --version)"
                echo -e "\n  ---> Location: $(which xdotool) \n"
            else
                echo -e "\n${RED} ${X} --->  Error... xdotool library not installed. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking for keyboard modifiers \n"
            if [[ $(xset q | awk '/LED/{ print $10 }' | grep -o '.$') == '1' ]]; then
                echo -e "\n${RED}  ---> ${X} Error... Caps Lock is turned on. Please turn it off. ${X} ${STD}\n"
            elif [[ $(xset q | awk '/LED/{ print $10 }' | grep -o '.$') == '2' ]]; then
                echo -e "\n${RED}  ---> ${X} Error... Num Lock is turned on. Please turn it off. ${X} ${STD}\n"
            elif [[ $(xset q | awk '/LED/{ print $10 }' | grep -o '.$') == '3' ]]; then
                echo -e "\n${RED}  ---> ${X} Error... Caps Lock and Num Lock are turned on. Please turn them off. ${X} ${STD}\n"
            else
                echo -e "${GREEN}  ---> ${C} Keyboard modifiers are all OFF. ${C} ${STD}\n"
            fi


            exit 1

    elif [[ "$OSTYPE" == "darwin"* ]]; then

            echo -e "\n${GREEN} ----- Mac support script called ----- ${STD}\n"

            echo -e "\n${GREEN} → You are running on : ${STD}\n"

            sw_vers
            system_profiler SPHardwareDataType

            echo -e "\n → Checking Mac OS version \n"
            os_ver=$(sw_vers -productVersion)

            # string comparison
            if [[ "$os_ver" =~ 10.14.* ]]; then
                echo -e "${RED}  ---> ✘ You are using MacOS Mojave "$os_ver". We currently do NOT fully supported it yet. ✘ ${STD}\n"
            elif [[ "$os_ver" =~ 10.13.* ]]; then
                echo -e "${GREEN}  ---> √ You are running on Mac OS High Sierra. √ ${STD}\n"
            elif [[ "$os_ver" =~ 10.12.* ]]; then
                echo -e "${GREEN}  ---> √ You are running on Mac OS Sierra. We recommend updating to High Sierra. √ ${STD}\n"
            else
                echo -e "${RED}  ---> ✘ MacOS X version: "$os_ver". We recommend using a higher version of Mac OS. ✘ ${STD}\n"
            fi


            echo -e "\n → Checking if multiple displays connected: \n"
            if [[ $(system_profiler SPDisplaysDataType | grep -sw 'Display Type' | wc -l) > '1' ]]; then
                echo -e "${GREEN}  ---> √ You have multiple displays connected: ${STD} \n\n$(system_profiler SPDisplaysDataType | grep -sw 'Display Type')\n$(system_profiler SPDisplaysDataType | grep -sw 'Resolution')"
            else
                echo -e "${GREEN}  ---> √ You have only one display connected: ${STD} \n\n$(system_profiler SPDisplaysDataType | grep -sw 'Display Type')\n$(system_profiler SPDisplaysDataType | grep -sw 'Resolution')"
            fi


            echo -e "\n → Checking if Display is Retina \n"
            if [[ $(system_profiler SPDisplaysDataType | grep 'Resolution') =~ 'Retina' ]]; then
                echo -e "${GREEN}  ---> √ Your display is Retina √ ${STD}  \n$(system_profiler SPDisplaysDataType | grep 'Retina')\n"
            else
                echo -e "${GREEN}  ---> √ Your display is Non-Retina √ ${STD}  \n$(system_profiler SPDisplaysDataType | grep -sw 'Display Type')\n"
            fi


            echo -e "\n → Checking screen resolution \n"
            if [[ $(system_profiler SPDisplaysDataType | awk '/Resolution/ { print $2$3$4 }') > '1280x800' ]]; then
                echo -e "${GREEN}  ---> √ Screen resolution is greater than 1280x800. √ ${STD} Your screen resolution: $(system_profiler SPDisplaysDataType | awk '/Resolution/ { print $2$3$4 }')\n"
            else
                echo -e "\n${RED}  ---> ✘ Error... Screen resolution must be greater than 1280x800. ✘ ${STD} Your screen resolution: $(system_profiler SPDisplaysDataType | awk '/Resolution/ { print $2$3$4 }')\n"
            fi


            echo -e "\n → Checking if Homebrew is installed \n"
            if command -v brew &>/dev/null; then
                echo -e "${GREEN}  ---> √ Homebrew is installed. √ ${STD} Version: $(brew --version)"
                echo -e "\n  ---> Location: $(which brew) \n"
            else
                echo -e "\n${RED}  ---> ✘ Error... Homebrew not found. Please run Iris Bootstrap. ✘ ${STD}\n"
            fi


            echo -e "\n → Checking if Python2 is installed \n"
            if command -v python2 &>/dev/null; then
                echo -e "${GREEN}  ---> √ Python 2.7 is installed. √ ${STD}\n"
                echo -e "Version: "
                $(python --version)
                echo -e "\n  ---> Location: $(which python) \n"
            else
                echo -e "\n${RED}  ---> ✘ Error... Python 2.7 is not installed. ✘ ${STD} Your Python default version is: $(python --version)\n"
            fi


            echo -e "\n → Checking if Pip is installed \n"
            if command -v pip &>/dev/null; then
                echo -e "${GREEN}  ---> √ Pip is installed. √ ${STD} Version: $(pip --version)"
                echo -e "\n  ---> Location: $(which pip) \n"
            else
                echo -e "\n${RED}  ---> ✘ Error... Pip not found. Please run the Iris Bootstrap. ✘ ${STD}\n"
            fi


            echo -e "\n Checking if Pipenv is installed \n"
            if command -v pipenv &>/dev/null; then
                echo -e "${GREEN}  ---> √ Pipenv is installed. √ ${STD} Version: $(pipenv --version)"
                echo -e "\n  ---> Location: $(which pipenv) \n"
            else
                echo -e "\n${RED}  ---> ✘ Error... Pipenv not installed. Please run the Iris Bootstrap. ✘ ${STD}\n"
            fi


            echo -e "\n → Checking if Virtualenv is installed \n"
            if command -v virtualenv &>/dev/null; then
                echo -e "${GREEN}  ---> √ Virtualenv is installed. √ ${STD} Version: $(virtualenv --version)"
                echo -e "\n  ---> Location: $(which virtualenv) \n"
            else
                echo -e "\n${RED}  ---> ✘ Error... Virtualenv is not installed. Please run the Iris Bootstrap. ✘ ${STD}\n"
            fi


            echo -e "\n → Checking if Tesseract is installed \n"
            if command -v tesseract &>/dev/null; then
                echo -e "${GREEN}  ---> √ Tesseract is installed. √ ${STD} \nVersion: \n$(tesseract -v)"
                echo -e "\n  ---> Location: $(which tesseract) \n"
            else
                echo -e "\n${RED}  ---> ✘ Error... Tesseract not found installed. Please run the Iris Bootstrap. ✘ ${STD}\n"
            fi


            echo -e "\n → Checking if 7zip is installed \n"
            if [[ $(brew list | grep p7zip) == 'p7zip' ]]; then
                echo -e "${GREEN}  ---> √ 7zip is installed. √ ${STD} Info: \n$(brew info p7zip)"
            else
                echo -e "\n${RED}  ---> ✘ Error... 7zip not found installed. Please run the Iris Bootstrap. ✘ ${STD}\n"
            fi


            echo -e "\n → Checking if XQuartz is installed \n"
            if [[ $(brew cask list | grep xquartz) == 'xquartz' ]]; then
                echo -e "${GREEN}  ---> √ XQuartz is installed. √ ${STD} Info: \n$(brew cask info xquartz)"
            else
                echo -e "\n${RED}  ---> ✘ Error... XQuartz not found installed. Please run the Iris Bootstrap. ✘ ${STD}\n"
            fi


            echo -e "\n → Checking if Pyobjc is installed \n"
            if [[ $(pip show pyobjc | grep Name:) =~ "pyobjc" ]]; then
                echo -e "${GREEN}  ---> √ Pyobjc is installed. √ ${STD} Info: \n$(pip show pyobjc)"
            else
                echo -e "\n${RED}  ---> ✘ Error... Pyobjc not found installed. Please run the Iris Bootstrap. ✘ ${STD}\n"
            fi


            echo -e "\n → Checking if Pyobjc-core is installed \n"
            if [[ $(pip show pyobjc-core | grep Name:) =~ "pyobjc-core" ]]; then
                echo -e "${GREEN}  ---> √ Pyobjc-core is installed. √ ${STD} Info: \n$(pip show pyobjc-core)"
            else
                echo -e "\n${RED}  ---> ✘ Error... Pyobjc-core not found installed. Please run the Iris Bootstrap. ✘ ${STD}\n"
            fi


            echo -e "\n → Checking if Firefox is installed \n"
            if [[ $(cd /Applications && ls | grep Firefox.app) == 'Firefox.app' ]]; then
                echo -e "${GREEN}  ---> √ Firefox is installed. √ ${STD} Version: $(/Applications/Firefox.app/Contents/MacOS/firefox --version)"
                echo -e "\n  ---> Location: /Applications/Firefox.app/Contents/MacOS/firefox \n"
            elif [[ $(cd /Applications && ls | grep "Firefox Developer Edition.app") == 'Firefox Developer Edition.app' ]]; then
                echo -e "${GREEN}  ---> √ Firefox Developer Edition is installed. √ ${STD} Version: $(/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox --version)"
                echo -e "\n  ---> Location: /Applications/Firefox Developer Edition.app/Contents/MacOS/firefox \n"
            elif [[ $(cd /Applications && ls | grep "Firefox Nightly.app") == 'Firefox Nightly.app' ]]; then
                echo -e "${GREEN}  ---> √ Firefox Nightly is installed. √ ${STD} Version: $(/Applications/Firefox Nightly.app/Contents/MacOS/firefox --version)"
                echo -e "\n  ---> Location: /Applications/Firefox Nightly.app/Contents/MacOS/firefox \n"
            else
                echo -e "\n${RED}  ---> ✘ Error... Could not find Firefox. Please make sure Firefox is installed. ✘ ${STD}\n"
            fi


            echo -e "\n → Checking if Git is installed \n"
            if command -v git &>/dev/null; then
                echo -e "${GREEN}  ---> √ Git is installed. √ ${STD} Version: $(git --version)"
                echo -e "\n  ---> Location: $(which git) \n"
            else
                echo -e "\n${RED} ---> ✘ Error... Git not installed. Plase make sure Git is installed. ✘ ${STD}\n"
            fi


            echo -e "\n → Checking for keyboard modifiers \n"
            if [[ $(xset q | awk '/LED/{ print $10 }' | grep -o '.$') == '1' ]]; then
                echo -e "\n${RED}  ---> ✘ Error... Caps Lock is turned on. Please turn it off. ✘ ${STD}\n"
            elif [[ $(xset q | awk '/LED/{ print $10 }' | grep -o '.$') == '2' ]]; then
                echo -e "\n${RED}  ---> ✘ Error... Num Lock is turned on. Please turn it off. ✘ ${STD}\n"
            elif [[ $(xset q | awk '/LED/{ print $10 }' | grep -o '.$') == '3' ]]; then
                echo -e "\n${RED}  ---> ✘ Error... Caps Lock and Num Lock are turned on. Please turn them off. ✘ ${STD}\n"
            else
                echo -e "${GREEN}  ---> √ Keyboard modifiers are all OFF. √ ${STD}\n"
            fi

            osascript -e 'quit app "Xquartz"'

            exit 1

    else
            echo -e "\n${GREEN} ----- Windows support script called ----- ${STD}\n"

            echo -e "\n${GREEN}${A} You are running on : ${STD}\n"
            powershell -Command "Get-CimInstance Win32_OperatingSystem | Select-Object  Caption, InstallDate, ServicePackMajorVersion, OSArchitecture, BootDevice,  BuildNumber, CSName | FL"


            echo -e "\n → Checking if multiple displays connected: \n"
            if [[ $(powershell -Command "Get-WmiObject win32_desktopmonitor" | grep 'DesktopMonitor' | wc -l) > '1' ]]; then
                echo -e "${GREEN}  ---> √ You have multiple displays connected: ${STD} \n$(powershell -Command "Get-WmiObject win32_desktopmonitor")"
            else
                echo -e "${GREEN}  ---> √ You have only one display connected: ${STD} \n$(powershell -Command "Get-WmiObject win32_desktopmonitor")"
            fi


            echo -e "\n ${A} Checking screen resolution. It should be greater than ${A} 1280x800. \n"
            if [[ $(powershell -Command "(Get-WmiObject -Class Win32_VideoController).VideoModeDescription;" | awk '{print $1$2$3;}') > '1280x800' ]]; then
                echo -e "${GREEN}  ---> ${C} Your screen resolution is $(powershell -Command "(Get-WmiObject -Class Win32_VideoController).VideoModeDescription;") ${C} ${STD}\n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Your screen resolution is $(powershell -Command "(Get-WmiObject -Class Win32_VideoController).VideoModeDescription;") ${X} ${STD}\n"
                echo $(powershell -Command "Get-WmiObject -Class Win32_DesktopMonitor | Select-Object ScreenWidth,ScreenHeight")
                echo $(powershell -Command "Get-WmiObject win32_videocontroller | select caption, CurrentHorizontalResolution, CurrentVerticalResolution")
            fi


            echo -e "\n → Checking if .NET Framework 4 is installed: \n"
            if [[ $(powershell -Command 'Get-ChildItem "HKLM:SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full\" | Get-ItemPropertyValue -Name Release | ForEach-Object { $_ -ge 394802 }') == 'True' ]]; then
                echo -e "${GREEN}  ---> ${C} .NET Framework 4 is installed. ${C} : ${STD}\n"
                echo $(powershell -Command "Get-ChildItem 'HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP' -recurse | Get-ItemProperty -name Version,Release -EA 0")
            else
                echo -e "${GREEN}  ---> ${C} .NET Framework 4 is NOT installed. Please follow Iris setup instructions. ${STD} \n$)"
            fi


            echo -e "\n ${A} Checking if Scoop is installed \n"
            if command -v scoop &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Scoop is installed. ${C} ${STD}"
                echo -e "\n  ---> Location: $(which scoop) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Scoop not found. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if Python 2.7 is installed \n"
            if command -v python2 &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Python 2.7 is installed. ${C} ${STD}"
                $(python --version)
                echo -e "\n  ---> Location: $(which python) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Python 2.7 not found. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if Git is installed \n"
            if command -v git &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Git is installed. ${C} ${STD} Version: $(git --version)"
                echo -e "\n  ---> Location: $(which git) \n"
                echo -e "\n $(scoop info git) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Git not found. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if Tesseract is installed \n"
            if command -v tesseract &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Tesseract is installed. ${C} ${STD} Version: \n\n$(tesseract -v)"
                echo -e "\n  ---> Location: $(which tesseract) \n"
                echo -e "\n $(scoop info tesseract) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Tesseract not found. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if 7zip is installed \n"
            if [[ $(scoop list | grep 7zip) =~ 7zip ]]; then
                echo -e "${GREEN}  ---> ${C} 7zip is installed. ${C} ${STD}"
                echo -e "\n $(scoop info 7zip) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... 7zip not found. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if Pip is installed \n"
            if command -v pip &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Pip is installed. ${C} ${STD} Version: $(pip --version)"
                echo -e "\n  ---> Location: $(which pip) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Pip not found. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n ${A} Checking if Pipenv is installed \n"
            if command -v pip &>/dev/null; then
                echo -e "${GREEN}  ---> ${C} Pipenv is installed. ${C} ${STD} Version: $(pipenv --version)"
                echo -e "\n  ---> Location: $(which pipenv) \n"
            else
                echo -e "\n${RED}  ---> ${X} Error... Pipenv not found. Please run the Iris Bootstrap. ${X} ${STD}\n"
            fi


            echo -e "\n → Checking for keyboard modifiers \n"
            if [[ $(powershell -Command "[console]::CapsLock") == 'True' ]]; then
                echo -e "\n${RED}  ---> ${X} Error... Caps Lock is turned on. Please turn it off. ${X} ${STD}\n"
            elif [[ $(powershell -Command "[console]::NumberLock") == 'True' ]]; then
                echo -e "\n${RED}  ---> ${X} Error... Num Lock is turned on. Please turn it off. ${X} ${STD}\n"
            else
                echo -e "${GREEN}  ---> ${C} Keyboard modifiers are all OFF. ${C} ${STD}\n"
            fi

            exit 1

    fi

}


show_menus() {
	clear
	echo "~~~~~~~~~~~~~~~~~~~~~~"
	echo " STARTING HELP SCRIPT "
	echo "~~~~~~~~~~~~~~~~~~~~~~"
	echo "                      "
}


while true
do
	show_menus
	help_script
	exit 1
done
