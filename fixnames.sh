#!/bin/sh
set -e
cd "$(dirname "$0")"
poetry install
poetry run flask publ reindex
poetry run python3 ./fix_dates.py

