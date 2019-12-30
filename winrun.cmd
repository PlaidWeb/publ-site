@ECHO OFF
TITLE Publ Service
ECHO Starting up Publ...

SET FLASK_RUN_PORT=5000
SET FLASK_DEBUG=1
set FLASK_ENV=development
pipenv run flask run
