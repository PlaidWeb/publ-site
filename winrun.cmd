@ECHO OFF
TITLE Publ Service
ECHO Starting up Publ...

SET PORT=5000
pipenv run python main.py
