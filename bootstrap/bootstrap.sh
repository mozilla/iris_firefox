#!/bin/bash
if which apt-get &>/dev/null
then
	echo "Bootstrapping for Linux / apt-get"
	echo "sudo required"
	sudo $(dirname "$0")/linux_bootstrap.sh
# elif which brew &>/dev/null
# then
	# Nothing for Mac right now
	# echo "Bootstrapping for Mac OS X / Homebrew"
	# $(dirname "$0")/osx_bootstrap.sh
# else
	# Nothing right now
fi
