#!/bin/sh

pipenv run flask publ reindex
FLASK_ENV=development FLASK_DEBUG=1 pipenv run flask run
