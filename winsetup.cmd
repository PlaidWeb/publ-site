@ECHO OFF
TITLE Publ Setup

poetry env info
IF %ERRORLEVEL% NEQ 0 (
    ECHO Running first-time install...
    pip -q install poetry
    poetry install
)

if %ERRORLEVEL% EQU 0 ECHO Install complete.
