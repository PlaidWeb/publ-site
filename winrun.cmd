@ECHO OFF
TITLE Publ Service
ECHO Starting up Publ...

SET PORT=5000
SET FLASK_DEBUG=1
set FLASK_ENV=development
set FLASK_APP=main.py
pipenv run flask run
