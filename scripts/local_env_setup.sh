#!/usr/bin/env bash

# Script to set up local environment in a mac for Taverna API project
set -e
set -o pipefail

# Install python3 if absent
if which python3; then
    echo "Python3 present. Moving on..."
else
    echo "Installing Python3...."
    brew install python3
fi

# Install virtualenvwrapper if absent
if pip freeze | grep virtualenvwrapper; then
    echo "Virtualenvwrapper present. Moving on..."
else
    echo "Installing Virtualenvwrapper....."
    echo "You might be prompted to enter your password for this installation to continue."
    sudo pip install virtualenvwrapper

    # Prompt user to enter path to shell start up file
    echo "Enter the path to your shell start up file."
    echo "For example: ~/.bash_profile"
    read -p -r "SHELL START UP FILE: " SHELL_START_UP_FILE

    # Stop executing script if no shell start up file is given
    if [ -z "$SHELL_START_UP_FILE" ]; then
        echo "You did not specify the path to your shell startup file"
        echo "Exiting script. Please re-run script to continue installation!"
        exit 1
    fi

    # Check if shell start up file exists and add virtualenvwrapper configuration
    if [ -f "$SHELL_START_UP_FILE" ]; then
        echo "Adding virtualenvwrapper configuration to $SHELL_START_UP_FILE"
        echo "export WORKON_HOME=$HOME/.virtualenvs
            export PROJECT_HOME=$HOME/Devel
            source /usr/local/bin/virtualenvwrapper.sh" >> $SHELL_START_UP_FILE

        # Reload the startup file
        source $SHELL_START_UP_FILE
    else
        echo "Path to shell start up file does not exist!"
        echo "Exiting script. Please re-run script to continue installation!"
    fi
fi
