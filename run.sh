#!/bin/sh

FLASK_ENV=development FLASK_DEBUG=1 FLASK_APP=main.py pipenv run flask run
