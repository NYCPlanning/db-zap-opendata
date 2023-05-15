#!/bin/bash
#
# Sets up environment for dev in local dev container.
set -e
SCRIPT_DIRECTORY=$( dirname -- "$0"; )

echo "Setting up dev container from $SCRIPT_DIRECTORY/ ..."

# create an empty .env if it doesn't exist
touch $SCRIPT_DIRECTORY/.env

# only do this when running locally (rather than in a github action)
if [[ ${CI} != "true" ]]; then
	echo "Adding local SSH keys ..."
	# Add local SSH private keys in order to push to github from the dev container
	git config --global --add safe.directory $PWD
	# ssh-add
fi

echo "Done setting up dev container"
