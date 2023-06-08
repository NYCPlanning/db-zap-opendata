#!/bin/bash
#
# Sets up environment for dev container
set -e
SCRIPT_DIRECTORY=$( dirname -- "$0"; )

echo "Running initializeCommand from $SCRIPT_DIRECTORY/ ..."

# create an empty .env if it doesn't exist to allow use of --env-file in runArgs
echo "If it doesn't exist, create an empty $SCRIPT_DIRECTORY/.env ..."
touch $SCRIPT_DIRECTORY/.env

# only do this when running locally (rather than in a github action)
if [[ ${CI} != "true" ]]; then
	# Avoiding git issues due to dubious ownership 
	echo "Setting directiory as safe for git ..."
	ssh-add
	git config --global --add safe.directory $PWD
fi

echo "Done running initializeCommand"
