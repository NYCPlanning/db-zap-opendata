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
	# Avoiding Dubious Ownership in Dev Containers for git
	echo "Setting directiory as safe for git ..."
	git config --global --add safe.directory $PWD
	# echo "Adding local SSH keys ..."
	# Add local SSH private keys in order to push to github from the dev container
	# ssh-add
fi

echo "Done setting up dev container"
