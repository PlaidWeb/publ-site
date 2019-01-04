#!/bin/sh

if ! which pipenv > /dev/null ; then
    echo "Couldn't find pipenv"
    exit 1
fi

if ! pipenv --venv ; then
    # We don't have a VEnv yet, so let's make sure we create one with Python 3
    echo "Creating new environment"
    pipenv --three install
else
    echo "Installing dependencies"
    pipenv install
fi

# Restart Passenger (at least per Dreamhost's config)
mkdir -p tmp
touch tmp/restart.txt

echo "Setup complete."
