#!/bin/sh
set -e
cd "$(dirname "$0")"
poetry install
poetry run flask publ reindex

poetry run flask publ normalize -var \
    -f '_{type}-{slug}' \
    -F '' '{date}-{sid} {title}' \
    blog

