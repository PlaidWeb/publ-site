#!/bin/sh

poetry install
poetry run flask publ reindex
FLASK_ENV=development FLASK_DEBUG=1 poetry run flask run
