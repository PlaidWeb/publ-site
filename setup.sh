#!/bin/sh

if ! which pipenv > /dev/null ; then
    for cmd in pip3 pip easy_install ; do
        if which $cmd > /dev/null ; then
            echo "\
Couldn't find pipenv; please install it with e.g.

    $cmd install -u pipenv
"
            exit 1
        fi
    done
    echo "\
Couldn't find pipenv or an appropriate tool to install it; please check your
Python installation for a current version of pip.
"
    exit 1
fi

if ! pipenv --venv > /dev/null ; then
    # We don't have a VEnv yet, so let's make sure we create one with Python 3
    echo "Creating new environment"
    pipenv --three install
else
    echo "Installing dependencies"
    pipenv install
fi

echo "Setup complete."
