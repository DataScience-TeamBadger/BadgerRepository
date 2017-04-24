@ECHO OFF
REM Autorun script for project
REM by Alex Kerzner


REM Verify that BADGER_ROOT environment variable exists
IF NOT "%BADGER_ROOT%"=="" GOTO RUN_PROGRAM
REM Set BADGER_ROOT to current working directory
SET BADGER_ROOT=%CD%

:RUN_PROGRAM
REM BADGER_ROOT is set

ECHO Working directory: '%BADGER_ROOT%'

REM Run the program
@ECHO ON
python.exe %BADGER_ROOT%\bin\BadgerDataScience.py
