#!/bin/sh
# wrapper script to pull the latest site content and redeploy

cd  $(dirname $0)

# see where in the history we are now
PREV=$(git rev-parse --short HEAD)

git pull --ff-only || exit 1

if git diff --name-only $PREV | grep -qE '^(templates/|app\.py|users\.cfg)' ; then
    echo "Configuration or template change detected"
    disposition=reload-or-restart
fi

if git diff --name-only $PREV | grep -q Pipfile.lock ; then
    echo "Pipfile.lock changed"
    pipenv install || exit 1
    disposition=restart
fi

if [ "$1" != "nokill" ] && [ ! -z "$disposition" ] ; then
    systemctl --user $disposition publ.beesbuzz.biz.service
fi
