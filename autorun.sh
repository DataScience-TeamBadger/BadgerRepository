#!/bin/sh
# Autorun script for project
# by Alex Kerzner


# Verify that BADGER_ROOT environment variable exists
#if [ -z ${BADGER_ROOT+set} ]
# Set BADGER_ROOT to current working directory
#set BADGER_ROOT="$pwd"

#:RUN_PROGRAM
#REM BADGER_ROOT is set

#echo Working directory: $BADGER_ROOT

# Run the program
#@ECHO ON
python ./bin/BadgerDataScience.py
