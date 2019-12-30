#!/bin/sh
# wrapper script to pull the latest site content and redeploy

cd  $(dirname $0)
git pull --ff-only || exit 1

if git diff --name-only HEAD@{1} | grep -q Pipfile.lock ; then
    echo "Pipfile.lock changed; redeploying"
    pipenv install || exit 1
fi

if [ "$1" != "nokill" ] &&
    git diff --name-only HEAD@{1} | grep -qE '^(templates/|app\.py)'
then
    echo "Configuration or template change detected; Restarting web services"
    systemctl --user restart publ.beesbuzz.biz.service
fi
