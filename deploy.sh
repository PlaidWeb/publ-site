#!/bin/sh
# wrapper script to pull the latest site content and redeploy

cd  $(dirname $0)
export PATH=$PATH:$HOME/.poetry/bin

# see where in the history we are now
PREV=$(git rev-parse --short HEAD)

git pull --ff-only || exit 1

if git diff --name-only $PREV | grep -qE '^(templates/|app\.py|users\.cfg)' ; then
    echo "Configuration or template change detected"
    disposition=reload-or-restart
fi

if git diff --name-only $PREV | grep -q poetry.lock ; then
    echo "poetry.lock changed"
    poetry install || exit 1
    disposition=restart
fi

if [ "$1" != "nokill" ] && [ ! -z "$disposition" ] ; then
    systemctl --user $disposition publ.plaidweb.site.service
fi

echo "Updating the content index..."
poetry run flask publ reindex

count=0
while [ $count -lt 5 ] && [ ! -S $HOME/.vhosts/publ.beesbuzz.biz ] ; do
    count=$(($count + 1))
    echo "Waiting for service to restart... ($count)"
    sleep $count
done

poetry run pushl -rvvc $HOME/var/pushl http://publ.plaidweb.site/feed https://publ.plaidweb.site/feed
