#!/bin/sh

if ! which pipenv > /dev/null ; then
    echo "Couldn't find pipenv"
    exit 1
fi

echo "Configuring environment..."

pipenv --three install

# Restart Passenger (at least per Dreamhost's config)
mkdir -p tmp
touch tmp/restart.txt

echo "Setup complete."
